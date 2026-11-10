import asyncio
import logging
from app.callbacks import AgentTraceHandler
from app.agent import create_stem_agent
from app.mcp_client import StemMCPClient
from app.logging_config import setup_logging
from app.rate_limiter import RateLimiter

logger = logging.getLogger("main")

async def main():
    setup_logging()

    client = StemMCPClient()
    rate_limiter = RateLimiter(max_calls=25, period=60.0)

    try:
        await client.connect()

        agent = await create_stem_agent(client)

        print("\nSTEM Chatbot")
        print("Type 'exit' to quit.\n")

        trace_handler = AgentTraceHandler()
        history = []

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                break

            print("\n" + "=" * 60)
            logger.info("[USER] %s", user_input)
            print("=" * 60)

            messages = history + [{"role": "user", "content": user_input}]

            await rate_limiter.acquire()

            response = await agent.ainvoke(
                {"messages": messages},
                config={"callbacks": [trace_handler]},
            )

            response_messages = response["messages"]

            logger.info("[AGENT] Final response generated")

            ai_content = response_messages[-1].content

            print("\nAssistant:")
            print(ai_content)
            print("\n" + "=" * 60 + "\n")

            history = [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": ai_content},
            ]

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
