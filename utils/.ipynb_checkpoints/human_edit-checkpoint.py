import os
import datetime

SPUN_DIR = "assets/spun_text"
REVIEWED_DIR = "assets/reviewed_text"
TRANSCRIPT_DIR = "assets/voice_transcripts"
EDITED_DIR = "assets/human_edits"

#output folder exists
os.makedirs(EDITED_DIR, exist_ok=True)

#editable text files
def list_all_versioned_files():
    versioned_files = []
    for folder in [SPUN_DIR, REVIEWED_DIR, TRANSCRIPT_DIR]:
        if os.path.exists(folder):
            for file in sorted(os.listdir(folder)):
                if file.endswith(".txt"):
                    versioned_files.append(os.path.join(folder, file))
    return versioned_files


def select_file(files):
    print("\n-- Available Files to Edit:\n")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    
    choice = int(input("\n-- Enter file number to edit: ")) - 1
    return files[choice]


def get_multiline_input():
    print("\n-- Enter your edits (type 'END' on a new line to finish):\n")
    lines = []
    while True:
        line = input()
        if line.strip().lower() == "end":
            break
        lines.append(line)
    return "\n".join(lines)


def save_edited_text(text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_path = os.path.join(EDITED_DIR, f"human_edit_{timestamp}.txt")
    latest_path = os.path.join(EDITED_DIR, "human_edit_latest.txt")

    with open(versioned_path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n-- Edit saved as version: {versioned_path}")
    print(f" -- Also updated: {latest_path}")


def launch_edit_interface():
    files = list_all_versioned_files()
    if not files:
        print("-:- No files found to edit.")
        return

    selected_file = select_file(files)
    with open(selected_file, "r", encoding="utf-8") as f:
        original = f.read()

    print("\n🧾 Original Content Preview:\n")
    print(original[:1000] + "...\n" if len(original) > 1000 else original)

    should_edit = input("-:- Do you want to edit this file? (yes/no): ").strip().lower()
    if should_edit != "yes":
        print("-- Edit cancelled.")
        return

    edited_text = get_multiline_input()
    save_edited_text(edited_text)


if __name__ == "__main__":
    launch_edit_interface()
