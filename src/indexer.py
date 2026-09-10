from pathlib import Path

from src.document_loader import load_all_pdfs
from src.chunking import create_chunks
from src.vector_store import create_vector_store, save_vector_store


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def rebuild_index():

    print("\nStarting knowledge base indexing...")

    documents = load_all_pdfs(PROJECT_ROOT / "data" / "documents")

    print(f"Total pages loaded: {len(documents)}")

    chunks = create_chunks(documents)

    print(f"Total chunks created: {len(chunks)}")

    index, chunks = create_vector_store(chunks)

    print(f"Total vectors created: {index.ntotal}")

    save_vector_store(index, chunks)

    print("Knowledge base indexing completed!")

    return len(documents), len(chunks)


if __name__ == "__main__":
    rebuild_index()