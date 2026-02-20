"""Model specification."""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired
from .model_pricing import ModelPricing, ModelPricingTypedDict


class ModelSpecTypedDict(TypedDict):
    """Type dictionary for model specification."""
    
    model_id: str
    model_name: str
    model_slug: str
    context_window: int
    pricing: ModelPricingTypedDict
    creation_date: float


class ModelSpec(BaseModel):
    """Specification of an available model."""
    
    model_id: str
    model_name: str
    model_slug: str
    context_window: int = Field(default=4096)
    pricing: ModelPricing
    creation_date: float
    description: Optional[str] = None
    architecture: Optional[str] = None
    
    def __init__(
        self,
        model_id: str,
        model_name: str,
        model_slug: str,
        pricing: ModelPricing,
        creation_date: float,
        context_window: int = 4096,
        description: Optional[str] = None,
        architecture: Optional[str] = None,
        **kwargs
    ):
        """Initialize model specification."""
        super().__init__(
            model_id=model_id,
            model_name=model_name,
            model_slug=model_slug,
            context_window=context_window,
            pricing=pricing,
            creation_date=creation_date,
            description=description,
            architecture=architecture,
            **kwargs
        )
