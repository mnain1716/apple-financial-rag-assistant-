from sentence_transformers import SentenceTransformer

from src.chunking import create_chunks
from src.document_loader import load_all_pdfs


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):

    texts = []

    for chunk in chunks:

        embedding_text = (
            f"Document: {chunk['source']}\n"
            f"Page: {chunk['page']}\n"
            f"Content: {chunk['text']}"
        )

        texts.append(embedding_text)

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


if __name__ == "__main__":

    # Load all PDF pages
    documents = load_all_pdfs("data/documents")

    # Create chunks
    chunks = create_chunks(documents)

    print(f"\nTotal chunks: {len(chunks)}")

    # Create embeddings
    embeddings = create_embeddings(chunks)

    print(f"Embedding shape: {embeddings.shape}")

    print(f"First embedding:\n{embeddings[0][:10]}")