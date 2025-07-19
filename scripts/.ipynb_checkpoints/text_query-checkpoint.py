import os
import sys
sys.path.append(os.path.abspath(".."))

from utils.embedding_utils import load_embedder
from utils.chroma_utils import get_chroma_collection, semantic_search

def main():
    embedder = load_embedder()
    collection = get_chroma_collection()

    query = input("❓ Ask something from the transcript or book: ").strip()

    if not query:
        print("-- Empty query provided.")
        return

    results = semantic_search(collection, query, embed_fn=embedder)

    print("\n-- Top Relevant Result:\n")
    print("-- Text:", results['documents'][0][0])
    print("-- Metadata:", results['metadatas'][0][0])

if __name__ == "__main__":
    main()
