"""Base types and models for message handling."""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class ContentBlockTypedDict(TypedDict):
    """Type dictionary for content blocks."""
    text: NotRequired[str]
    data_type: str


class ContentBlock(BaseModel):
    """Represents a content block in a message."""
    
    text: Optional[str] = None
    data_type: str = "text"


class BaseMessageTypedDict(TypedDict):
    """Base type dictionary for messages."""
    
    content: Union[str, List[Dict[str, Any]]]
    metadata: NotRequired[Dict[str, Any]]
    msg_id: NotRequired[str]


class BaseMessage(BaseModel):
    """Base class for all message types."""
    
    content: Union[str, List[ContentBlock]]
    metadata: Optional[Dict[str, Any]] = None
    msg_id: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
