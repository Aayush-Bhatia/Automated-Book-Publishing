import os
import json
from groq import Groq
from textstat import flesch_reading_ease
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def calculate_reward(original_text, new_text):
    # Length score
    orig_len = len(original_text)
    new_len = len(new_text)
    length_score = 1 - abs(orig_len - new_len) / max(orig_len, new_len)

    
    readability = flesch_reading_ease(new_text)
    readability_score = min(readability / 100, 1)

    
    prompt = f"""Rate how human-like and coherent the following passage is, on a scale of 1 to 10:

---
{new_text}
---

Only reply with the number:"""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=5
        )
        score = float(response.choices[0].message.content.strip())
        human_like_score = min(max(score / 10, 0), 1)
    except:
        human_like_score = 0.5  # fallback

    # Final weighted score
    final = (
        0.4 * length_score +
        0.3 * readability_score +
        0.3 * human_like_score
    )

    return {
        "length_score": round(length_score, 3),
        "readability_score": round(readability_score, 3),
        "human_like_score": round(human_like_score, 3),
        "final_reward": round(final, 3)
    }

# ✅ CLI usage
def run_reward_comparison(original_path, edited_path):
    if not (os.path.exists(original_path) and os.path.exists(edited_path)):
        print("-- One or both files not found.")
        return

    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()

    with open(edited_path, "r", encoding="utf-8") as f:
        edited = f.read()

    result = calculate_reward(original, edited)

    print("\n-:- Reward Breakdown:\n")
    print(json.dumps(result, indent=2))

    os.makedirs("assets/rewards", exist_ok=True)
    out_name = os.path.basename(edited_path).replace(".txt", ".json")
    out_path = os.path.join("assets/rewards", out_name)

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n-- Reward saved at: {out_path}")


if __name__ == "__main__":
    
    raw = "assets/raw_text/chapter1.txt"
    edited = "assets/human_edits/human_edit_latest.txt"
    run_reward_comparison(raw, edited)
