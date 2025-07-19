from groq import Groq
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def get_reward_score(text):
    prompt = f"""
You are an AI reward model trained to evaluate book content drafts.

Your job is to assign a reward score (between 0 and 1) to the following text based on:
- Coherence
- Creativity
- Flow
- Grammar
- Story impact

Return ONLY a number between 0 and 1 (float). Do not add anything else.

--------------
{text}
--------------
"""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a reward scoring engine."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        score = response.choices[0].message.content.strip()
        return float(score)
    except Exception as e:
        print(f"-- Error in reward scoring: {e}")
        return -1.0


def score_versions(text_list):
    """
    Scores multiple text versions using get_reward_score.
    Returns list of tuples: (text, score)
    """
    results = []
    for idx, text in enumerate(text_list):
        print(f"-- Scoring version {idx+1}...")
        score = get_reward_score(text)
        results.append((text, score))
        time.sleep(1)  # prevent rate limit
    return results
