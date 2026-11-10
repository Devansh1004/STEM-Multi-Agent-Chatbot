from typing import Any

from pydantic import Field, create_model
from langchain_core.tools import StructuredTool

from app.mcp_client import StemMCPClient

def python_type_from_schema(schema: dict):
    schema_type = schema.get("type")
    if schema_type == "string":
        return str
    if schema_type == "integer":
        return int
    if schema_type == "number":
        return float
    if schema_type == "boolean":
        return bool
    return Any

def create_input_model(mcp_tool: Any):
    schema = mcp_tool.input_schema
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    fields = {}
    for name, property_schema in properties.items():
        python_type = python_type_from_schema(property_schema)
        if name in required:
            fields[name] = (python_type, Field(...))
        else:
            default = property_schema.get("default", None)
            fields[name] = (python_type | None, Field(default))
    return create_model(f"{mcp_tool.name.title()}Input", **fields)

def create_mcp_tool(client: StemMCPClient, mcp_tool: Any):
    input_model = create_input_model(mcp_tool)

    async def call_mcp_tool(**kwargs):
        return await client.call_tool(mcp_tool.name, kwargs)

    return StructuredTool.from_function(
        coroutine=call_mcp_tool,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        args_schema=input_model,
    )

async def create_mcp_tools(client: StemMCPClient):
    mcp_tools = await client.list_tools()
    tools = []
    for mcp_tool in mcp_tools:
        tools.append(create_mcp_tool(client, mcp_tool))
    return tools
