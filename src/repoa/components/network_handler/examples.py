"""Network handler examples - Workflow patterns similar to LangGraph."""

from repoa.components.network_handler import (
    WorkflowNetwork,
    START,
    END,
)


def example_1_simple_workflow():
    """Example 1: Simple linear workflow."""
    print("=== Example 1: Simple Linear Workflow ===\n")
    
    # Define node functions
    def process_input(state):
        """First step: process input."""
        text = state.get("input", "")
        return {"processed": text.upper()}
    
    def add_prefix(state):
        """Second step: add prefix."""
        processed = state.get("processed", "")
        return {"result": f"PREFIX: {processed}"}
    
    # Build network
    network = WorkflowNetwork(graph_id="simple_workflow")
    network.add_node("process", process_input, description="Process input text")
    network.add_node("prefix", add_prefix, description="Add prefix to text")
    
    # Connect nodes
    network.add_edge(START, "process")
    network.add_edge("process", "prefix")
    network.add_edge("prefix", END)
    
    # Execute
    compiled = network.compile()
    result = compiled.invoke({"input": "hello world"})
    
    print(f"Input: hello world")
    print(f"Result: {result}\n")


def example_2_conditional_routing():
    """Example 2: Conditional routing based on state."""
    print("=== Example 2: Conditional Routing ===\n")
    
    def check_length(state):
        """Check input length and decide routing."""
        text = state.get("input", "")
        state["length"] = len(text)
        return {"length": len(text)}
    
    def handle_short(state):
        """Handle short input (< 5 chars)."""
        return {"output": f"Short: {state.get('input')}"}
    
    def handle_long(state):
        """Handle long input (>= 5 chars)."""
        text = state.get("input", "")
        return {"output": f"Long: {text.upper()}"}
    
    # Build network
    network = WorkflowNetwork(graph_id="conditional_workflow")
    network.add_node("check", check_length)
    network.add_node("short_handler", handle_short)
    network.add_node("long_handler", handle_long)
    
    # Conditional routing
    def route_by_length(state):
        return "short" if state.get("length", 0) < 5 else "long"
    
    network.add_edge(START, "check")
    network.add_conditional_edge(
        "check",
        route_by_length,
        {"short": "short_handler", "long": "long_handler", "default": END}
    )
    network.add_edge("short_handler", END)
    network.add_edge("long_handler", END)
    
    # Execute
    compiled = network.compile()
    
    # Test with short input
    result1 = compiled.invoke({"input": "hi"})
    print(f"Short input result: {result1}\n")
    
    # Test with long input
    result2 = compiled.invoke({"input": "hello world"})
    print(f"Long input result: {result2}\n")


def example_3_streaming():
    """Example 3: Stream execution output."""
    print("=== Example 3: Streaming Execution ===\n")
    
    def worker_1(state):
        return {"step1_done": True, "count": state.get("count", 0) + 1}
    
    def worker_2(state):
        return {"step2_done": True, "count": state.get("count", 0) + 1}
    
    def worker_3(state):
        return {"final": state.get("count", 0) * 10}
    
    # Build network
    network = WorkflowNetwork(graph_id="streaming_workflow")
    network.add_node("work1", worker_1)
    network.add_node("work2", worker_2)
    network.add_node("work3", worker_3)
    
    network.add_edge(START, "work1")
    network.add_edge("work1", "work2")
    network.add_edge("work2", "work3")
    network.add_edge("work3", END)
    
    # Stream execution
    compiled = network.compile()
    
    print("Streaming execution:")
    for node_id, update in compiled.stream({"count": 0}):
        print(f"  Node: {node_id}, Update: {update}")
    
    print()


def example_4_agent_loop():
    """Example 4: Agent-like loop with decision making."""
    print("=== Example 4: Agent Loop Pattern ===\n")
    
    MAX_STEPS = 3
    
    def plan_action(state):
        """Agent plans next action."""
        messages = state.get("messages", [])
        step = state.get("step", 0)
        
        if step < MAX_STEPS:
            action = f"action_{step}"
            return {
                "current_action": action,
                "step": step + 1,
                "messages": messages + [f"Planning {action}"]
            }
        return {"finished": True, "step": step}
    
    def execute_action(state):
        """Execute the planned action."""
        action = state.get("current_action", "")
        messages = state.get("messages", [])
        return {
            "messages": messages + [f"Executed {action}"],
            "action_result": f"result_of_{action}"
        }
    
    def should_continue(state):
        """Decide if loop should continue."""
        step = state.get("step", 0)
        return "execute" if step < MAX_STEPS else "end"
    
    # Build network
    network = WorkflowNetwork(graph_id="agent_loop")
    network.add_node("plan", plan_action, description="Plan next action")
    network.add_node("execute", execute_action, description="Execute action")
    
    network.add_edge(START, "plan")
    network.add_conditional_edge(
        "plan",
        should_continue,
        {"execute": "execute", "end": END}
    )
    network.add_edge("execute", "plan")  # Loop back
    
    # Execute
    compiled = network.compile()
    result = compiled.invoke({"messages": [], "step": 0})
    
    print(f"Final state: {result}\n")


def example_5_with_streaming():
    """Example 5: Network with streaming output."""
    print("=== Example 5: Full Streaming Workflow ===\n")
    
    def fetch_data(state):
        return {
            "data": [1, 2, 3, 4, 5],
            "fetched": True
        }
    
    def process_data(state):
        data = state.get("data", [])
        return {
            "processed_data": [x * 2 for x in data],
            "processed": True
        }
    
    def aggregate(state):
        processed = state.get("processed_data", [])
        return {
            "total": sum(processed),
            "count": len(processed)
        }
    
    # Build network
    network = WorkflowNetwork(graph_id="full_streaming")
    network.add_node("fetch", fetch_data)
    network.add_node("process", process_data)
    network.add_node("aggregate", aggregate)
    
    network.add_edge(START, "fetch")
    network.add_edge("fetch", "process")
    network.add_edge("process", "aggregate")
    network.add_edge("aggregate", END)
    
    # Stream execution
    compiled = network.compile()
    
    print("Streaming output:")
    for node_id, updates in compiled.stream({}):
        if node_id in [START, END]:
            print(f"  {node_id.upper()}")
        else:
            print(f"  {node_id}: {updates}")
    
    print()


if __name__ == "__main__":
    example_1_simple_workflow()
    example_2_conditional_routing()
    example_3_streaming()
    example_4_agent_loop()
    example_5_with_streaming()
    
    print("=== All examples completed ===")
