"""Edge definitions for workflow routing."""

from __future__ import annotations
from typing import Callable, Dict, Any, Optional, Union, List
from pydantic import BaseModel, Field
from .network_state import StateDict


# Type for edge conditions
EdgeCondition = Callable[[StateDict], str]
"""Callable that takes state and returns next node ID."""


class Edge(BaseModel):
    """
    Represents a connection between two nodes in the workflow.
    
    Edges can be:
    - Simple: Always route to the same next node
    - Conditional: Route based on state values
    """
    
    source_node: str = Field(..., description="ID of source node")
    target_node: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[EdgeCondition] = None
    condition_name: str = Field(default="", description="Name of condition function")
    is_conditional: bool = Field(default=False, description="Whether this edge is conditional")
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def __init__(
        self,
        source_node: str,
        target_node: Optional[str] = None,
        description: Optional[str] = None,
        condition: Optional[EdgeCondition] = None,
        **kwargs
    ):
        """
        Initialize an edge.
        
        Args:
            source_node: ID of node this edge comes from
            target_node: ID of node to route to (for unconditional edges)
            description: Human-readable description
            condition: Function for conditional routing
        """
        condition_name = condition.__name__ if condition else ""
        is_conditional = condition is not None
        
        super().__init__(
            source_node=source_node,
            target_node=target_node,
            description=description,
            condition=condition,
            condition_name=condition_name,
            is_conditional=is_conditional,
            **kwargs
        )
    
    def route(self, state: StateDict) -> str:
        """
        Determine next node based on this edge.
        
        Args:
            state: Current workflow state
            
        Returns:
            ID of the next node to execute
        """
        if self.condition:
            return self.condition(state)
        elif self.target_node:
            return self.target_node
        else:
            raise RuntimeError(f"Edge from {self.source_node} has no routing target")


class ConditionalEdge(Edge):
    """
    Edge with multiple possible destinations based on state.
    Routes to one of several target nodes based on a condition function.
    """
    
    target_nodes: List[str] = Field(default_factory=list, description="Possible target nodes")
    
    def __init__(
        self,
        source_node: str,
        target_nodes: List[str],
        condition: EdgeCondition,
        description: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize a conditional edge.
        
        Args:
            source_node: ID of node this edge comes from
            target_nodes: List of possible destination node IDs
            condition: Function that returns which target to use
            description: Human-readable description
        """
        super().__init__(
            source_node=source_node,
            target_node=None,
            condition=condition,
            description=description,
            **kwargs
        )
        self.target_nodes = target_nodes


class EdgeSet(BaseModel):
    """Collection of edges in the network."""
    
    edges: List[Edge] = Field(default_factory=list)
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the set."""
        self.edges.append(edge)
    
    def get_edges_from(self, source_node: str) -> List[Edge]:
        """Get all edges originating from a node."""
        return [e for e in self.edges if e.source_node == source_node]
    
    def get_next_node(self, source_node: str, state: StateDict) -> Optional[str]:
        """
        Get next node for a given source node and state.
        
        Args:
            source_node: Current node ID
            state: Current workflow state
            
        Returns:
            Next node ID or None if no edge found
        """
        edges = self.get_edges_from(source_node)
        
        if not edges:
            return None
        
        # Conditional edges first
        for edge in edges:
            if edge.is_conditional:
                return edge.route(state)
        
        # Simple edges second
        for edge in edges:
            if not edge.is_conditional and edge.target_node:
                return edge.target_node
        
        return None
