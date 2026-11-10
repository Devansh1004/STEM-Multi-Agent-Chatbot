import logging
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler

logger = logging.getLogger("agent")

class AgentTraceHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized: dict[str, Any], messages: list[Any], **kwargs: Any) -> None:
        logger.info("[LLM] Request sent")

    def on_tool_start(self, serialized: dict[str, Any], input_str: str, **kwargs: Any) -> None:
        tool_name = serialized.get("name", "unknown")
        logger.info("[AGENT] Executing tool: %s", tool_name)
        logger.info("[AGENT] Tool input: %s", input_str)

    def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        logger.info("[AGENT] Tool execution completed: %s", output)

    def on_chat_model_end(self, response: Any, **kwargs: Any) -> None:
        logger.info("[LLM] Response received")
