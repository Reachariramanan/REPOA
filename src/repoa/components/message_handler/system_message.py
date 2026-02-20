"""System message type."""

from __future__ import annotations
from typing import Optional
from pydantic import Field
from typing_extensions import TypedDict, NotRequired
from .base_types import BaseMessage


class SystemMessageTypedDict(TypedDict):
    """Type dictionary for system messages."""
    
    instructions: str
    priority: NotRequired[int]
    context_scope: NotRequired[str]


class SystemMessage(BaseMessage):
    """Represents a system message with instructions/configuration."""
    
    instructions: str = Field(default="")
    priority: int = Field(default=0)
    context_scope: Optional[str] = None
    
    def __init__(
        self,
        instructions: str,
        priority: int = 0,
        context_scope: Optional[str] = None,
        **kwargs
    ):
        """Initialize system message."""
        super().__init__(
            content=instructions,
            instructions=instructions,
            priority=priority,
            context_scope=context_scope,
            **kwargs
        )
