
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_versions(input_text, n_versions=3):
    versions = []
    for i in range(n_versions):
        prompt = f"""Improve the following book draft version while preserving its original meaning. Enhance grammar, tone, readability and also modify it so that it seems written by someone another:

--- Original ---
{input_text}
----------------

Respond with only the improved version. Do not explain anything."""

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            improved = response.choices[0].message.content.strip()
            versions.append(improved)

        except Exception as e:
            print(f"❌ Error in version {i+1}: {e}")
            versions.append(input_text)  # fallback

    return versions
