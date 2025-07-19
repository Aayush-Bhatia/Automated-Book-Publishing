
import os
import asyncio
import datetime
from utils import scraping, reviewer_agent, writer_agent, human_edit, reward_score
from scripts import merge_edits

# Step 1: Scrape Chapter from the given project URL
print("\n🔍 Scraping Chapter...")
screenshot_path = "assets/screenshots/chapter1.png"
raw_text_path = "assets/raw_text/chapter1.txt"
url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

async def run_scraping():
    await scraping.scrape_chapter(url, screenshot_path, raw_text_path)

asyncio.run(run_scraping())

#Generate improved versions
print("\n-- Generating Multiple Versions...")
with open(raw_text_path, "r", encoding="utf-8") as f:
    original_text = f.read()


chunks = original_text.split("\n\n")
chunks = [c for c in chunks if c.strip() != ""]
limited_text = "\n\n".join(chunks[:10])

versions = writer_agent.generate_versions(limited_text, n_versions=3)

os.makedirs("assets/spun_text", exist_ok=True)
for i, text in enumerate(versions):
    with open(f"assets/spun_text/version_{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(text)

#Reviewer Agent
print("\n-- Running Reviewer Agent...")

reviewed = reviewer_agent.reviewer_agent(limited_text)
os.makedirs("assets/reviewed_text", exist_ok=True)
with open("assets/reviewed_text/reviewed_chapter1.txt", "w", encoding="utf-8") as f:
    f.write(reviewed)

#Human Edit
print("\n-- Human Editing...")
human_edit.launch_edit_interface()

# Reward Evaluation (Basic RL Score)
print("\n-- Scoring Human Edit...")
raw = "assets/raw_text/chapter1.txt"
edited = "assets/human_edits/human_edit_latest.txt"
reward = reward_score.get_reward_score(open(edited, "r", encoding="utf-8").read())

result_path = "assets/rewards/human_edit_latest.json"
os.makedirs("assets/rewards", exist_ok=True)
with open(result_path, "w") as f:
    import json
    json.dump({"reward_score": reward}, f, indent=2)

print(f"-- Reward saved at: {result_path}")

# Merge All Edits into Final Book
print("\n-- Merging All Human Edits...")
merge_edits.merge_all_edits()

print("\n-- All essential steps completed successfully!")
