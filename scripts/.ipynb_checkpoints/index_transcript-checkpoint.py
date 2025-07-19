# 📁 File: scripts/index_transcript.py

import os
import sys
import uuid
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.embedding_utils import load_embedder
from utils.chroma_utils import get_chroma_collection, add_to_chroma


def load_transcript(transcript_path):
    if not os.path.exists(transcript_path):
        raise FileNotFoundError("-- transcript_latest.txt not found. Run voice_input.py first!")

    with open(transcript_path, "r", encoding="utf-8") as f:
        latest_text = f.read().strip()

    #check for timestamp header
    lines = latest_text.splitlines()
    if len(lines) > 1 and lines[0].startswith("[") and lines[0].endswith("]"):
        timestamp = lines[0].strip("[] ")
        user_text = "\n".join(lines[1:]).strip()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_text = latest_text

    return timestamp, user_text


def main():
    print("🔍 Indexing latest transcript into ChromaDB...")
    transcript_path = os.path.join("assets", "voice_transcripts", "transcript_latest.txt")

    try:
        timestamp, user_text = load_transcript(transcript_path)

        embedder = load_embedder()
        collection = get_chroma_collection()

        unique_id = str(uuid.uuid4())

        add_to_chroma(
            collection=collection,
            texts=[user_text],
            metadatas=[{"timestamp": timestamp}],
            ids=[unique_id],
            embed_fn=embedder
        )

        print(f"-- Indexed transcript with ID: {unique_id}")
        print(f"-- Timestamp: {timestamp}")
        print(f"-- Content Preview:\n{user_text[:300]}...")

    except Exception as e:
        print(f"-- Error: {e}")


if __name__ == "__main__":
    main()
