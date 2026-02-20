# Network Handler Quick Reference

## Installation & Import

```python
from repoa.components.network_handler import (
    WorkflowNetwork,
    CompiledWorkflow,
    Node,
    Edge,
    NetworkState,
    ExecutionEngine,
    START,
    END,
)
```

---

## Quick Start

### 1. Simple Workflow

```python
# Define node functions
def step_1(state):
    return {"result": state["input"].upper()}

def step_2(state):
    return {"final": f"Processed: {state['result']}"}

# Build network
network = WorkflowNetwork(graph_id="simple")
network.add_node("uppercase", step_1)
network.add_node("format", step_2)

network.add_edge(START, "uppercase")
network.add_edge("uppercase", "format")
network.add_edge("format", END)

# Execute
compiled = network.compile()
result = compiled.invoke({"input": "hello"})
print(result)  # {'input': 'hello', 'result': 'HELLO', 'final': 'Processed: HELLO'}
```

### 2. Conditional Routing

```python
def check_type(state):
    return {"type": "number" if state["input"].isdigit() else "text"}

def handle_number(state):
    return {"output": int(state["input"]) * 2}

def handle_text(state):
    return {"output": state["input"].upper()}

network = WorkflowNetwork()
network.add_node("check", check_type)
network.add_node("num_handler", handle_number)
network.add_node("text_handler", handle_text)

network.add_edge(START, "check")
network.add_conditional_edge(
    "check",
    lambda s: "number" if s["type"] == "number" else "text",
    {"number": "num_handler", "text": "text_handler"}
)
network.add_edge("num_handler", END)
network.add_edge("text_handler", END)

compiled = network.compile()
print(compiled.invoke({"input": "42"}))    # {'input': '42', 'type': 'number', 'output': 84}
print(compiled.invoke({"input": "hello"})) # {'input': 'hello', 'type': 'text', 'output': 'HELLO'}
```

### 3. Agent Loop Pattern

```python
MAX_ITERATIONS = 3

def agent_think(state):
    iteration = state.get("iteration", 0)
    if iteration < MAX_ITERATIONS:
        plan = f"step_{iteration}"
        return {
            "iteration": iteration + 1,
            "plan": plan,
            "history": state.get("history", []) + [plan]
        }
    return {"done": True}

def execute(state):
    plan = state.get("plan", "")
    return {
        "result": f"Executed {plan}",
        "history": state.get("history", []) + [f"executed_{plan}"]
    }

network = WorkflowNetwork()
network.add_node("think", agent_think)
network.add_node("do", execute)

network.add_edge(START, "think")
network.add_conditional_edge(
    "think",
    lambda s: "do" if not s.get("done") else "end",
    {"do": "do", "end": END}
)
network.add_edge("do", "think")  # Loop back

compiled = network.compile()
result = compiled.invoke({})
print(result)
# {
#     'iteration': 3,
#     'plan': 'step_2',
#     'history': ['step_0', 'executed_step_0', 'step_1', 'executed_step_1', 'step_2', 'executed_step_2'],
#     'done': True,
#     'result': 'Executed step_2'
# }
```

### 4. Streaming Execution

```python
network = WorkflowNetwork()
# ... add nodes ...
compiled = network.compile()

print("Execution stream:")
for node_id, updates in compiled.stream({"input": "data"}):
    print(f"  {node_id:15} → {updates}")
```

---

## Node Functions

```python
# Node function signature
def my_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Args:
        state: Current workflow state
        
    Returns:
        Dictionary of updates to merge into state
    """
    # Process state
    value = state.get("key")
    
    # Return updates
    return {"result": processed_value}
```

---

## Network Building API

### add_node()

```python
network.add_node(
    node_id="my_node",
    func=my_function,
    description="Optional description",
    timeout=30.0,  # Optional timeout
    retry_count=2  # Optional retries
)
```

### add_edge()

```python
# Simple edge
network.add_edge("node1", "node2")

# From START
network.add_edge(START, "first_node")

# To END
network.add_edge("last_node", END)
```

### add_conditional_edge()

```python
network.add_conditional_edge(
    source="decision_node",
    condition=lambda state: "option_a" if state["flag"] else "option_b",
    target_map={
        "option_a": "handler_a",
        "option_b": "handler_b",
        "default": END
    }
)
```

---

## Execution Methods

### invoke() - Synchronous

```python
network = WorkflowNetwork()
# ... build network ...
compiled = network.compile()

# Run to completion
final_state = compiled.invoke(
    initial_state={"input": "data"},
    max_iterations=100
)
```

### stream() - Streaming

