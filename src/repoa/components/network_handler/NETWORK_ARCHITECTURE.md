# REPOA Network Handler - Workflow Orchestration

## Overview

The Network Handler is a **workflow orchestration framework** inspired by LangGraph but with original architecture and naming conventions. It enables building complex, stateful workflows as directed graphs.

**Naming:** `WorkflowNetwork` 

---

## Architecture

### Core Concepts

1. **WorkflowNetwork** - The main network structure 
2. **Node** - Processing units that execute functions
3. **Edge** - Connections between nodes with optional routing logic
4. **ExecutionEngine** - Runs the network based on Pregel algorithm
5. **NetworkState** - Immutable state flowing through the network

### Workflow Flow

```
         ┌──────────────┐
         │    START     │
         └──────┬───────┘
                │
           ┌────▼────────────┐
           │    Node 1       │
           │ (process_input) │
           └────┬────────────┘
                │
        ┌───────▼────────────┐
        │  Conditional Edge  │
        │  (route by state)  │
        └───┬────────────┬───┘
            │            │
      ┌─────▼──┐   ┌─────▼──┐
      │ Node 2 │   │ Node 3 │
      └────┬───┘   └────┬───┘
         │              │
      ┌─────────────────┘
      │
      └────┬──────────┐
           │   END    │
           └──────────┘
```

---

## Core Classes

### 1. WorkflowNetwork

Main network builder class.

```python
from repoa.components.network_handler import WorkflowNetwork, START, END

# Create network
network = WorkflowNetwork(graph_id="my_workflow")

# Add nodes
network.add_node("step1", my_function, description="First step")
network.add_node("step2", another_function)

# Add edges
network.add_edge(START, "step1")
network.add_edge("step1", "step2")
network.add_edge("step2", END)

# Compile and execute
compiled = network.compile()
result = compiled.invoke({"input": "data"})
```

**Key Methods:**
- `add_node(node_id, func, ...)` - Add processing node
- `add_edge(source, target)` - Add simple edge
- `add_conditional_edge(source, condition, target_map)` - Add routing edge
- `set_entry_point(node_id)` - Change start node
- `set_finish_point(node_id)` - Change end node
- `validate()` - Check network integrity
- `compile()` - Prepare for execution

---

### 2. Node

Represents a processing unit in the workflow.

```python
def my_processor(state):
    """Node function - takes state dict, returns updates."""
    processed = state.get("input", "").upper()
    return {"output": processed}

# Create node
node = Node(
    node_id="processor",
    func=my_processor,
    description="Uppercase processor",
    timeout=30.0,
    retry_count=2
)

# Or add via network
network.add_node("processor", my_processor)
```

**Node Function Signature:**
```python
def node_function(state: Dict[str, Any]) -> Dict[str, Any]:
    # Process state
    # Return updates to merge into state
    return {"key": value}
```

**Key Fields:**
- `node_id` - Unique identifier
- `func` - Callable that processes state
- `description` - Human-readable description
- `timeout` - Execution timeout
- `retry_count` - Retry attempts on failure
- `is_agent` - Whether this runs an agent/LLM

---

### 3. Edge

Connection between nodes with optional routing.

**Simple Edge:**
```python
edge = Edge(
    source_node="process",
    target_node="validate"
)
```

**Conditional Edge:**
```python
def route_by_type(state):
    """Return next node ID based on state."""
    if state.get("type") == "api":
        return "api_handler"
    else:
        return "db_handler"

# Add conditional routing
network.add_conditional_edge(
    "parse",
    route_by_type,
    {"api": "api_handler", "db": "db_handler"}
)
```

---

### 4. ExecutionEngine

Runs the network using Pregel algorithm concepts.

```python
engine = ExecutionEngine(network=my_graph)

# Execute to completion
result = engine.execute(
    initial_state={"input": "data"},
    max_iterations=100
)

# Stream execution
for node_id, state_update in engine.stream({"input": "data"}):
    print(f"{node_id}: {state_update}")
```

**Returns:**
- `ExecutionResult` with:
  - `final_state` - Final workflow state
  - `steps` - List of execution steps
  - `total_duration_ms` - Total execution time
  - `iterations` - Number of nodes executed
  - `error` - Error message if failed

---

### 5. NetworkState

Manages state flowing through the network.

```python
from repoa.components.network_handler import NetworkState

state = NetworkState(
    current_node="node1",
    state_data={"key": "value"},
    history=["__start__", "node1"]
)

# Update state
new_state = state.update({"key": "new_value"})

# Get as dict
state_dict = state.to_dict()
```

---

## Common Patterns

### Pattern 1: Simple Linear Workflow

```python
network = WorkflowNetwork()

network.add_node("fetch", fetch_data)
network.add_node("process", process_data)
network.add_node("save", save_results)

network.add_edge(START, "fetch")
network.add_edge("fetch", "process")
network.add_edge("process", "save")
network.add_edge("save", END)

compiled = network.compile()
result = compiled.invoke({})
```

### Pattern 2: Conditional Branching

```python
network = WorkflowNetwork()

network.add_node("check", check_condition)
network.add_node("path_a", handler_a)
network.add_node("path_b", handler_b)

def route(state):
    return "branch_a" if state.get("flag") else "branch_b"

network.add_edge(START, "check")
network.add_conditional_edge(
    "check",
    route,
    {"branch_a": "path_a", "branch_b": "path_b"}
)
network.add_edge("path_a", END)
network.add_edge("path_b", END)
```

