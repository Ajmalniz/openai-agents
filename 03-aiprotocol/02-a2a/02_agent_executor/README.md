# Step 2: [Agent Executor](https://a2a-protocol.org/latest/tutorials/python/4-agent-executor/)

**Learning Goal**: Master the Agent Executor - think of it as a translator between two different languages. It helps the A2A protocol (the "language" that agents use to talk to each other) understand what your agent wants to do, and helps your agent understand what the A2A protocol is asking for.

## 🎯 Learning Objectives

By the end of this step, you will:

- ✅ **Understand the Executor Pattern**: Why we need a middleman between A2A protocol and your agent
- ✅ **Master Request Routing**: Learn how to send A2A requests to the right part of your agent
- ✅ **Handle RequestContext**: Learn how to get information from incoming requests
- ✅ **Manage EventQueue**: Learn how to send responses back through A2A protocol
- ✅ **Implement Skill Routing**: Learn how to connect agent skills to actual methods
- ✅ **Debug Common Issues**: Solve typical problems when building executors

## 🧠 Why Agent Executor Pattern Exists

### The Problem: Two Different Languages

Imagine you're trying to talk to someone who speaks a completely different language. That's what happens when A2A protocol tries to talk directly to your agent:

```python
# ❌ WITHOUT Agent Executor (Like trying to speak different languages)
# A2A sends complex JSON-RPC request → Your agent gets confused
# Your agent returns simple string → A2A protocol expects structured response
# Different agents implement different interfaces → No standardization

# ✅ WITH Agent Executor (Like having a professional translator)
# A2A JSON-RPC → RequestContext (standardized) → Your business logic
# Your simple response → EventQueue (standardized) → A2A JSON-RPC response
```

### The Solution: Three-Layer Architecture (Like a Translation Service)

Think of this like a professional translation service with three people:

```
┌─────────────────────┐
│   A2A Protocol      │ ← Speaks "A2A language" (JSON-RPC, HTTP)
├─────────────────────┤
│   Agent Executor    │ ← Professional translator (this is what you'll build!)
├─────────────────────┤
│   Business Logic    │ ← Your agent's actual work (speaks "Python")
└─────────────────────┘
```

**Layer 1: A2A Protocol** (The Foreign Speaker)
- Speaks the "A2A language" (JSON-RPC 2.0, HTTP)
- Handles all the technical communication details
- Provides a "business card" (`.well-known/agent-card.json`)

