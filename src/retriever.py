import faiss
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_vector_store():

    index = faiss.read_index(
        str(PROJECT_ROOT / "vectorstore" / "faiss.index")
    )

    with open(
        PROJECT_ROOT / "vectorstore" / "chunks.pkl",
        "rb"
    ) as file:

        chunks = pickle.load(file)

    return index, chunks


def search(query, index, chunks, top_k=5):

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # Normalize query embedding
    faiss.normalize_L2(query_embedding)

    # Search using cosine similarity
    similarities, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for similarity, index_number in zip(
        similarities[0],
        indices[0]
    ):

        results.append({
            "text": chunks[index_number]["text"],
            "source": chunks[index_number]["source"],
            "page": chunks[index_number]["page"],
            "similarity": float(similarity)
        })

    return results


if __name__ == "__main__":

    index, chunks = load_vector_store()

    query = "What was Apple's total net sales in 2025?"

    results = search(
        query,
        index,
        chunks,
        top_k=5
    )

    print("\n==============================")
    print("SEARCH RESULTS")
    print("==============================")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {i}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(
            f"Cosine Similarity: "
            f"{result['similarity']:.4f}"
        )

        print("\nText:")
        print(result["text"][:500])

        print("-" * 50)