### Pattern 3: Agent Loop

```python
network = WorkflowNetwork()

network.add_node("agent", agent_think)
network.add_node("tool", use_tool)

def should_continue(state):
    return "tool" if state.get("needs_tool") else "end"

network.add_edge(START, "agent")
network.add_conditional_edge("agent", should_continue, {
    "tool": "tool",
    "end": END
})
network.add_edge("tool", "agent")  # Loop back
```

### Pattern 4: Parallel Processing

```python
# Execute multiple branches that converge
network = WorkflowNetwork()

network.add_node("split", split_work)
network.add_node("work_a", process_a)
network.add_node("work_b", process_b)
network.add_node("merge", merge_results)

network.add_edge(START, "split")
network.add_edge("split", "work_a")
network.add_edge("split", "work_b")
network.add_edge("work_a", "merge")
network.add_edge("work_b", "merge")
network.add_edge("merge", END)
```

---

## State Management

### State as Dictionary

States flow as dictionaries through the network:

```python
initial_state = {
    "input": "raw data",
    "user_id": 123,
    "config": {"verbose": True}
}

# Nodes receive and update state
def process(state):
    return {
        "processed": state["input"].upper(),
        "timestamp": datetime.now().isoformat()
    }

# Node updates are merged into state
# Final state includes all updates from all nodes
```

### State Updates

Each node returns a **partial update** which gets merged:

```python
# Initial
state = {"count": 0}

# Node 1
network.add_node("inc1", lambda s: {"count": s["count"] + 1})

# Node 2
network.add_node("inc2", lambda s: {"count": s["count"] + 10})

# State after execution: {"count": 11}
```

---

## Execution Modes

### Invoke (Synchronous)

Execute to completion and get final state:

```python
result = compiled.invoke({"input": "data"})
# Returns: {"input": "data", "output": "...", ...}
```

### Stream (Streaming)

Get updates as each node executes:

```python
for node_id, updates in compiled.stream({"input": "data"}):
    if node_id != "__start__":
        print(f"{node_id} output: {updates}")
```

---

## Comparison with LangGraph

| Feature | LangGraph | REPOA | Notes |
|---------|---|---|---|
| **Class Name** | StateGraph | WorkflowNetwork | Different name, same concept |
| **State** | TypedDict schema | Dict[str, Any] | More flexible |
| **Nodes** | Functions | Node objects | Explicit node management |
| **Edges** | add_edge() | Edge objects | More control |
| **Routing** | Conditional edges | EdgeCondition functions | Same routing concept |
| **Execution** | Pregel-like | ExecutionEngine | Based on Pregel algorithm |
| **Streaming** | ✅ Yes | ✅ Yes | Stream node outputs |
| **Human-in-loop** | ✅ Yes | ⏳ Planned | Pause/resume support |
| **Checkpointing** | ✅ Yes | ⏳ Planned | State persistence |

---

## Inspired By

- **[Google's Pregel](https://research.google/pubs/pub37252/)** - Bulk synchronous parallel computing
- **[Apache Beam](https://beam.apache.org/)** - Distributed pipeline execution  
- **[NetworkX](https://networkx.org/)** - Network APIs and patterns
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Network-based agent orchestration

---

## Files Structure

```
network_handler/
├── __init__.py           # Exports
├── constants.py          # START, END constants
├── network_state.py        # NetworkState class
├── node.py              # Node definition
├── edge.py              # Edge and routing
├── workflow_network.py    # Main WorkflowNetwork
├── execution_engine.py  # Pregel-based execution
├── examples.py          # 5+ working examples
└── NETWORK_ARCHITECTURE.md # This doc
```

---

## Advanced Topics

### Custom Node Metadata

Attach extra info to nodes:

```python
network.add_node(
    "llm_call",
    llm_function,
    description="Call LLM model",
    timeout=60.0,
    retry_count=3,
)
```

### Complex Routing

Chain conditions:

```python
def multi_level_router(state):
    if state.get("requires_approval"):
        return "approval_queue"
    elif state.get("priority") == "high":
        return "fast_track"
    else:
        return "standard"

network.add_conditional_edge(
    "check",
    multi_level_router,
    {
        "approval_queue": "approver",
        "fast_track": "expedited",
        "standard": "normal",
    }
)
```

### Error Handling

Nodes can return error state:

```python
def safe_node(state):
    try:
        return {"result": process(state)}
    except Exception as e:
        return {"error": str(e), "fallback": True}
```

---

## Next Steps

Planned enhancements:
- [ ] Human-in-the-loop interrupts
- [ ] State checkpointing & persistence
- [ ] Error recovery strategies
- [ ] Async/await support
- [ ] Node timeout handling
- [ ] Logging & observability
- [ ] Network visualization
- [ ] Subgraph support

---

## See Also

- `examples.py` - Runnable examples
- `REPOA/components/ARCHITECTURE.md` - Component architecture  
- `REPOA/components/COMPARISON.md` - vs OpenRouter SDK

---

**Version:** 1.0  
**Date:** February 20, 2026  
**Framework:** REPOA Components
