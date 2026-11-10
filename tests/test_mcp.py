import pytest

from app.mcp_client import StemMCPClient

@pytest.mark.asyncio
async def test_mcp_tools():
    client = StemMCPClient()
    try:
        await client.connect()
        tools = await client.list_tools()
        tool_names = {tool.name for tool in tools}
        assert "solve_algebra" in tool_names
        assert "differentiate" in tool_names
        assert "integrate" in tool_names
        assert "find_limit" in tool_names
        assert "calculate_force" in tool_names
        assert "orbital_period" in tool_names
        assert "ohms_law" in tool_names
        assert "ideal_gas_law" in tool_names
        assert "base_convert" in tool_names
        assert "search_physics_knowledge" in tool_names
        assert "search_astronomy_knowledge" in tool_names
        assert "search_engineering_knowledge" in tool_names
        assert "search_chemistry_knowledge" in tool_names
        assert "search_computer_science_knowledge" in tool_names
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_differentiate():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("differentiate", {"expression": "x**3", "variable": "x"})
        assert result == "3*x**2"
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_search_math_knowledge():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("search_math_knowledge", {"query": "What is the value of pi?", "top_k": 2})
        assert "Pi" in result
        assert "3.141592653589793" in result
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_calculate_force():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("calculate_force", {"mass": 10, "acceleration": 5})
        assert float(result) == 50
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_search_physics_knowledge():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("search_physics_knowledge", {"query": "Newton's second law", "top_k": 2})
        assert "Newton" in result
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_search_astronomy_knowledge():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("search_astronomy_knowledge", {"query": "Kepler's laws", "top_k": 2})
        assert "Kepler" in result
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_search_engineering_knowledge():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("search_engineering_knowledge", {"query": "Ohm's law", "top_k": 2})
        assert "Ohm" in result
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_search_chemistry_knowledge():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("search_chemistry_knowledge", {"query": "ideal gas law", "top_k": 2})
        assert "gas" in result.lower()
    finally:
        await client.close()

@pytest.mark.asyncio
async def test_mcp_search_computer_science_knowledge():
    client = StemMCPClient()
    try:
        await client.connect()
        result = await client.call_tool("search_computer_science_knowledge", {"query": "Big O notation", "top_k": 2})
        assert "O(" in result
    finally:
        await client.close()
