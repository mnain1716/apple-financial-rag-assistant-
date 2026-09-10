import faiss
import numpy as np
import pickle
from pathlib import Path

from src.embeddings import create_embeddings
from src.chunking import create_chunks
from src.document_loader import load_all_pdfs


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def create_vector_store(chunks):

    embeddings = create_embeddings(chunks)

    embeddings = np.array(embeddings).astype("float32")

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Inner Product on normalized vectors = cosine similarity
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index, chunks


def save_vector_store(index, chunks):

    faiss.write_index(
        index,
        str(PROJECT_ROOT / "vectorstore" / "faiss.index")
    )

    with open(
        PROJECT_ROOT / "vectorstore" / "chunks.pkl",
        "wb"
    ) as file:

        pickle.dump(chunks, file)

    print("\nVector store saved successfully!")


if __name__ == "__main__":

    documents = load_all_pdfs(
        "data/documents"
    )

    chunks = create_chunks(documents)

    print(f"Total chunks: {len(chunks)}")

    index, chunks = create_vector_store(
        chunks
    )

    print(f"FAISS vectors: {index.ntotal}")

    save_vector_store(
        index,
        chunks
    )