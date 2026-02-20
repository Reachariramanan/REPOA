"""Network state management and schema definitions."""

from __future__ import annotations
from typing import Any, Dict, Optional, TypeVar, Generic, Union
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# Type aliases for state representation
StateDict = Dict[str, Any]
"""Dictionary-based state representation."""

T = TypeVar('T', bound=Union[StateDict, BaseModel])


class NetworkState(BaseModel, Generic[T]):
    """
    Represents the network execution state.
    
    This is the data that flows through the workflow network,
    updated by each node as it executes.
    """
    
    current_node: str = Field(default="", description="Currently executing node ID")
    state_data: T = Field(default_factory=dict, description="Workflow state data")
    history: list[str] = Field(default_factory=list, description="Execution history of node IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def update(self, updates: Dict[str, Any]) -> NetworkState:
        """
        Update state data with new values.
        
        Args:
            updates: Dictionary of updates to apply
            
        Returns:
            Updated NetworkState instance
        """
        if isinstance(self.state_data, dict):
            new_data = {**self.state_data, **updates}
        else:
            # For Pydantic models
            new_data = self.state_data.copy(update=updates)
        
        return NetworkState(
            current_node=self.current_node,
            state_data=new_data,
            history=self.history.copy(),
            metadata=self.metadata.copy()
        )
    
    def record_execution(self, node_id: str) -> None:
        """
        Record node execution in history.
        
        Args:
            node_id: ID of node that executed
        """
        self.current_node = node_id
        self.history.append(node_id)
    
    def to_dict(self) -> StateDict:
        """
        Convert state to dictionary format.
        
        Returns:
            Dictionary representation of state data
        """
        if isinstance(self.state_data, dict):
            return self.state_data.copy()
        elif isinstance(self.state_data, BaseModel):
            return self.state_data.model_dump()
        else:
            return dict(self.state_data)
