"""Provider information and preferences."""

from __future__ import annotations
from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class ProviderInfoTypedDict(TypedDict):
    """Type dictionary for provider information."""
    
    provider_id: str
    provider_name: str
    is_available: bool
    performance_score: NotRequired[Optional[float]]


class ProviderInfo(BaseModel):
    """Information about an AI service provider."""
    
    provider_id: str
    provider_name: str
    is_available: bool = True
    performance_score: Optional[float] = None
    latency_ms: Optional[float] = None
    throughput_tokens_per_sec: Optional[float] = None


class ProviderPreferencesTypedDict(TypedDict):
    """Type dictionary for provider preferences."""
    
    enable_fallback: bool
    preferred_providers: NotRequired[List[str]]
    blocked_providers: NotRequired[List[str]]
    max_price_per_prompt: NotRequired[Optional[str]]


class ProviderPreferences(BaseModel):
    """User preferences for provider selection."""
    
    enable_fallback: bool = Field(default=True, description="Allow fallback to other providers")
    preferred_providers: List[str] = Field(default_factory=list)
    blocked_providers: List[str] = Field(default_factory=list)
    max_price_per_prompt: Optional[str] = None
    sort_by: Literal["price", "latency", "throughput"] = "latency"
    data_retention_policy: Literal["allow", "deny"] = "allow"
    
    def __init__(
        self,
        enable_fallback: bool = True,
        preferred_providers: Optional[List[str]] = None,
        blocked_providers: Optional[List[str]] = None,
        max_price_per_prompt: Optional[str] = None,
        sort_by: Literal["price", "latency", "throughput"] = "latency",
        data_retention_policy: Literal["allow", "deny"] = "allow",
        **kwargs
    ):
        """Initialize provider preferences."""
        super().__init__(
            enable_fallback=enable_fallback,
            preferred_providers=preferred_providers or [],
            blocked_providers=blocked_providers or [],
            max_price_per_prompt=max_price_per_prompt,
            sort_by=sort_by,
            data_retention_policy=data_retention_policy,
            **kwargs
        )
