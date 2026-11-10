import pytest

from app.agent import create_stem_agent
from app.mcp_client import StemMCPClient

@pytest.mark.asyncio
async def test_agent_uses_math_knowledge_tool():
    client = StemMCPClient()
    try:
        await client.connect()
        agent = await create_stem_agent(client)
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "What is pi and what is its approximate value?"}]}
        )
        messages = response["messages"]
        tool_calls = []
        for message in messages:
            for call in getattr(message, "tool_calls", []):
                tool_calls.append(call["name"])
        assert "search_math_knowledge" in tool_calls
        final_response = messages[-1].content
        assert "3.141" in final_response
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_agent_uses_physics_tool():
    client = StemMCPClient()
    try:
        await client.connect()
        agent = await create_stem_agent(client)
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Calculate the force on a 10 kg object with acceleration 5 m/s^2."}]}
        )
        messages = response["messages"]
        tool_calls = []
        for message in messages:
            for call in getattr(message, "tool_calls", []):
                tool_calls.append(call["name"])
        assert "calculate_force" in tool_calls
    finally:
        await client.close()
