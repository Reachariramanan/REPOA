"""Network handler module for REPOA framework - Workflow orchestration."""

from .constants import START, END
from .workflow_network import WorkflowNetwork, CompiledWorkflow
from .node import Node, NodeFunction
from .edge import Edge, EdgeCondition
from .network_state import NetworkState, StateDict
from .execution_engine import ExecutionEngine, ExecutionResult

__all__ = [
    # Constants
    "START",
    "END",
    # Core classes
    "WorkflowNetwork",
    "CompiledWorkflow",
    "Node",
    "NodeFunction",
    "Edge",
    "EdgeCondition",
    "NetworkState",
    "StateDict",
    # Execution
    "ExecutionEngine",
    "ExecutionResult",
]
