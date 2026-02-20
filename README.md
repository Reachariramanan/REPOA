# REPOA Components Framework

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-pydantic-blue)]()

REPOA is a comprehensive, production-ready LLM application framework designed for building sophisticated AI systems with robust message handling, tool orchestration, and workflow management. Built with full type safety using Pydantic v2 and TypedDict, REPOA provides low-level infrastructure for long-running, stateful agent workflows.

## Get Started

### Installation

Install REPOA from the source:

```bash
git clone https://github.com/Reachariramanan/REPOA.git
cd REPOA
export PYTHONPATH="$PWD/src:$PYTHONPATH"
```

### Quick Example

Create your first workflow in minutes:

```python
from repoa.components import WorkflowNetwork, START, END

# Define a simple network
network = WorkflowNetwork()

# Add processing nodes
network.add_node("transform", lambda state: {
    "result": state["input"].upper()
})

# Connect nodes
network.add_edge(START, "transform")
network.add_edge("transform", END)

# Compile and execute
compiled = network.compile()
result = compiled.invoke({"input": "hello world"})

print(result)
# Output: {'input': 'hello world', 'result': 'HELLO WORLD'}
```

For more examples, see [QUICK_REFERENCE.md](src/repoa/components/network_handler/QUICK_REFERENCE.md).

## Core Components

REPOA is organized into five specialized handlers, each addressing distinct aspects of LLM application development:

### Message Handler

Type-safe message abstraction supporting multiple communication patterns.

**Key Classes:**
- `BaseMessage` - Abstract message foundation with metadata
- `UserMessage` - Messages from users or human actors
- `AssistantMessage` - Responses from LLM assistants
- `SystemMessage` - System-level instructions and context
- `ToolMessage` - Results from tool/function execution
- `TextMessage` - Pure text content without role semantics

**Benefits:**
- Discriminated unions with automatic type detection
- Multimodal content support (text, images, etc.)
- Metadata tracking (timestamps, token counts, custom fields)
- Full Pydantic validation and serialization

### Response Handler

Structured response management with comprehensive token tracking.

**Key Classes:**
- `TokenUsage` - Aggregate token counting across modalities
- `ChatResponse` - Complete response with multiple output choices
- `StreamResponse` - Streaming response wrapper for real-time output

**Benefits:**
- Automatic token aggregation
- Cost calculation per response
- Support for streaming and batch responses
- State serialization and deserialization

### Tool Handler

Function definition and invocation framework for tool calling.

**Key Classes:**
- `ToolDefinition` - Function schema with parameters and description
- `ToolInvocation` - Individual tool call with arguments
- `ToolChoice` - Tool selection behavior configuration

**Benefits:**
- JSON schema parameter definition
- Execution status tracking (pending, executing, completed, failed)
- Return value and error handling
- Tool choice policy configuration

### Model Handler

Model specification and provider management for LLM selection.

**Key Classes:**
- `ModelSpec` - Model metadata including pricing and context windows
- `ModelPricing` - Per-token costs across modalities
- `ProviderInfo` - Provider performance metrics
- `ProviderPreferences` - Model selection and fallback strategies

**Benefits:**
- Cost tracking and optimization
- Provider performance metrics
- Fallback and filtering strategies
- Multi-provider model selection

### Network Handler

Workflow orchestration using graph-based execution patterns.

**Key Classes:**
- `WorkflowNetwork` - Builder interface for constructing workflows
- `CompiledWorkflow` - Executable workflow instance
- `Node` - Processing unit with execution logic
- `Edge` - Routing connections (simple and conditional)
- `NetworkState` - Immutable state container
- `ExecutionEngine` - Pregel-inspired execution model

**Benefits:**
- Graph-based workflow composition
- Conditional routing and branching
- Streaming execution support
- State management with history tracking
- Iteration bounds and safety limits

## Core Benefits

### Type Safety

Every component in REPOA provides complete type annotations. Pydantic v2 models ensure runtime validation while TypedDict pairs enable static type analysis and IDE support.

```python
from repoa.components import UserMessage, ChatResponse

# Full type checking at development time
message: UserMessage = UserMessage(content="Query")
response: ChatResponse = ChatResponse(content="Answer")
```

### Modular Architecture

Components are independently usable but compose seamlessly. Import only what you need without unnecessary dependencies.

```python
from repoa.components import (
    UserMessage,           # Just messages
    WorkflowNetwork,       # Just orchestration
    ToolDefinition,        # Just tools
)
```

### Production Ready

Built on battle-tested patterns from LangGraph and Pregel, with proper error handling, iteration bounds, and state management.

```python
# Bounded iterations prevent infinite loops
compiled = network.compile()  # MAX_ITERATIONS = 100 (configurable)

# Streaming for real-time response
for node_id, updates in compiled.stream({"input": "data"}):
    print(f"{node_id}: {updates}")
```

### Comprehensive Documentation

Each component includes detailed architecture guides, API references, and working examples.

