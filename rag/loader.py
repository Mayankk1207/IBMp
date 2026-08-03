import fitz

from rag.splitter import split_pages
from rag.embedding import embed
from rag.vectorstore import add_chunks


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)

    pages = []

    for page_num, page in enumerate(doc):
        pages.append(
            {
                "page": page_num + 1,
                "text": page.get_text()
            }
        )

    return pages


def process_pdf(pdf_path):

    pages = extract_text(pdf_path)

    chunks = split_pages(pages)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embed(texts)

    add_chunks(chunks, embeddings)