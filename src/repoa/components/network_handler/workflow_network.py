"""Core workflow network implementation - Similar to LangGraph's StateGraph."""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field
from .constants import START, END
from .node import Node, NodeFunction
from .edge import Edge, EdgeSet, EdgeCondition
from .network_state import NetworkState, StateDict
from .execution_engine import ExecutionEngine


class WorkflowNetwork(BaseModel):
    """
    Main network structure for defining workflows.
    
    Similar to LangGraph's StateGraph, but with different naming:
    - WorkflowNetwork vs StateGraph
    - Nodes represent processing units
    - Edges represent routing logic
    - Execute through compiled workflow
    """
    
    graph_id: str = Field(default="workflow", description="Unique network identifier")
    nodes: Dict[str, Node] = Field(default_factory=dict, description="Map of node_id -> Node")
    edges: EdgeSet = Field(default_factory=EdgeSet, description="All edges in network")
    entry_node: str = Field(default=START, description="Starting node ID")
    exit_node: str = Field(default=END, description="Exit node ID")
    description: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def add_node(
        self,
        node_id: str,
        func: NodeFunction,
        description: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Node:
        """
        Add a node to the workflow.
        
        Args:
            node_id: Unique identifier for the node
            func: Function that executes the node logic
            description: Human-readable description
            timeout: Execution timeout in seconds
            
        Returns:
            The created Node
        """
        node = Node(
            node_id=node_id,
            func=func,
            description=description,
            timeout=timeout,
        )
        self.nodes[node_id] = node
        return node
    
    def add_edge(
        self,
        source: str,
        target: str,
        description: Optional[str] = None,
    ) -> Edge:
        """
        Add a simple edge from source to target node.
        
        Args:
            source: Source node ID
            target: Target node ID
            description: Human-readable description
            
        Returns:
            The created Edge
        """
        edge = Edge(
            source_node=source,
            target_node=target,
            description=description,
        )
        self.edges.add_edge(edge)
        return edge
    
    def add_conditional_edge(
        self,
        source: str,
        condition: EdgeCondition,
        target_map: Dict[str, str],
        description: Optional[str] = None,
    ) -> Edge:
        """
        Add a conditional edge that routes based on state.
        
        Args:
            source: Source node ID
            condition: Function that evaluates state and returns target
            target_map: Map from condition results to target node IDs
            description: Human-readable description
            
        Returns:
            The created Edge
        """
        # Wrap condition to use the mapping
        def routed_condition(state: StateDict) -> str:
            result = condition(state)
            return target_map.get(result, target_map.get("default", END))
        
        targets = list(target_map.values())
        edge = Edge(
            source_node=source,
            target_node=None,
            condition=routed_condition,
            description=description,
        )
        self.edges.add_edge(edge)
        return edge
    
    def set_entry_point(self, node_id: str) -> None:
        """
        Set the entry point of the workflow.
        
        Args:
            node_id: ID of node to start from
        """
        self.entry_node = node_id
    
    def set_finish_point(self, node_id: str) -> None:
        """
        Set the finish/exit point of the workflow.
        
        Args:
            node_id: ID of node to end at
        """
        self.exit_node = node_id
    
    def validate(self) -> bool:
        """
        Validate the network structure.
        
        Returns:
            True if network is valid
            
        Raises:
            ValueError if network is invalid
        """
        # Check entry point exists
        if self.entry_node not in [START] + list(self.nodes.keys()):
            raise ValueError(f"Entry point {self.entry_node} not found")
        
        # Check exit point exists
        if self.exit_node not in [END] + list(self.nodes.keys()):
            raise ValueError(f"Exit point {self.exit_node} not found")
        
        # Check all edges reference valid nodes
        for edge in self.edges.edges:
            if edge.source_node not in [START] + list(self.nodes.keys()):
                raise ValueError(f"Edge source {edge.source_node} not found")
            if edge.target_node and edge.target_node not in [END] + list(self.nodes.keys()):
                raise ValueError(f"Edge target {edge.target_node} not found")
        
        return True
    
    def compile(self) -> CompiledWorkflow:
        """
        Compile the workflow network for execution.
        
        Returns:
            CompiledWorkflow ready to execute
            
        Raises:
            ValueError if network is invalid
        """
        self.validate()
        return CompiledWorkflow(network=self)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert network to dictionary representation.
        
        Returns:
            Dictionary representation of network
        """
        return {
            "graph_id": self.graph_id,
            "description": self.description,
            "entry_node": self.entry_node,
            "exit_node": self.exit_node,
            "nodes": {
                node_id: {
                    "id": node.node_id,
                    "func_name": node.func_name,
                    "description": node.description,
                }
                for node_id, node in self.nodes.items()
            },
            "edges": [
                {
                    "source": e.source_node,
                    "target": e.target_node,
                    "conditional": e.is_conditional,
                }
                for e in self.edges.edges
            ]
        }


class CompiledWorkflow(BaseModel):
    """
    Compiled workflow ready for execution.
    
    Similar to LangGraph's compiled network.
    """
    
    network: WorkflowNetwork = Field(..., description="The workflow network")
    engine: Optional[ExecutionEngine] = None
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def __init__(self, network: WorkflowNetwork, **kwargs):
        """
        Initialize compiled workflow.
        
        Args:
            network: The WorkflowNetwork to compile
        """
        super().__init__(network=network, **kwargs)
        self.engine = ExecutionEngine(network=network)
    
    def invoke(
        self,
        initial_state: StateDict,
        max_iterations: int = 100,
    ) -> StateDict:
        """
        Execute the workflow synchronously.
        
        Args:
            initial_state: Starting state dictionary
            max_iterations: Maximum number of node executions
            
        Returns:
            Final state after execution
        """
        if not self.engine:
            raise RuntimeError("ExecutionEngine not initialized")
        
        result = self.engine.execute(
            initial_state=initial_state,
            max_iterations=max_iterations,
        )
        return result.final_state
    
    def stream(
        self,
        initial_state: StateDict,
        max_iterations: int = 100,
    ):
        """
        Execute the workflow and stream results.
        
        Args:
            initial_state: Starting state dictionary
            max_iterations: Maximum number of node executions
            
        Yields:
            Tuples of (node_id, state_update)
        """
        if not self.engine:
            raise RuntimeError("ExecutionEngine not initialized")
        
        for node_id, state_update in self.engine.stream(
            initial_state=initial_state,
            max_iterations=max_iterations,
        ):
            yield node_id, state_update
