# REPOA Components - Import Guide

## Main Package Import
```python
from repoa.components import (
    # Messages
    BaseMessage,
    UserMessage,
    AssistantMessage,
    SystemMessage, 
    ToolMessage,
    TextMessage,
    Message,
    
    # Responses
    ChatResponse,
    ChatResponseChoice,
    StreamResponse,
    StreamingChoice,
    TokenUsage,
    
    # Tools
    ToolDefinition,
    ToolInvocation,
    ToolChoice,
    
    # Models & Providers
    ModelSpec,
    ProviderInfo,
    ProviderPreferences,
    ModelPricing,
)
```

## Module-Level Imports

### Message Handler
```python
from repoa.components.message_handler import (
    BaseMessage,
    TextMessage,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ToolMessage,
    Message,  # Discriminated union
)
```

### Response Handler
```python
from repoa.components.response_handler import (
    TokenUsage,
    ChatResponse,
    ChatResponseChoice,
    StreamResponse,
    StreamingChoice,
)
```

### Tool Handler
```python
from repoa.components.tool_handler import (
    ToolDefinition,
    ToolInvocation,
    ToolInvocationStatus,
    ToolChoice,
)
```

### Model Handler
```python
from repoa.components.model_handler import (
    ModelSpec,
    ProviderInfo,
    ProviderPreferences,
    ModelPricing,
)
```

## Detailed Module Structure

### `message_handler/__init__.py`
Exports:
- `BaseMessage` (from `base_types`)
- `ContentBlock` (from `base_types`)
- `TextMessage` (from `text_message`)
- `UserMessage` (from `user_message`)
- `AssistantMessage` (from `assistant_message`)
- `SystemMessage` (from `system_message`)
- `ToolMessage` (from `tool_message`)
- `Message` (from `message`)

### `response_handler/__init__.py`
Exports:
- `TokenUsage` (from `token_usage`)
- `ChatResponse` (from `chat_response`)
- `ChatResponseChoice` (from `chat_response`)
- `StreamResponse` (from `stream_response`)
- `StreamingChoice` (from `stream_response`)

### `tool_handler/__init__.py`
Exports:
- `ToolDefinition` (from `tool_definition`)
- `ToolInvocation` (from `tool_invocation`)
- `ToolInvocationStatus` (from `tool_invocation`)
- `ToolChoice` (from `tool_choice`)

### `model_handler/__init__.py`
Exports:
- `ModelSpec` (from `model_spec`)
- `ProviderInfo` (from `provider_info`)
- `ProviderPreferences` (from `provider_info`)
- `ModelPricing` (from `model_pricing`)

## Class Hierarchy

```
BaseModel (Pydantic)
├── TokenUsage
│   └── used by ChatResponse
│
├── ContentBlock
│   └── used by UserMessage
│
├── BaseMessage
│   ├── TextMessage
│   ├── UserMessage
│   ├── AssistantMessage
│   ├── SystemMessage
│   └── ToolMessage
│
├── ChatResponseChoice
│   └── used by ChatResponse
│
├── ChatResponse
│
├── StreamingChoice
│   └── used by StreamResponse
│
├── StreamResponse
│
├── ToolDefinitionFunction
│   └── used by ToolDefinition
│
├── ToolDefinition
│
├── ToolInvocation
│
├── ToolInvocationStatus
│
├── ToolChoice
│
├── ModelPricing
│   └── used by ModelSpec
│
├── ModelSpec
│
├── ProviderInfo
│
└── ProviderPreferences
```

## Type Definitions

Each class typically has a TypedDict companion for serialization:

```python
class MessageTypedDict(TypedDict): ...
class MessageResponse(BaseModel): ...

class UserMessageTypedDict(TypedDict): ...
class UserMessage(BaseMessage): ...

# etc.
```

This dual approach provides:
1. **Runtime validation** via Pydantic
2. **Static type checking** via TypedDict/IDE
3. **Serialization flexibility** with TypedDict

## Usage Pattern Summary

### Creating Messages
```python
# Single message types
msg = UserMessage(payload="Hello")
msg = SystemMessage(instructions="Be helpful")
msg = AssistantMessage(response="Hi there!")

# Generic message type
from typing import List
messages: List[Message] = [msg, ...]
```

### Creating Responses
```python
usage = TokenUsage(prompt_tokens=50, completion_tokens=30)
choice = ChatResponseChoice(index=0, generated_text="...")
response = ChatResponse(
    response_id="...",
    deployed_model="gpt-4",
    generated_at=time.time(),
    usage=usage,
    choices=[choice]
)
```

### Creating Tools
```python
func = ToolDefinitionFunction(name="search", parameters={...})
tool = ToolDefinition(function=func)

invocation = ToolInvocation(
    invocation_id="call_1",
    tool_name="search",
    arguments={"query": "..."},
    call_timestamp=time.time()
)
```

### Creating Models & Providers
```python
pricing = ModelPricing(prompt_cost="0.03", completion_cost="0.06")
model = ModelSpec(
    model_id="gpt4",
    model_name="GPT-4",
    model_slug="gpt-4",
    pricing=pricing,
    creation_date=time.time(),
    context_window=8192
)

prefs = ProviderPreferences(
    enable_fallback=True,
    preferred_providers=["openai"],
    sort_by="latency"
)
```

## Cross-References

### Message Contains
- `content` (str | List[ContentBlock])
- `metadata` (Optional[Dict])
- `msg_id` (Optional[str])

### ChatResponse Contains
- `use` (TokenUsage)
- `choices` (List[ChatResponseChoice])

### AssistantMessage Contains
- `tool_invocations` (List[ToolInvocation])

### ModelSpec Contains
- `pricing` (ModelPricing)

---

This comprehensive typing structure ensures type safety throughout the framework while remaining flexible for future extensions.
