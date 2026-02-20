"""Discriminated union of all message types."""

from __future__ import annotations
from typing import Union, Annotated
from pydantic import Discriminator, Tag
from typing_extensions import TypeAliasType

from .system_message import SystemMessage, SystemMessageTypedDict
from .user_message import UserMessage, UserMessageTypedDict
from .assistant_message import AssistantMessage, AssistantMessageTypedDict
from .tool_message import ToolMessage, ToolMessageTypedDict
from .text_message import TextMessage, TextMessageTypedDict


def get_message_type(msg_data: dict) -> str:
    """Extract message type from discriminator field."""
    if isinstance(msg_data, dict):
        # Try different discriminator fields
        if "agent" in msg_data and msg_data["agent"] == "assistant":
            return "assistant"
        elif "sender" in msg_data and msg_data["sender"] == "user":
            return "user"
        elif "instructions" in msg_data:
            return "system"
        elif "handler" in msg_data and msg_data["handler"] == "tool":
            return "tool"
        elif "response" in msg_data:
            return "assistant"
    return "text"


# Type alias for typed dicts
MessageTypedDict = TypeAliasType(
    "MessageTypedDict",
    Union[
        SystemMessageTypedDict,
        UserMessageTypedDict,
        AssistantMessageTypedDict,
        ToolMessageTypedDict,
        TextMessageTypedDict,
    ],
)

# Discriminated union with automatic type detection
Message = Annotated[
    Union[
        Annotated[SystemMessage, Tag("system")],
        Annotated[UserMessage, Tag("user")],
        Annotated[AssistantMessage, Tag("assistant")],
        Annotated[ToolMessage, Tag("tool")],
        Annotated[TextMessage, Tag("text")],
    ],
    Discriminator(lambda m: get_message_type(m.model_dump() if hasattr(m, "model_dump") else m)),
]
