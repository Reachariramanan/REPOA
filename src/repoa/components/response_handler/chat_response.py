"""Chat response types."""

from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired
from .token_usage import TokenUsage, TokenUsageTypedDict


class ChatResponseChoiceTypedDict(TypedDict):
    """Type dictionary for response choice."""
    
    index: int
    finish_reason: str
    generated_text: str
    logprobs: NotRequired[Optional[dict]]


class ChatResponseChoice(BaseModel):
    """Represents a single completion choice."""
    
    index: int
    finish_reason: str = Field(default="stop")
    generated_text: str = Field(default="")
    logprobs: Optional[dict] = None


class ChatResponseTypedDict(TypedDict):
    """Type dictionary for chat response."""
    
    response_id: str
    choices: List[ChatResponseChoiceTypedDict]
    generated_at: float
    deployed_model: str
    response_type: Literal["chat.completion"]
    usage: TokenUsageTypedDict
    fingerprint: NotRequired[Optional[str]]


class ChatResponse(BaseModel):
    """Complete chat response from an LLM."""
    
    response_id: str
    choices: List[ChatResponseChoice] = Field(default_factory=list)
    generated_at: float
    deployed_model: str
    response_type: Literal["chat.completion"] = "chat.completion"
    usage: TokenUsage
    fingerprint: Optional[str] = None
    
    def __init__(
        self,
        response_id: str,
        deployed_model: str,
        generated_at: float,
        usage: TokenUsage,
        choices: Optional[List[ChatResponseChoice]] = None,
        fingerprint: Optional[str] = None,
        **kwargs
    ):
        """Initialize chat response."""
        super().__init__(
            response_id=response_id,
            choices=choices or [],
            generated_at=generated_at,
            deployed_model=deployed_model,
            response_type="chat.completion",
            usage=usage,
            fingerprint=fingerprint,
            **kwargs
        )