- [ARCHITECTURE.md](src/repoa/components/ARCHITECTURE.md) - Component overview
- [NETWORK_ARCHITECTURE.md](src/repoa/components/network_handler/NETWORK_ARCHITECTURE.md) - Orchestration deep dive
- [QUICK_REFERENCE.md](src/repoa/components/network_handler/QUICK_REFERENCE.md) - API and examples
- [examples.py](src/repoa/components/network_handler/examples.py) - Runnable code patterns

## Common Patterns

### Multi-Step Workflows

Chain processing steps with clear data flow:

```python
from repoa.components import WorkflowNetwork, START, END

network = WorkflowNetwork()
network.add_node("validate", validate_fn)
network.add_node("process", process_fn)
network.add_node("format", format_fn)

network.add_edge(START, "validate")
network.add_edge("validate", "process")
network.add_edge("process", "format")
network.add_edge("format", END)
```

### Conditional Routing

Make decisions based on state:

```python
def route_decision(state):
    if state.get("complexity") > 5:
        return "advanced_process"
    return "simple_process"

network.add_conditional_edge("router", route_decision)
network.add_edge("advanced_process", END)
network.add_edge("simple_process", END)
```

### Tool-Calling Agents

Execute external functions with controlled interfaces:

```python
from repoa.components import ToolDefinition, ToolInvocation

tool = ToolDefinition(
    name="calculate",
    description="Perform calculations",
    function={"parameters": {...}}
)

call = ToolInvocation(
    tool_name="calculate",
    arguments={"operation": "add", "a": 2, "b": 3}
)
```

## Project Structure

```
REPOA/
├── src/repoa/components/
│   ├── __init__.py                     # Main exports
│   ├── message_handler/                # Message types (8 files)
│   ├── response_handler/               # Response management (4 files)
│   ├── tool_handler/                   # Tool definition (4 files)
│   ├── model_handler/                  # Model configuration (4 files)
│   ├── network_handler/                # Workflow orchestration (11 files)
│   └── documentation files             # Comprehensive guides
├── PROJECT_STATUS.md                   # Project status and statistics
├── verify_structure.sh                 # Structure verification script
└── README.md                           # This file
```

## Statistics

- **Total Files:** 40
- **Lines of Code:** 6,000+
- **Lines of Documentation:** 10,000+
- **Pydantic Models:** 25+
- **Type Coverage:** 100%
- **Components:** 5 specialized handlers

## Design Philosophy

REPOA is built on proven architectural principles:

1. **Separation of Concerns** - Each handler manages a specific domain (messages, responses, tools, models, orchestration)
2. **Type Safety First** - Pydantic v2 models with dual TypedDict definitions for runtime validation and static analysis
3. **Modularity** - Use individual components independently or compose them for complete workflows
4. **Production Ready** - Based on research (Pregel) and proven frameworks (LangGraph)
5. **Documentation** - Comprehensive guides, examples, and API references included

## Additional Resources

### Documentation

- [Project Status](PROJECT_STATUS.md) - Framework overview and statistics
- [Component Architecture](src/repoa/components/ARCHITECTURE.md) - Detailed component guide
- [Network Architecture](src/repoa/components/network_handler/NETWORK_ARCHITECTURE.md) - Orchestration system
- [Import Guide](src/repoa/components/IMPORT_GUIDE.md) - How to import components
- [Quick Reference](src/repoa/components/network_handler/QUICK_REFERENCE.md) - API and code examples

### Code Examples

- [Network Handler Examples](src/repoa/components/network_handler/examples.py) - Five complete workflow patterns
- [Components Examples](src/repoa/components/examples.py) - Integration examples

### Comparison

- [vs OpenRouter SDK](src/repoa/components/COMPARISON.md) - How REPOA relates to existing frameworks

## Use Cases

REPOA is well-suited for:

- Building LLM-powered agents with multi-step reasoning
- Implementing tool-calling workflows
- Creating stateful, long-running AI systems
- Orchestrating complex AI pipelines
- Multi-model systems with provider selection
- Cost-optimized LLM applications

## Compatibility

- **Python:** 3.8+
- **Dependencies:** Pydantic v2.x
- **Type Support:** Full type hints, mypy compatible
- **Serialization:** JSON-serializable Pydantic models

## Framework Inspiration

REPOA's design draws inspiration from:

- **Pregel** - Google's distributed computation model for graph processing
- **LangGraph** - LangChain's graph orchestration framework
- **NetworkX** - Graph data structure and algorithms library

## Contributing

This is an open-source framework. Contributions, issues, and feedback are welcome.

## License

MIT License - see LICENSE file for details.

## Acknowledgements

REPOA is inspired by the Pregel distributed computation model and LangGraph's approach to agent orchestration. The framework is designed to be modular, allowing usage as a standalone component library or as a complete system for building sophisticated LLM applications.

---

For detailed implementation information and API documentation, see [NETWORK_ARCHITECTURE.md](src/repoa/components/network_handler/NETWORK_ARCHITECTURE.md) and [QUICK_REFERENCE.md](src/repoa/components/network_handler/QUICK_REFERENCE.md).
