

import os
from datetime import datetime

EDITED_DIR = "assets/human_edits"
FINAL_BOOK_DIR = "assets/final_book"
os.makedirs(FINAL_BOOK_DIR, exist_ok=True)

def merge_all_edits():
    #human_edit_*.txt 
    all_files = sorted([
        f for f in os.listdir(EDITED_DIR)
        if f.endswith(".txt") and f.startswith("human_edit_") and "latest" not in f
    ])

    if not all_files:
        print("-- No human edits found. Please run the editing step first.")
        return

    #Output paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_txt_path = os.path.join(FINAL_BOOK_DIR, f"final_book_{timestamp}.txt")
    latest_path = os.path.join(FINAL_BOOK_DIR, "final_book_latest.txt")

    # Merge edits
    with open(final_txt_path, "w", encoding="utf-8") as outfile:
        for fname in all_files:
            chapter_path = os.path.join(EDITED_DIR, fname)
            with open(chapter_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(content.strip() + "\n\n" + "="*80 + "\n\n")

    #as latest
    with open(latest_path, "w", encoding="utf-8") as f_latest:
        with open(final_txt_path, "r", encoding="utf-8") as f_final:
            f_latest.write(f_final.read())

    print("-- Merging complete.")
    print("-- Final merged file saved at:", final_txt_path)
    print("-- Also updated:", latest_path)


if __name__ == "__main__":
    merge_all_edits()
