from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

def split_pages(pages):

    chunks = []

    for page in pages:

        texts = splitter.split_text(page["text"])

        for chunk in texts:
            chunks.append({
                "page": page["page"],
                "text": chunk
            })

    return chunks