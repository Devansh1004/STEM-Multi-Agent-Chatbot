import sys
from mcp.server.mcpserver import MCPServer
from mcp_server.tools_math import solve_algebra, differentiate, integrate, find_limit, get_power
from mcp_server.tools_physics import calculate_force, kinematics_velocity
from mcp_server.tools_astronomy import orbital_period, escape_velocity
from mcp_server.tools_engineering import ohms_law, stress_calculation
from mcp_server.tools_chemistry import ideal_gas_law, ph_from_concentration
from mcp_server.tools_computer_science import base_convert, time_complexity_compare
from mcp_server.rag import (
    search_math_knowledge,
    search_physics_knowledge,
    search_astronomy_knowledge,
    search_engineering_knowledge,
    search_chemistry_knowledge,
    search_computer_science_knowledge,
)

mcp = MCPServer("stem-tools")

TOOLS = [
    solve_algebra,
    differentiate,
    integrate,
    find_limit,
    get_power,
    calculate_force,
    kinematics_velocity,
    orbital_period,
    escape_velocity,
    ohms_law,
    stress_calculation,
    ideal_gas_law,
    ph_from_concentration,
    base_convert,
    time_complexity_compare,
    search_math_knowledge,
    search_physics_knowledge,
    search_astronomy_knowledge,
    search_engineering_knowledge,
    search_chemistry_knowledge,
    search_computer_science_knowledge,
]

for tool in TOOLS:
    mcp.tool()(tool)

if __name__ == "__main__":
    print("Starting STEM MCP server...", file=sys.stderr)
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
