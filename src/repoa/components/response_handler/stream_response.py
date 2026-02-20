"""Streaming response types."""

from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired
from .token_usage import TokenUsage, TokenUsageTypedDict


class StreamingChoiceTypedDict(TypedDict):
    """Type dictionary for streaming choice."""
    
    index: int
    delta: dict
    finish_reason: NotRequired[Optional[str]]


class StreamingChoice(BaseModel):
    """Represents a streaming completion choice."""
    
    index: int
    delta: dict = Field(default_factory=dict)
    finish_reason: Optional[str] = None


class StreamResponseTypedDict(TypedDict):
    """Type dictionary for streaming response."""
    
    chunk_id: str
    choices: List[StreamingChoiceTypedDict]
    generation_timestamp: float
    model_deployed: str
    chunk_type: Literal["chat.completion.chunk"]
    usage: NotRequired[TokenUsageTypedDict]


class StreamResponse(BaseModel):
    """Represents a single streaming chunk in a response."""
    
    chunk_id: str
    choices: List[StreamingChoice] = Field(default_factory=list)
    generation_timestamp: float
    model_deployed: str
    chunk_type: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    usage: Optional[TokenUsage] = None
    
    def __init__(
        self,
        chunk_id: str,
        model_deployed: str,
        generation_timestamp: float,
        choices: Optional[List[StreamingChoice]] = None,
        usage: Optional[TokenUsage] = None,
        **kwargs
    ):
        """Initialize streaming response."""
        super().__init__(
            chunk_id=chunk_id,
            choices=choices or [],
            generation_timestamp=generation_timestamp,
            model_deployed=model_deployed,
            chunk_type="chat.completion.chunk",
            usage=usage,
            **kwargs
        )
