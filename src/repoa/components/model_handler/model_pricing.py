"""Model pricing information."""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class ModelPricingTypedDict(TypedDict):
    """Type dictionary for model pricing."""
    
    prompt_cost: str
    completion_cost: str
    image_cost: NotRequired[Optional[str]]
    audio_cost: NotRequired[Optional[str]]


class ModelPricing(BaseModel):
    """Pricing information for a model."""
    
    prompt_cost: str = Field(default="0", description="Cost per million prompt tokens")
    completion_cost: str = Field(default="0", description="Cost per million completion tokens")
    image_cost: Optional[str] = None
    audio_cost: Optional[str] = None
    
    def __init__(
        self,
        prompt_cost: str = "0",
        completion_cost: str = "0",
        image_cost: Optional[str] = None,
        audio_cost: Optional[str] = None,
        **kwargs
    ):
        """Initialize model pricing."""
        super().__init__(
            prompt_cost=prompt_cost,
            completion_cost=completion_cost,
            image_cost=image_cost,
            audio_cost=audio_cost,
            **kwargs
        )
