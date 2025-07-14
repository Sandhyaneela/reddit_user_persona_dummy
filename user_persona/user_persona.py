import os
from dotenv import load_dotenv
import praw
import openai

# Load Reddit and OpenAI credentials from .env
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_username_from_url(url):
    return url.strip("/").split("/")[-1]

def scrape_user_data(username, limit=25):
    redditor = reddit.redditor(username)
    posts = []
    comments = []

    try:
        for post in redditor.submissions.new(limit=limit):
            posts.append(f"POST TITLE: {post.title}\nBODY: {post.selftext}\n")
    except Exception as e:
        print(f"Error fetching posts: {e}")

    try:
        for comment in redditor.comments.new(limit=limit):
            comments.append(f"COMMENT: {comment.body}\n")
    except Exception as e:
        print(f"Error fetching comments: {e}")

    return posts, comments

def generate_persona(posts, comments):
    joined_text = "\n".join(posts + comments)
    prompt = f"""
You are an intelligent assistant that builds detailed user personas.
Below are posts and comments from a Reddit user.

Your task is to generate a persona that includes:
- Fake Name (realistic)
- Age Range
- Interests or Hobbies
- Personality Traits
- Profession or Student
- Writing Style
- Any Political / Ideological leanings
- For each point, cite exactly which post or comment was used.

Here is the Reddit content:
{joined_text[:8000]}  # limit for OpenAI input
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response['choices'][0]['message']['content']

def save_output_to_file(username, persona_text):
    output_dir = "persona_outputs"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{username}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Persona saved to: {file_path}")

def main():
    url = input("Enter Reddit user profile URL: ").strip()
    username = extract_username_from_url(url)
    print(f"Fetching data for user: {username}")

    posts, comments = scrape_user_data(username)

    print(f"📝 Scraped {len(posts)} posts and {len(comments)} comments")
    persona = generate_persona(posts, comments)
    save_output_to_file(username, persona)

if __name__ == "__main__":
    main()
