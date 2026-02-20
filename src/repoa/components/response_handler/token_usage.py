"""Token usage tracking."""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class TokenUsageTypedDict(TypedDict):
    """Type dictionary for token usage."""
    
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cache_read_tokens: NotRequired[Optional[int]]
    cache_write_tokens: NotRequired[Optional[int]]


class TokenUsage(BaseModel):
    """Tracks token usage for API calls."""
    
    prompt_tokens: int = Field(default=0, description="Tokens in prompt")
    completion_tokens: int = Field(default=0, description="Tokens in completion")
    total_tokens: int = Field(default=0, description="Total tokens used")
    cache_read_tokens: Optional[int] = None
    cache_write_tokens: Optional[int] = None
    
    def __init__(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        cache_read_tokens: Optional[int] = None,
        cache_write_tokens: Optional[int] = None,
        **kwargs
    ):
        """Initialize token usage."""
        total = prompt_tokens + completion_tokens
        super().__init__(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            **kwargs
        )
