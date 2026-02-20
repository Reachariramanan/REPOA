"""Execution engine for workflow Network - Based on Pregel algorithm concept."""

from __future__ import annotations
from typing import Dict, Tuple, Iterator, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from .constants import START, END, MAX_ITERATIONS
from .network_state import StateDict, NetworkState
from .node import Node


@dataclass
class ExecutionStep:
    """Represents a single step in execution."""
    
    node_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    state_before: Optional[StateDict] = None
    state_after: Optional[StateDict] = None
    error: Optional[str] = None
    duration_ms: float = 0.0


@dataclass
class ExecutionResult:
    """Result of complete workflow execution."""
    
    final_state: StateDict
    steps: List[ExecutionStep] = field(default_factory=list)
    total_duration_ms: float = 0.0
    iterations: int = 0
    error: Optional[str] = None
    completed: bool = True


class ExecutionEngine:
    """
    Executes a workflow network.
    
    Based on concepts from Google's Pregel algorithm:
    - Vertex-centric computation
    - Bounded iterations
    - State flow through network
    """
    
    def __init__(self, network):
        """
        Initialize execution engine.
        
        Args:
            network: WorkflowNetwork to execute
        """
        self.network = network
        self.network.validate()
    
    def execute(
        self,
        initial_state: StateDict,
        max_iterations: int = MAX_ITERATIONS,
    ) -> ExecutionResult:
        """
        Execute workflow to completion.
        
        Args:
            initial_state: Starting state
            max_iterations: Max iterations to prevent infinite loops
            
        Returns:
            ExecutionResult with final state and metadata
        """
        import time
        start_time = time.time()
        
        current_state = initial_state.copy()
        steps: List[ExecutionStep] = []
        current_node = self.network.entry_node
        iteration = 0
        
        try:
            while current_node != self.network.exit_node and iteration < max_iterations:
                iteration += 1
                step_start = time.time()
                
                # Execute node if not START
                if current_node == START:
                    # First edge from START
                    next_node = self.network.edges.get_next_node(START, current_state)
                    if next_node:
                        current_node = next_node
                    else:
                        break
                    continue
                
                # Get and execute the node
                if current_node in self.network.nodes:
                    node = self.network.nodes[current_node]
                    
                    step = ExecutionStep(
                        node_id=current_node,
                        state_before=current_state.copy(),
                    )
                    
                    try:
                        # Execute node
                        updates = node(current_state)
                        
                        # Apply updates to state
                        if updates:
                            current_state.update(updates)
                        
                        step.state_after = current_state.copy()
                        step.duration_ms = (time.time() - step_start) * 1000
                        
                    except Exception as e:
                        step.error = str(e)
                        step.duration_ms = (time.time() - step_start) * 1000
                        raise RuntimeError(f"Node {current_node} failed: {str(e)}")
                    
                    steps.append(step)
                
                # Find next node
                next_node = self.network.edges.get_next_node(current_node, current_state)
                if next_node is None:
                    break
                current_node = next_node
            
            total_duration = (time.time() - start_time) * 1000
            
            return ExecutionResult(
                final_state=current_state,
                steps=steps,
                total_duration_ms=total_duration,
                iterations=iteration,
                completed=current_node == self.network.exit_node,
            )
        
        except Exception as e:
            total_duration = (time.time() - start_time) * 1000
            return ExecutionResult(
                final_state=current_state,
                steps=steps,
                total_duration_ms=total_duration,
                iterations=iteration,
                error=str(e),
                completed=False,
            )
    
    def stream(
        self,
        initial_state: StateDict,
        max_iterations: int = MAX_ITERATIONS,
    ) -> Iterator[Tuple[str, StateDict]]:
        """
        Execute workflow and stream node outputs.
        
        Args:
            initial_state: Starting state
            max_iterations: Max iterations to prevent infinite loops
            
        Yields:
            Tuples of (node_id, state_update)
        """
        current_state = initial_state.copy()
        current_node = self.network.entry_node
        iteration = 0
        
        while current_node != self.network.exit_node and iteration < max_iterations:
            iteration += 1
            
            # Handle START node
            if current_node == START:
                next_node = self.network.edges.get_next_node(START, current_state)
                if next_node:
                    current_node = next_node
                    yield START, {"next_node": next_node}
                else:
                    break
                continue
            
            # Execute regular node
            if current_node in self.network.nodes:
                node = self.network.nodes[current_node]
                
                try:
                    updates = node(current_state)
                    if updates:
                        current_state.update(updates)
                        yield current_node, updates
                    else:
                        yield current_node, {}
                        
                except Exception as e:
                    yield current_node, {"error": str(e)}
            
            # Find next node
            next_node = self.network.edges.get_next_node(current_node, current_state)
            if next_node is None:
                break
            current_node = next_node
        
        if current_node == self.network.exit_node:
            yield self.network.exit_node, current_state
