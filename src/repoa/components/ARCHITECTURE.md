# REPOA Components Framework - Structure & Architecture

Created: February 20, 2026

## Overview
REPOA Components is a Langchain-like framework built with Pydantic models, inspired by OpenRouter SDK architecture but with original code logic and naming conventions.

---

## Directory Structure

```
/src/repoa/components/
├── __init__.py
├── message_handler/          # Message types and handlers
│   ├── __init__.py
│   ├── base_types.py         # BaseMessage, ContentBlock
│   ├── text_message.py       # TextMessage
│   ├── user_message.py       # UserMessage with multimodal support
│   ├── assistant_message.py  # AssistantMessage from LLM
│   ├── system_message.py     # SystemMessage for instructions
│   ├── tool_message.py       # ToolMessage for tool responses
│   └── message.py            # Discriminated union of all message types
│
├── response_handler/         # Response types and tracking
│   ├── __init__.py
│   ├── token_usage.py        # TokenUsage tracking
│   ├── chat_response.py      # Complete ChatResponse
│   └── stream_response.py    # StreamResponse chunks
│
├── tool_handler/             # Tool/function calling
│   ├── __init__.py
│   ├── tool_definition.py    # ToolDefinition with schema
│   ├── tool_invocation.py    # ToolInvocation requests
│   └── tool_choice.py        # ToolChoice behavior config
│
└── model_handler/            # Model and provider management
    ├── __init__.py
    ├── model_spec.py         # ModelSpec definition
    ├── model_pricing.py      # ModelPricing info
    └── provider_info.py      # ProviderInfo & ProviderPreferences
```

---

## Core Components

### 1. Message Handler (`message_handler/`)

**Purpose:** Type-safe message handling with support for multiple message roles.

#### Key Classes:

| Class | Purpose | Key Fields |
|-------|---------|-----------|
| `BaseMessage` | Base for all message types | `content`, `metadata`, `msg_id` |
| `TextMessage` | Simple text content | `content` |
| `UserMessage` | User input (multimodal) | `payload`, `sender`, `session_id` |
| `AssistantMessage` | Model response | `response`, `tool_invocations`, `stop_reason` |
| `SystemMessage` | System instructions | `instructions`, `priority` |
| `ToolMessage` | Tool response | `tool_call_id`, `execution_result` |
| `Message` | Discriminated union | Auto-detects message type |

**Usage Pattern:**
```python
from repoa.components import UserMessage, AssistantMessage, Message

# Create messages
user_msg = UserMessage(payload="What is AI?")
assistant_msg = AssistantMessage(response="AI is...")

# Union type handles polymorphism
messages: List[Message] = [user_msg, assistant_msg]
```

---

### 2. Response Handler (`response_handler/`)

**Purpose:** Track and structure LLM responses with token usage.

#### Key Classes:

| Class | Purpose | Key Fields |
|-------|---------|-----------|
| `TokenUsage` | Token counting | `prompt_tokens`, `completion_tokens`, `total_tokens` |
| `ChatResponseChoice` | Single completion | `index`, `generated_text`, `finish_reason` |
| `ChatResponse` | Complete response | `response_id`, `choices`, `usage`, `deployed_model` |
| `StreamingChoice` | Streaming chunk part | `index`, `delta`, `finish_reason` |
| `StreamResponse` | Streaming chunk | `chunk_id`, `choices`, `usage` |

**Usage Pattern:**
```python
from repoa.components import ChatResponse, TokenUsage

usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
response = ChatResponse(
    response_id="resp_123",
    deployed_model="gpt-4",
    generated_at=1708352400.0,
    usage=usage
)
```

---

### 3. Tool Handler (`tool_handler/`)

**Purpose:** Define and manage tool/function calling.

#### Key Classes:

| Class | Purpose | Key Fields |
|-------|---------|-----------|
| `ToolDefinitionFunction` | Function spec | `name`, `description`, `parameters` |
| `ToolDefinition` | Complete tool def | `type`, `function` |
| `ToolInvocation` | Call request | `invocation_id`, `tool_name`, `arguments` |
| `ToolInvocationStatus` | Call status | `status`, `result`, `error_msg` |
| `ToolChoice` | Choice behavior | `mode` (auto/required/none), `preferred_tool` |

**Usage Pattern:**
```python
from repoa.components import ToolDefinition, ToolInvocation, ToolDefinitionFunction

# Define a tool
tool_func = ToolDefinitionFunction(
    name="calculate",
    description="Perform calculation",
    parameters={"type": "object", "properties": {...}}
)
tool = ToolDefinition(function=tool_func)

# Invoke it
invocation = ToolInvocation(
    invocation_id="call_1",
    tool_name="calculate",
    arguments={"expr": "2+2"},
    call_timestamp=1708352400.0
)
```

---

### 4. Model Handler (`model_handler/`)

**Purpose:** Model and provider configuration/metadata.

#### Key Classes:

