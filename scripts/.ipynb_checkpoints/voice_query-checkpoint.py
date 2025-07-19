import os
import sys
import time
sys.path.append(os.path.abspath(".."))

from utils.voice_input import record_voice, transcribe_and_append
from utils.embedding_utils import load_embedder
from utils.chroma_utils import get_chroma_collection, semantic_search

def main():
    duration = 10  # Record for 10 seconds (can make it CLI arg if needed)
    print(f"🎙️ Recording for {duration} seconds...")

    wav_path, timestamp = record_voice(duration)
    query = transcribe_and_append(wav_path, timestamp)

    if not query.strip():
        print("-- No recognizable speech detected.")
        return

    print(f"\n-- You asked: {query}")

    embedder = load_embedder()
    collection = get_chroma_collection()

    results = semantic_search(collection, query, embed_fn=embedder)

    print("\n-- Top Relevant Result:\n")
    print("-- Text:", results['documents'][0][0])
    print("-- Metadata:", results['metadatas'][0][0])

if __name__ == "__main__":
    main()
