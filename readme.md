# Reddit User Persona Generator

**About**  
This script scrapes Reddit posts/comments for a user and uses GPT to generate a persona (name, age, interests, tone), saving it as a `.txt` file.

**Setup**  
1. Clone this repo  
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a `.env` file (not included) with:
```
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
USER_AGENT=...
OPENAI_API_KEY=...
```
4. Run:
```
python user_persona.py
```

**Note:**  
Reddit & OpenAI require valid keys. If scraping fails (e.g., API rate limits or private app access), please refer to `persona_outputs/` for sample output files.
