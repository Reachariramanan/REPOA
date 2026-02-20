"""Text message content type."""

from __future__ import annotations
from typing import Optional
from pydantic import Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated, TypedDict
from .base_types import BaseMessage, ContentBlock


class TextMessageTypedDict(TypedDict):
    """Type dictionary for text messages."""
    
    content: str
    msg_id: Optional[str]


class TextMessage(BaseMessage):
    """Represents a simple text message."""
    
    content: str
    msg_id: Optional[str] = None
    
    def __init__(self, text_content: str, msg_id: Optional[str] = None, **kwargs):
        """Initialize text message."""
        super().__init__(content=text_content, msg_id=msg_id, **kwargs)
