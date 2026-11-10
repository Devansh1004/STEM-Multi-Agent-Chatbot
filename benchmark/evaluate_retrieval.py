import asyncio

from app.agent import create_stem_agent
from app.mcp_client import StemMCPClient
from app.rate_limiter import RateLimiter
from benchmark.dataset import BENCHMARK

def get_tool_calls(messages):
    tool_calls = []
    for message in messages:
        for call in getattr(message, "tool_calls", []):
            tool_calls.append(call["name"])
    return tool_calls

def evaluate_tool_selection(actual_tools, expected_tools):
    return set(actual_tools) == set(expected_tools)

def evaluate():
    asyncio.run(run_evaluation())

async def run_evaluation():
    client = StemMCPClient()
    rate_limiter = RateLimiter(max_calls=25, period=60.0)

    try:
        await client.connect()

        agent = await create_stem_agent(client)

        total = len(BENCHMARK)
        correct = 0
        tool_calls_total = 0
        tool_calls_successful = 0
        multi_tool_total = 0
        multi_tool_correct = 0

        results = []

        for index, item in enumerate(BENCHMARK, start=1):
            query = item["query"]
            expected = item["expected_tools"]

            print(f"\n[{index}/{total}] {query}")

            try:
                await rate_limiter.acquire()

                response = await agent.ainvoke(
                    {"messages": [{"role": "user", "content": query}]}
                )

                messages = response["messages"]
                actual = get_tool_calls(messages)

                tool_calls_total += len(expected)

                if actual:
                    tool_calls_successful += len(actual)

                selection_correct = evaluate_tool_selection(actual, expected)

                if selection_correct:
                    correct += 1

                if len(expected) > 1:
                    multi_tool_total += 1
                    if selection_correct:
                        multi_tool_correct += 1

                results.append({"query": query, "expected": expected, "actual": actual, "correct": selection_correct})

                status = "PASS" if selection_correct else "FAIL"

                print(f"  Expected: {expected}")
                print(f"  Actual:   {actual}")
                print(f"  [{status}]")

            except Exception as e:
                print(f"  ERROR: {e}")
                results.append({"query": query, "expected": expected, "actual": [], "correct": False})

        selection_accuracy = correct / total
        multi_tool_accuracy = multi_tool_correct / multi_tool_total if multi_tool_total else 0
        tool_success_rate = tool_calls_successful / tool_calls_total if tool_calls_total else 0

        print("\n" + "=" * 70)
        print("AGENT BENCHMARK")
        print("=" * 70)
        print(f"Tool Selection Accuracy: {selection_accuracy:.2%} ({correct}/{total})")
        print(f"MCP Tool Success Rate: {tool_success_rate:.2%}")
        print(f"Multi-Tool Accuracy: {multi_tool_accuracy:.2%} ({multi_tool_correct}/{multi_tool_total})")
        print("=" * 70)

    finally:
        await client.close()

if __name__ == "__main__":
    evaluate()
