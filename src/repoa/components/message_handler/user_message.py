"""User message type."""

from __future__ import annotations
from typing import List, Optional, Union
from pydantic import Field, BaseModel
from typing_extensions import Annotated, TypedDict, NotRequired
from .base_types import BaseMessage, ContentBlock


class UserContentItemTypedDict(TypedDict):
    """Type dictionary for user content items."""
    
    type: str
    text: NotRequired[str]
    url: NotRequired[str]
    detail: NotRequired[str]


class UserContentItem(BaseModel):
    """Represents a content item in user message."""
    
    type: str
    text: Optional[str] = None
    url: Optional[str] = None
    detail: Optional[str] = None


class UserMessageTypedDict(TypedDict):
    """Type dictionary for user messages."""
    
    sender: str
    payload: Union[str, List[UserContentItemTypedDict]]
    timestamp: NotRequired[Optional[str]]
    session_id: NotRequired[Optional[str]]


class UserMessage(BaseMessage):
    """Represents a user message with support for multimodal content."""
    
    sender: str = "user"
    payload: Union[str, List[UserContentItem]] = Field(default="")
    timestamp: Optional[str] = None
    session_id: Optional[str] = None
    
    def __init__(
        self,
        payload: Union[str, List[UserContentItem]],
        sender: str = "user",
        timestamp: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ):
        """Initialize user message."""
        # Convert payload to content
        content = payload if isinstance(payload, str) else payload
        super().__init__(
            content=content,
            sender=sender,
            payload=payload,
            timestamp=timestamp,
            session_id=session_id,
            **kwargs
        )
