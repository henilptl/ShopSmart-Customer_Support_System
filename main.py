"""CLI entry point.

    python -m src.main                       # run the five demo queries
    python -m src.main "Where is ORD-1005?"  # run a single query
"""

import sys

from dotenv import load_dotenv

load_dotenv()  # must run before src.nodes constructs the ChatOpenAI client

from .graph import build_graph  # noqa: E402

DEMO_QUERIES = [
    "Where is my order ORD-1005? It has been 10 days and I still haven't received my TV.",
    "I received a damaged Sony headphone in my order ORD-1002. The left ear cup is cracked. I want a replacement.",
    "I was charged twice for my MacBook Air order! ₹1,14,900 was deducted two times from my credit card.",
    "I'm looking for wireless earbuds under ₹2,000. What do you recommend? How are the Boat Airdopes?",
    "I ordered a Samsung Galaxy S24 three days ago. When will it be delivered to Mumbai?",
]


def run_support_agent(agent, query: str, verbose: bool = False) -> dict:
    """Stream the query through the graph and print the final state."""
    final_state = {}
    events = agent.stream(
        {"customer_query": query, "category": "", "priority": "", "response": ""},
        stream_mode="values",
    )

    print(f"\n{'=' * 60}")
    print(f"Customer Query: {query}")
    print("=" * 60)

    for event in events:
        if verbose:
            print(event)
        final_state = event

    print(f"\nCategory: {final_state.get('category')}")
    print(f"Priority: {final_state.get('priority')}")
    print(f"\nResponse:\n{final_state.get('response')}")
    return final_state


def main() -> None:
    agent = build_graph()
    queries = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else DEMO_QUERIES
    for query in queries:
        run_support_agent(agent, query)


if __name__ == "__main__":
    main()
