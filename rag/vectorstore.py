import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    "legal_docs"
)

def add_chunks(chunks, embeddings):

    collection.add(

        ids=[
            str(i)
            for i in range(len(chunks))
        ],

        documents=[
            c["text"]
            for c in chunks
        ],

        embeddings=embeddings,

        metadatas=[
            {
                "page": c["page"]
            }
            for c in chunks
        ]
    )