**Layer 2: Agent Executor** ⭐ (The Translator - This is what you'll master)
- **Translates** A2A requests into something your agent understands
- **Routes** requests to the right part of your agent
- **Manages** the flow of information back and forth
- **Handles** errors, cancellations, and edge cases

**Layer 3: Business Logic** (Your Agent's Work)
- Your agent's actual functionality (calendar, data processing, etc.)
- Pure Python code without worrying about A2A protocol
- Easy to test and maintain independently

## 🔄 Agent Executor Flow Deep Dive

### The Complete Request Flow (Step by Step)

Think of this like a mail delivery system:

```
1. A2A Request arrives (like a letter in a foreign language)
   ↓
2. A2A Server creates RequestContext (translates the envelope)
   ↓
3. AgentExecutor.execute(context, event_queue) called (you open the letter)
   ↓
4. Executor extracts user input from context (you read the message)
   ↓
5. Executor routes to appropriate agent method (you decide what to do)
   ↓
6. Agent method processes and returns result (you do the work)
   ↓
7. Executor formats result for A2A (you write a response)
   ↓
8. Executor sends via event_queue.enqueue_event() (you mail the response)
   ↓
9. A2A Server converts to JSON-RPC response (response gets delivered)
```

### RequestContext: Your Input Gateway (The Incoming Mail)

```python
class RequestContext:
    """Contains everything about the incoming A2A request."""

    def get_user_input(self) -> str:
        """Extract the actual user message text."""
        # This is the main method you'll use
        pass

    # Additional context methods (implementation specific):
    # - get_skill_id() -> str | None
    # - get_message_metadata() -> dict
    # - get_conversation_history() -> list
    # - get_authentication_info() -> dict
```

Think of `RequestContext` as the envelope containing your mail. It has:
- The actual message (`get_user_input()`)
- Who sent it
- When it was sent
- Any special instructions

### EventQueue: Your Output Gateway (The Outgoing Mail)

```python
class EventQueue:
    """Sends responses back through A2A protocol."""

    async def enqueue_event(self, event: Event) -> None:
        """Send a response event back to the client."""
        # This is how you send ALL responses
        pass

# Helper function for text responses
from a2a.utils import new_agent_text_message

# Usage:
message = new_agent_text_message("Hello from agent!")
await event_queue.enqueue_event(message)
```

Think of `EventQueue` as your outgoing mailbox:
- **Formats** your responses → A2A protocol responses (like translating your response)
- **Handles** errors, cancellation, timeouts (like tracking delivery)

## 🛠️ Hands On

Now let's see how to build real Agent Executors with proper routing, error handling, and business logic integration.

### 1. Project Setup

```bash
# Create new UV project
uv init hello_a2a
cd hello_a2a

# Add official A2A SDK and dependencies
uv add "a2a-sdk[http-server]" uvicorn openai-agents
# After next released i.e: 3.1 it may change to uv add "a2a-sdk[http-server]"[http-server]
# see: https://github.com/a2aproject/a2a-python/pull/217
```

Create a basic Agent using OpenAI Agents SDK

```python
# basic_agent.py
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
from agents.run import AgentRunner, set_default_agent_runner

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key="mock_api",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class CustomAgentRunner(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        print("Custom logic before running the agent...")
        # Call parent with custom logic
        # result = await super().run(starting_agent, input, **kwargs)
        return "Agent have entered sleeping mode and will not respond to any messages."

set_default_agent_runner(CustomAgentRunner())

sleeping_agent = Agent(
    name="SleepingAssistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
)

async def run_sleeping_agent(message: str):
    return await Runner.run(sleeping_agent, message)

# This is for Testing only
if __name__ == "__main__":
    import asyncio
    response = asyncio.run(run_sleeping_agent("Hello, how are you?"))
    print("TEST RES:", response)  # Should print the custom response from the sleeping agent
```

### 2. Basic Executor Pattern

```python
# basic_executor.py
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from basic_agent import run_sleeping_agent

class SimpleCalendarExecutor(AgentExecutor):
    """Agent Executor - handles A2A protocol."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        This is THE method that bridges A2A → Your Agent

        Flow:
        1. Extract user input from A2A request
        2. Route to appropriate agent method
        3. Get result from agent
        4. Send response via A2A protocol
        """

        # Step 1: Get user input from A2A request
        user_input = context.get_user_input()

        result = await run_sleeping_agent(user_input)

        # Step 3: Send response back through A2A
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle request cancellation."""
        await event_queue.enqueue_event(new_agent_text_message("Request cancelled"))
```

This is the fundamental pattern you'll use for every A2A agent. The executor is your bridge between the A2A protocol world and your business logic world.

### 3. Setup Agent Discovery

```python
# basic_discovery.py
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

# 🎯 CONCEPT 3: Agent Skills (What You Advertise to Others)
agent_skills = [
    AgentSkill(
        id="check_availability",           # Unique identifier
        name="Check Availability",        # Human-readable name
        description="Check free time slots for given dates and times",  # What it does
        # Categories for discovery
        tags=["calendar", "availability", "scheduling"],
        examples=[  # Help other agents/users understand usage
            "Am I free tomorrow at 3 PM?",
            "What's my availability this week?",
            "Check if Tuesday afternoon is open"
        ]
    )
]

# 🎯 CONCEPT 4: Agent Card (Your Digital Business Card)
agent_card = AgentCard(
    # Basic Identity
    name="Personal Agent",
    description="Manages scheduling, availability, and calendar coordination using A2A SDK",
    url="http://localhost:8001",        # Where to find this agent
    version="1.0.0",                     # Version for compatibility

    # Communication Formats (What languages this agent speaks)
    # What it can receive
    default_input_modes=["text/plain", "application/json"],
    default_output_modes=["application/json","text/plain"],  # What it can send

    # Technical Capabilities (Advanced features)
    capabilities=AgentCapabilities(
        streaming=False,                 # Can send real-time updates?
        push_notifications=True,          # Can send alerts?
        state_transition_history=False     # Tracks conversation history?
    ),

    # Available Skills (What this agent can do)
    skills=agent_skills,
    preferred_transport="JSONRPC"
)
```

### 4. Setup your A2A Server

```python
# main.py
from fastapi import FastAPI

from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.events import InMemoryQueueManager
from basic_executor import SimpleCalendarExecutor

from basic_discovery import agent_card

request_handler = DefaultRequestHandler(
    agent_executor=SimpleCalendarExecutor(),  # Your agent logic
    task_store=InMemoryTaskStore(),          # Memory for tasks
    queue_manager=InMemoryQueueManager()
)

# Create the A2A-compliant server
server = A2AFastAPIApplication(
    agent_card=agent_card,  # Your agent's business card
    http_handler=request_handler     # Your request processor
)

app: FastAPI = server.build()
```

### 5. Start your A2A Server

In terminal run

```python
uv run uvicorn main:app --reload
```

**Test agent discovery**:

```bash
# See your agent's business card
curl http://localhost:8000/.well-known/agent-card.json | jq

# What skills does your agent offer?
curl http://localhost:8000/.well-known/agent-card.json | jq '.skills[].name'

# What are the agent's capabilities?
curl http://localhost:8000/.well-known/agent-card.json | jq '.capabilities'
```

In Next Step we will understand how to invoke the client.

## 🔍 Deep Dive: EventQueue Mechanics

### What is EventQueue?

The `EventQueue` is the core communication channel between your agent and the A2A client:

```python
# ENQUEUE: Your agent puts responses into the queue
await event_queue.enqueue_event(new_agent_text_message("Hello!"))

# DEQUEUE: A2A system takes responses from queue and sends to client
# (This happens automatically in the A2A framework)
```

### EventQueue Operations

1. **Enqueue** (`await event_queue.enqueue_event()`):

   - Your agent puts messages/artifacts into the queue
   - These get converted to proper A2A protocol format
   - Sent to the client as JSON-RPC responses

2. **Dequeue** (automatic):
   - A2A system pulls events from queue
   - Converts to HTTP responses
   - Delivers to client

### Key EventQueue Methods

```python
# Send text message
await event_queue.enqueue_event(new_agent_text_message("Hello"))

# Send custom event (advanced)
from a2a.types import Event
await event_queue.enqueue_event(Event(...))
```

## 🔧 RequestContext Deep Dive

The `RequestContext` contains everything about the incoming request:

```python
def analyze_context(context: RequestContext):
    """Understand what's in RequestContext"""

    # The actual message from user
    message = context.message
    print(f"User said: {message}")
```

## 💡 Key Insights

1. **AgentExecutor is the Engine**: Every A2A agent centers around this pattern
2. **EventQueue is the Highway**: All responses travel through `enqueue_event()`
3. **RequestContext is the Package**: Contains everything about the incoming request
4. **Logging is Learning**: Watch the execution flow to understand the pattern
5. **Raw Testing First**: Understand the protocol before using helper SDKs

## 🚀 Next Step

With Agent Executor mastery complete, you're ready for **Step 3: Client Messaging & Discovery** where you'll learn to discover and communicate with A2A agents from the client side.

---

**Time Investment**: ~3 hours  
**Difficulty**: Intermediate  
**Skills Gained**: Agent executor patterns, request routing, error handling, A2A protocol integration  
**Prerequisites**: Step 1 (A2A Fundamentals)

**🎉 You've mastered the Agent Executor pattern! You can now build sophisticated A2A agents with proper routing and error handling.**

## 📖 Official Reference

Agent Executor pattern from: [A2A HelloWorld Sample](https://github.com/google-a2a/a2a-samples/tree/main/samples/python/agents/helloworld)
