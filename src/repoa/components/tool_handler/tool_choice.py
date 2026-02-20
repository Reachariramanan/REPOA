"""Tool choice configuration."""

from __future__ import annotations
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class ToolChoice(BaseModel):
    """Specifies tool choice behavior."""
    
    mode: Literal["auto", "required", "none"] = Field(default="auto")
    preferred_tool: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        use_enum_values = True
    
    def __init__(
        self,
        mode: Literal["auto", "required", "none"] = "auto",
        preferred_tool: Optional[str] = None,
        **kwargs
    ):
        """Initialize tool choice."""
        super().__init__(
            mode=mode,
            preferred_tool=preferred_tool,
            **kwargs
        )
