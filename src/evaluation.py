import pandas as pd
from src.rag_pipeline import generate_answer

def evaluate_rag():

    df = pd.read_csv("data/evaluation_questions.csv")

    results = []

    print("\n==============================")
    print("RAG EVALUATION")
    print("==============================")

    for i, row in df.iterrows():

        question = row["question"]
        expected_answer = row["expected_answer"]

        print(f"\nQuestion {i + 1}: {question}")

        try:

            answer, sources = generate_answer(question)

            source_found = len(sources) > 0

            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "generated_answer": answer,
                "source_found": source_found,
                "top_source": (
                    sources[0]["source"]
                    if sources else ""
                ),
                "top_page": (
                    sources[0]["page"]
                    if sources else ""
                ),
                "similarity": (
                    sources[0]["similarity"]
                    if sources else ""
                )
            })

            print("Answer:", answer)
            print("Source found:", source_found)

        except Exception as e:

            print("\n❌ ERROR DETAILS:")
            print(type(e).__name__)
            print(str(e))

            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "generated_answer": "ERROR",
                "source_found": False,
                "top_source": "",
                "top_page": "",
                "similarity": ""
            })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        "data/evaluation_results.csv",
        index=False
    )

    print("\n==============================")
    print("EVALUATION COMPLETED")
    print("==============================")

    print(
        f"Questions evaluated: {len(results_df)}"
    )

    print(
        f"Questions with retrieved sources: "
        f"{results_df['source_found'].sum()}"
    )

    print("\nResults saved to:")
    print("data/evaluation_results.csv")

if __name__ == "__main__":
    evaluate_rag()