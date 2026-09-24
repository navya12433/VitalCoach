from rag.retriever import create_retriever


def evaluate_rag():

    print("=" * 60)
    print("VitalCoach RAG Evaluation")
    print("=" * 60)

    retriever = create_retriever()

    query = (
        "Physical activity recommendations for a beginner "
        "who wants to improve general fitness"
    )

    documents = retriever.invoke(query)

    print(f"\nRetrieved documents: {len(documents)}")

    if not documents:
        print("\nRAG Grounding: FAIL")
        return

    print("\nRetrieved guidance:\n")

    for index, document in enumerate(documents, start=1):

        print(f"--- Document {index} ---")
        print(document.page_content[:500])
        print()

    combined_text = " ".join(
        document.page_content.lower()
        for document in documents
    )

    grounding_terms = [
        "physical activity",
        "moderate",
        "vigorous",
        "week"
    ]

    matches = sum(
        1
        for term in grounding_terms
        if term in combined_text
    )

    print("=" * 60)

    if matches >= 2:
        print("RAG Grounding: PASS")
        print(
            "Retrieved documents contain relevant "
            "physical-activity guidance."
        )
    else:
        print("RAG Grounding: REVIEW")
        print(
            "Retrieved documents may not contain "
            "enough relevant guidance."
        )


if __name__ == "__main__":
    evaluate_rag()