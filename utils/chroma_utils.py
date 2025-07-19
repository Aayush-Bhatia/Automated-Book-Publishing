import chromadb

<<<<<<< HEAD

=======
# ✅ Use new PersistentClient without Settings
>>>>>>> 6f0beb6 (initial workflow done)
def get_chroma_collection(collection_name="transcript_store"):
    client = chromadb.PersistentClient(path=".chromadb")
    return client.get_or_create_collection(name=collection_name)

def add_to_chroma(collection, texts, metadatas, ids, embed_fn):
    embeddings = embed_fn.encode(texts).tolist()
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

def semantic_search(collection, query, embed_fn, n_results=3):
    embedding = embed_fn.encode([query]).tolist()[0]
    return collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
