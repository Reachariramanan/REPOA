"""Tool message type."""

from __future__ import annotations
from typing import Optional, Any
from pydantic import Field
from typing_extensions import TypedDict, NotRequired
from .base_types import BaseMessage


class ToolMessageTypedDict(TypedDict):
    """Type dictionary for tool messages."""
    
    handler: str
    tool_call_id: str
    execution_result: Any
    execution_status: NotRequired[str]


class ToolMessage(BaseMessage):
    """Represents a response from a tool/function execution."""
    
    handler: str = "tool"
    tool_call_id: str = Field(default="")
    execution_result: Any = None
    execution_status: Optional[str] = None
    
    def __init__(
        self,
        tool_call_id: str,
        execution_result: Any,
        handler: str = "tool",
        execution_status: Optional[str] = None,
        **kwargs
    ):
        """Initialize tool message."""
        content_str = f"Tool {tool_call_id} result: {execution_result}"
        super().__init__(
            content=content_str,
            handler=handler,
            tool_call_id=tool_call_id,
            execution_result=execution_result,
            execution_status=execution_status,
            **kwargs
        )