```python
# Stream node outputs as they execute
for node_id, state_update in compiled.stream({"input": "data"}):
    if node_id not in ["__start__", "__end__"]:
        print(f"{node_id}: {state_update}")
```

---

## State Management

```python
# State is a dictionary
state = {
    "input": "raw_input",
    "processed": True,
    "result": None
}

# Node updates merge into state
def my_node(state):
    return {"result": state["input"] + "_processed"}

# After execution, state has all updates
# state = {
#     "input": "raw_input",
#     "processed": True,
#     "result": "raw_input_processed"
# }
```

---

## Routing Decisions

```python
# Condition function returns next node ID or target key
def route_by_priority(state):
    if state["priority"] == "high":
        return "fast_track"
    elif state["priority"] == "low":
        return "slow_track"
    else:
        return "default"

# Use in conditional edge
network.add_conditional_edge(
    "classifier",
    route_by_priority,
    {
        "fast_track": "express_handler",
        "slow_track": "normal_handler",
        "default": "queue"
    }
)
```

---

## Common Patterns

### Pattern: Fan-Out / Fan-In

```python
network.add_node("split", split_func)
network.add_node("work_a", work_func_a)
network.add_node("work_b", work_func_b)
network.add_node("merge", merge_func)

network.add_edge(START, "split")
network.add_edge("split", "work_a")
network.add_edge("split", "work_b")
network.add_edge("work_a", "merge")
network.add_edge("work_b", "merge")
network.add_edge("merge", END)
```

### Pattern: Loop with Counter

```python
def should_continue(state):
    return "work" if state["counter"] < 10 else "end"

network.add_edge(START, "init")
network.add_conditional_edge(
    "check",
    should_continue,
    {"work": "work", "end": END}
)
network.add_edge("work", "check")
```

### Pattern: Error Handling

```python
def safe_node(state):
    try:
        result = risky_operation(state)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_error(state):
    if not state.get("success"):
        return {"error_handled": True, "recovery_action": "retry"}
    return {}
```

---

## Execution Result

```python
# invoke() returns final state
result = compiled.invoke({"x": 1})
# result = {"x": 1, "y": 2, "z": 3, ...}

# stream() yields (node_id, updates) tuples
for node_id, updates in compiled.stream({"x": 1}):
    # node_id: str - which node executed
    # updates: dict - what it returned
```

---

## Network Validation

```python
# Automatic validation before compilation
try:
    compiled = network.compile()
except ValueError as e:
    print(f"Network error: {e}")

# Manual validation
if network.validate():
    print("Network is valid")
```

---

## Advanced: Custom Node Objects

```python
from repoa.components.network_handler import Node

# Create node with metadata
node = Node(
    node_id="processor",
    func=my_function,
    description="Processes user input",
    timeout=30.0,
    retry_count=3,
    is_agent=False
)

# Add to network
network.nodes["processor"] = node
```

---

## Debugging

```python
# Inspect network structure
print(network.to_dict())
# {
#     'graph_id': 'my_graph',
#     'entry_node': '__start__',
#     'exit_node': '__end__',
#     'nodes': {...},
#     'edges': [...]
# }

# Stream to see execution flow
for node_id, updates in compiled.stream(state):
    print(f"Executed: {node_id}")
    print(f"Updates: {updates}")
```

---

## Tips & Tricks

### Tip 1: State Inspection

```python
# Add diagnostic node
def debug_node(state):
    print(f"Current state: {state}")
    return {"debug": True}
```

### Tip 2: Conditional Gates

```python
def allow_or_skip(state):
    return "process" if state.get("enabled") else END

network.add_conditional_edge("gate", allow_or_skip, {
    "process": "worker",
    END: END
})
```

### Tip 3: Accumulate Results

```python
def accumulate(state):
    results = state.get("results", [])
    return {"results": results + [state.get("new_result")]}
```

---

## Performance Considerations

- **max_iterations**: Prevent infinite loops (default: 100)
- **Node timeout**: Add to node if long-running
- **State size**: Keep state updates minimal
- **Streaming**: Use for real-time visibility

---

## Common Errors

```python
# Error: Entry point not found
# Solution: Ensure first node exists
network.add_node("first", my_func)
network.add_edge(START, "first")

# Error: Circular infinite loop
# Solution: Use max_iterations or add termination condition
compiled.invoke(state, max_iterations=100)

# Error: Node not found in edges
# Solution: Add all nodes before adding edges
network.add_node("missing", func)
```

---

## See Also

- `network_handler/NETWORK_ARCHITECTURE.md` - Full documentation
- `network_handler/examples.py` - 5 complete examples
- `network_handler/` directory - All source code

---

**Quick Reference Guide v1.0**  
**REPOA Components - Network Handler**