| Class | Purpose | Key Fields |
|-------|---------|-----------|
| `ModelPricing` | Pricing info | `prompt_cost`, `completion_cost`, `image_cost` |
| `ModelSpec` | Model definition | `model_id`, `model_slug`, `context_window`, `pricing` |
| `ProviderInfo` | Provider metadata | `provider_id`, `is_available`, `latency_ms` |
| `ProviderPreferences` | Selection config | `enable_fallback`, `preferred_providers`, `max_price` |

**Usage Pattern:**
```python
from repoa.components import ModelSpec, ModelPricing, ProviderPreferences

# Define model pricing
pricing = ModelPricing(
    prompt_cost="0.03",
    completion_cost="0.06"
)

# Define model
model = ModelSpec(
    model_id="gpt4_v1",
    model_name="GPT-4",
    model_slug="gpt-4",
    pricing=pricing,
    creation_date=1708352400.0,
    context_window=8192
)

# Set provider preferences
prefs = ProviderPreferences(
    enable_fallback=True,
    preferred_providers=["openai", "anthropic"],
    sort_by="latency"
)
```

---

## Key Design Patterns

### 1. Pydantic Models with TypedDict
Every model has both:
- **Pydantic `BaseModel`** - For runtime validation & serialization
- **`TypedDict`** - For static type checking

```python
class MessageTypedDict(TypedDict):
    content: str
    role: str

class Message(BaseModel):
    content: str
    role: str
```

### 2. Discriminated Unions
`message.py` uses discriminated unions for polymorphic message handling:
```python
Message = Annotated[
    Union[
        Annotated[SystemMessage, Tag("system")],
        Annotated[UserMessage, Tag("user")],
        ...
    ],
    Discriminator(lambda m: get_message_type(m))
]
```

### 3. Flexible Content Support
- **Text**: Simple strings
- **Multimodal**: List of content items (text, image, audio, video placeholders)
- **Structured**: Dict-based parameters

### 4. Extensible Validation
Uses `pydantic.functional_validators` for custom validation logic.

---

## Integration with LLM Framework

### Flow Example:

```python
from repoa.components import (
    UserMessage, AssistantMessage, ChatResponse, 
    ToolDefinition, TokenUsage, Message
)

# 1. Prepare input
user_msg: Message = UserMessage(payload="What's the weather?")

# 2. Call LLM (pseudo-code)
# response = llm_client.chat([user_msg], tools=[weather_tool])

# 3. Structure response
usage = TokenUsage(prompt_tokens=50, completion_tokens=30)
response = ChatResponse(
    response_id="resp_1",
    deployed_model="gpt-4",
    generated_at=time.time(),
    usage=usage,
    choices=[ChatResponseChoice(index=0, generated_text="...")]
)

# 4. Handle tool calls if any
# if response.tool_invocations:
#     for tool_call in response.tool_invocations:
#         result = execute_tool(tool_call)
#         tool_response = ToolMessage(...)

# 5. Continue conversation
messages: List[Message] = [user_msg, response, ...]
```

---

## Comparison with OpenRouter SDK

| Aspect | OpenRouter SDK | REPOA Components |
|--------|---|---|
| **Code Origin** | Auto-generated by Speakeasy | Manually written |
| **Variable Names** | `ChatResponse`, `UserMessage` | `ChatResponse`, `UserMessage` (fresh logic) |
| **File Names** | Matches OpenRouter API schema | Same structure, different implementation |
| **Pydantic Usage** | ✅ Heavy use of BaseModel | ✅ Heavy use of BaseModel |
| **Multimodal Support** | ✅ Text, image, audio, video | ✅ Designed for extensibility |
| **Tool Calling** | ✅ `ToolDefinition`, `ToolCall` | ✅ `ToolDefinition`, `ToolInvocation` |
| **Streaming** | ✅ `ChatStreamingResponseChunk` | ✅ `StreamResponse` |
| **Provider Routing** | ✅ Complex routing config | ✅ Simplified `ProviderPreferences` |

---

## Next Steps

To expand REPOA Components, consider adding:

1. **Error Handling** (`error_handler/`)
   - HTTP error types (BadRequest, Unauthorized, etc.)
   - Error recovery strategies

2. **Reasoning Support** (`reasoning_handler/`)
   - Reasoning token configuration
   - Reasoning output types

3. **Advanced Features** (`advanced_handler/`)
   - Web search integration
   - File parsing options
   - Vision/image generation

4. **Client Layer** (`client/`)
   - HTTP client implementation
   - Request/response serialization
   - Provider routing logic

5. **Tests** (`tests/`)
   - Unit tests for each component
   - Integration tests
   - Validation tests

---

## Development Notes

- **Date Created:** February 20, 2026
- **Framework Base:** Inspired by OpenRouter Python SDK
- **Type System:** Pydantic v2.x with TypedDict
- **Python Version:** 3.8+
- **Status:** Core components complete, ready for client layer integration
