"""Node definitions for workflow execution."""

from __future__ import annotations
from typing import Callable, Dict, Any, Optional
from pydantic import BaseModel, Field
from .network_state import StateDict


# Type for node execution functions
NodeFunction = Callable[[StateDict], Dict[str, Any]]
"""Callable that takes state dict and returns updates dict."""


class Node(BaseModel):
    """
    Represents a single node in the workflow network.
    
    A node is a discrete unit of work that:
    - Takes current state as input
    - Performs some computation/side-effect
    - Returns state updates
    """
    
    node_id: str = Field(..., description="Unique identifier for this node")
    func: Optional[NodeFunction] = None
    func_name: str = Field(default="", description="Name of the function for serialization")
    description: Optional[str] = None
    timeout: Optional[float] = Field(default=None, description="Node execution timeout in seconds")
    retry_count: int = Field(default=0, description="Number of retry attempts on failure")
    is_agent: bool = Field(default=False, description="Whether this node runs an agent/LLM")
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def __init__(
        self,
        node_id: str,
        func: Optional[NodeFunction] = None,
        description: Optional[str] = None,
        timeout: Optional[float] = None,
        retry_count: int = 0,
        is_agent: bool = False,
        **kwargs
    ):
        """
        Initialize a workflow node.
        
        Args:
            node_id: Unique identifier for the node
            func: Function that executes the node logic
            description: Human-readable description
            timeout: Execution timeout in seconds
            retry_count: Number of retries on failure
            is_agent: Whether this is an agent/LLM node
        """
        func_name = func.__name__ if func else ""
        super().__init__(
            node_id=node_id,
            func=func,
            func_name=func_name,
            description=description,
            timeout=timeout,
            retry_count=retry_count,
            is_agent=is_agent,
            **kwargs
        )
    
    async def execute(self, state: StateDict) -> Dict[str, Any]:
        """
        Execute the node function on the given state.
        
        Args:
            state: Current workflow state
            
        Returns:
            State updates from execution
        """
        if not self.func:
            return {}
        
        try:
            result = self.func(state)
            if result is None:
                return {}
            return result if isinstance(result, dict) else {"result": result}
        except Exception as e:
            raise RuntimeError(f"Node {self.node_id} execution failed: {str(e)}")
    
    def __call__(self, state: StateDict) -> Dict[str, Any]:
        """
        Convenience method to execute node synchronously.
        
        Args:
            state: Current workflow state
            
        Returns:
            State updates from execution
        """
        if not self.func:
            return {}
        result = self.func(state)
        if result is None:
            return {}
        return result if isinstance(result, dict) else {"result": result}
