"""Tool definition types."""

from __future__ import annotations
from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired


class ToolDefinitionFunctionTypedDict(TypedDict):
    """Type dictionary for tool function definition."""
    
    name: str
    description: NotRequired[str]
    parameters: NotRequired[Dict[str, Any]]
    strict: NotRequired[Optional[bool]]


class ToolDefinitionFunction(BaseModel):
    """Defines a function/tool that can be called."""
    
    name: str = Field(..., description="Function name")
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    strict: Optional[bool] = None


class ToolDefinitionTypedDict(TypedDict):
    """Type dictionary for complete tool definition."""
    
    type: Literal["function"]
    function: ToolDefinitionFunctionTypedDict


class ToolDefinition(BaseModel):
    """Complete definition of a callable tool."""
    
    type: Literal["function"] = "function"
    function: ToolDefinitionFunction
    
    def __init__(
        self,
        function: ToolDefinitionFunction,
        type: Literal["function"] = "function",
        **kwargs
    ):
        """Initialize tool definition."""
        super().__init__(
            type=type,
            function=function,
            **kwargs
        )
