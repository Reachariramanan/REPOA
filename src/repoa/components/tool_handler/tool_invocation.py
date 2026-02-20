"""Tool invocation types."""

from __future__ import annotations
from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class ToolInvocationStatusTypedDict(TypedDict):
    """Type dictionary for tool invocation status."""
    
    call_id: str
    status: Literal["pending", "executing", "completed", "failed"]
    result: NotRequired[Optional[Any]]
    error_msg: NotRequired[Optional[str]]


class ToolInvocationStatus(BaseModel):
    """Represents the status of a tool invocation."""
    
    call_id: str
    status: Literal["pending", "executing", "completed", "failed"] = "pending"
    result: Optional[Any] = None
    error_msg: Optional[str] = None


class ToolInvocationTypedDict(TypedDict):
    """Type dictionary for tool invocation."""
    
    invocation_id: str
    tool_name: str
    arguments: Dict[str, Any]
    call_timestamp: float


class ToolInvocation(BaseModel):
    """Represents a request to invoke a tool."""
    
    invocation_id: str
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    call_timestamp: float
    
    def __init__(
        self,
        invocation_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
        call_timestamp: float,
        **kwargs
    ):
        """Initialize tool invocation."""
        super().__init__(
            invocation_id=invocation_id,
            tool_name=tool_name,
            arguments=arguments,
            call_timestamp=call_timestamp,
            **kwargs
        )
