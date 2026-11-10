import logging

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

from app.mcp_bridge import create_mcp_tools
from app.mcp_client import StemMCPClient

load_dotenv()

logger = logging.getLogger("agent")

async def create_stem_agent(client: StemMCPClient):
    tools = await create_mcp_tools(client)

    logger.info("[AGENT] Available tools: %s", [tool.name for tool in tools])

    # Reads ANTHROPIC_API_KEY from the environment / .env.
    # No temperature: sampling params are rejected (400) on Claude Opus 5.5.
    model = ChatAnthropic(model="claude-sonnet-5-5", max_tokens=16000)

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a STEM assistant covering mathematics, physics, astronomy, "
            "engineering, chemistry, and computer science. "
            "Use computation tools whenever the user asks you to solve, differentiate, "
            "integrate, find a limit, or calculate a physical, engineering, or scientific "
            "quantity such as force, velocity, orbital period, escape velocity, Ohm's law, "
            "stress, ideal gas law values, pH, base conversion, or time complexity. "
            "Use the relevant search_*_knowledge tool when the user asks about constants, "
            "definitions, laws, properties, or other factual knowledge in a given topic. "
            "If a question requires both factual knowledge and computation, use the "
            "appropriate tools for both. "
            "Do not perform calculations yourself when a computation tool is available. "
            "Base factual answers on retrieved knowledge when a knowledge tool is relevant. "
            "Give clear and concise explanations."
        ),
    )

    logger.info("[AGENT] Agent created successfully")

    return agent
