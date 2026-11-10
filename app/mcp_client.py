import logging
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

logger = logging.getLogger("mcp")

class StemMCPClient:
    def __init__(self, url: str = "http://127.0.0.1:8000/mcp"):
        self.url = url
        self._http_context = None
        self._session_context = None
        self.session = None

    async def connect(self):
        self._http_context = streamable_http_client(self.url)
        read, write = await self._http_context.__aenter__()
        self._session_context = ClientSession(read, write)
        self.session = await self._session_context.__aenter__()
        await self.session.initialize()
        logger.info("[MCP] Connected to %s", self.url)

    async def list_tools(self):
        result = await self.session.list_tools()
        logger.info("[MCP] Discovered tools: %s", ", ".join(tool.name for tool in result.tools))
        return result.tools

    async def call_tool(self, name: str, arguments: dict):
        logger.info("[MCP] Calling tool: %s", name)
        logger.info("[MCP] Arguments: %s", json.dumps(arguments))
        result = await self.session.call_tool(name, arguments=arguments)
        if result.content:
            output = result.content[0].text
        else:
            output = str(result)
        logger.info("[MCP] Result: %s", output)
        return output

    async def close(self):
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._http_context:
            await self._http_context.__aexit__(None, None, None)
        logger.info("[MCP] Connection closed")
