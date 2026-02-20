"""Assistant message type."""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired
from .base_types import BaseMessage


class ToolInvocation(BaseModel):
    """Represents a tool/function invocation."""
    
    invocation_id: str
    tool_name: str
    parameters: dict
    

class AssistantMessageTypedDict(TypedDict):
    """Type dictionary for assistant messages."""
    
    agent: str
    response: str
    tokens_used: NotRequired[Optional[int]]
    tool_invocations: NotRequired[List[dict]]
    stop_reason: NotRequired[str]


class AssistantMessage(BaseMessage):
    """Represents a message from an assistant/model."""
    
    agent: str = "assistant"
    response: str = Field(default="")
    tokens_used: Optional[int] = None
    tool_invocations: List[ToolInvocation] = Field(default_factory=list)
    stop_reason: Optional[str] = None
    
    def __init__(
        self,
        response: str,
        agent: str = "assistant",
        tokens_used: Optional[int] = None,
        tool_invocations: Optional[List[ToolInvocation]] = None,
        stop_reason: Optional[str] = None,
        **kwargs
    ):
        """Initialize assistant message."""
        super().__init__(
            content=response,
            agent=agent,
            response=response,
            tokens_used=tokens_used,
            tool_invocations=tool_invocations or [],
            stop_reason=stop_reason,
            **kwargs
        )
