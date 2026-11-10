from mcp_server.rag import (
    create_vector_store,
    search_math_knowledge,
)


def main():
    create_vector_store()

    queries = [
        "What is the value of pi?",
        "Which mathematical constant is approximately 2.718?",
        "Tell me about the golden ratio",
        "What is the square root of 2?",
        "What constant is associated with harmonic series?",
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print("QUERY:", query)

        results = search_math_knowledge(query, top_k=2)

        for result in results:
            print("\nSOURCE:", result.metadata["source"])
            print(result.page_content[:500])


if __name__ == "__main__":
    main()