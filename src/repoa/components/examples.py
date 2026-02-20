"""Example usage of REPOA Components."""

from repoa.components import (
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ToolMessage,
    ChatResponse,
    ChatResponseChoice,
    TokenUsage,
    ToolDefinition,
    ToolDefinitionFunction,
    ToolInvocation,
    ModelSpec,
    ModelPricing,
    ProviderPreferences,
)
import time
from typing import List


def example_basic_conversation():
    """Example: Basic conversation flow."""
    print("=== Example 1: Basic Conversation ===\n")
    
    # Create system prompt
    system = SystemMessage(
        instructions="You are a helpful AI assistant.",
        priority=100
    )
    
    # Create user message
    user = UserMessage(
        payload="What is machine learning?",
        session_id="sess_123"
    )
    
    # Create assistant response
    assistant = AssistantMessage(
        response="Machine learning is a subset of AI that enables systems to learn from data.",
        tokens_used=45
    )
    
    print(f"System: {system.instructions}")
    print(f"User: {user.payload}")
    print(f"Assistant: {assistant.response}")
    print(f"Tokens used: {assistant.tokens_used}\n")


def example_with_token_tracking():
    """Example: Response with token tracking."""
    print("=== Example 2: Token Tracking ===\n")
    
    # Track token usage
    usage = TokenUsage(
        prompt_tokens=150,
        completion_tokens=75,
        cache_read_tokens=50
    )
    
    # Create response with token info
    choice = ChatResponseChoice(
        index=0,
        finish_reason="stop",
        generated_text="Here's my response..."
    )
    
    response = ChatResponse(
        response_id="resp_abc123",
        deployed_model="gpt-4-turbo",
        generated_at=time.time(),
        usage=usage,
        choices=[choice]
    )
    
    print(f"Response ID: {response.response_id}")
    print(f"Model: {response.deployed_model}")
    print(f"Total tokens: {response.usage.total_tokens}")
    print(f"  Prompt: {response.usage.prompt_tokens}")
    print(f"  Completion: {response.usage.completion_tokens}")
    print(f"  Cache read: {response.usage.cache_read_tokens}\n")


def example_tool_calling():
    """Example: Tool calling workflow."""
    print("=== Example 3: Tool Calling ===\n")
    
    # Define a tool
    calculator_func = ToolDefinitionFunction(
        name="calculate",
        description="Perform mathematical calculations",
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"}
            },
            "required": ["expression"]
        }
    )
    
    tool_def = ToolDefinition(function=calculator_func)
    print(f"Tool defined: {tool_def.function.name}")
    print(f"Description: {tool_def.function.description}\n")
    
    # Tool invocation request
    invocation = ToolInvocation(
        invocation_id="call_xyz123",
        tool_name="calculate",
        arguments={"expression": "25 * 4"},
        call_timestamp=time.time()
    )
    
    print(f"Tool invoked: {invocation.tool_name}")
    print(f"Arguments: {invocation.arguments}\n")
    
    # Tool response
    tool_response = ToolMessage(
        tool_call_id=invocation.invocation_id,
        execution_result=100,
        execution_status="completed"
    )
    
    print(f"Tool response: {tool_response.execution_result}")
    print(f"Status: {tool_response.execution_status}\n")


def example_model_and_provider():
    """Example: Model and provider configuration."""
    print("=== Example 4: Model & Provider Config ===\n")
    
    # Define model pricing
    pricing = ModelPricing(
        prompt_cost="0.03",
        completion_cost="0.06",
        image_cost="0.01"
    )
    
    # Define model
    model = ModelSpec(
        model_id="gpt-4-20240115",
        model_name="GPT-4 Turbo",
        model_slug="gpt-4-turbo",
        pricing=pricing,
        creation_date=time.time(),
        context_window=128000,
        description="Advanced reasoning model",
        architecture="Transformer"
    )
    
    print(f"Model: {model.model_name}")
    print(f"Slug: {model.model_slug}")
    print(f"Context: {model.context_window} tokens")
    print(f"Pricing (per 1M tokens):")
    print(f"  Prompt: ${model.pricing.prompt_cost}")
    print(f"  Completion: ${model.pricing.completion_cost}\n")
    
    # Configure provider preferences
    prefs = ProviderPreferences(
        enable_fallback=True,
        preferred_providers=["openai", "anthropic"],
        blocked_providers=["unreliable-provider"],
        sort_by="latency",
        data_retention_policy="deny"
    )
    
    print(f"Provider Preferences:")
    print(f"  Fallback enabled: {prefs.enable_fallback}")
    print(f"  Preferred: {', '.join(prefs.preferred_providers)}")
    print(f"  Sort by: {prefs.sort_by}")
    print(f"  Data policy: {prefs.data_retention_policy}\n")


def example_conversation_flow():
    """Example: Complete conversation workflow."""
    print("=== Example 5: Complete Conversation Flow ===\n")
    
    # Initialize
    messages: List = []
    
    # Step 1: System context
    system = SystemMessage(
        instructions="You are a Python programming expert.",
        priority=100
    )
    messages.append(system)
    print(f"[1] Added system message")
    
    # Step 2: User question
    user = UserMessage(
        payload="How do I use decorators in Python?",
        session_id="conv_001"
    )
    messages.append(user)
    print(f"[2] User asked: {user.payload}")
    
    # Step 3: LLM response (simulated)
    usage = TokenUsage(prompt_tokens=50, completion_tokens=150)
    assistant = AssistantMessage(
        response="Decorators are functions that modify other functions...",
        tokens_used=usage.total_tokens,
        stop_reason="end_turn"
    )
    messages.append(assistant)
    print(f"[3] Assistant responded ({usage.total_tokens} tokens)")
    
    # Step 4: Follow-up
    user2 = UserMessage(payload="Can you show me an example?")
    messages.append(user2)
    print(f"[4] Follow-up: {user2.payload}")
    
    # Step 5: Response with example
    assistant2 = AssistantMessage(
        response="""
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def hello():
    print("Hello!")
        """,
        tokens_used=200
    )
    messages.append(assistant2)
    print(f"[5] Code example provided")
    
    print(f"\nConversation length: {len(messages)} turns\n")


if __name__ == "__main__":
    example_basic_conversation()
    example_with_token_tracking()
    example_tool_calling()
    example_model_and_provider()
    example_conversation_flow()
    
    print("=== All examples completed ===")
