# A2A Fundamentals: Building Your First AI Agent

**What You'll Learn**: How to create an AI agent that can talk to other AI agents using the official A2A (Agent-to-Agent) system.

## 🎯 What is A2A? (Simple Explanation)

Imagine you're building a digital marketplace where AI assistants can:
- **Find each other** (like looking someone up in a phone book)
- **Know what each other can do** (like reading someone's resume)
- **Work together** (like humans collaborating on a project)

**A2A makes this possible** by providing a standard way for AI agents to:
1. **Introduce themselves** (using "agent cards")
2. **Advertise their skills** (what they can help with)
3. **Communicate** (send messages back and forth)

## 🚀 What You'll Build

You'll create a **Calendar Agent** - an AI assistant that can:
- Check if you're free at certain times
- Schedule meetings for you
- Find scheduling conflicts

This agent will be **discoverable** by other AI agents, meaning they can find it and ask for help with calendar tasks.

## 🛠️ Prerequisites

- **Python 3.12+** installed on your computer
- **UV package manager** (a modern Python package manager)
- Basic understanding of Python (variables, functions, classes)

## 📁 Project Setup

Let's start by creating your project:

```bash
# Create a new project folder
uv init hello_a2a
cd hello_a2a

# Install the A2A toolkit and web server
uv add a2a-sdk uvicorn
```

## 🏗️ Building Your First Agent

### Step 1: Understanding the Structure

Your agent will have **3 main parts**:

1. **The Brain** (CalendarAgent) - Does the actual work
2. **The Translator** (CalendarAgentExecutor) - Converts A2A messages to work requests
3. **The Business Card** (AgentCard) - Tells other agents about you

### Step 2: Create Your Agent File

Create a file called `calendar_agent.py` with this complete code:

```python
# calendar_agent.py - Your First A2A Agent
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue, InMemoryQueueManager
from a2a.utils import new_agent_text_message
from a2a.types import AgentCapabilities, AgentCard, AgentSkill, AgentProvider

# 🧠 PART 1: Your Agent's Brain (The Worker)
class CalendarAgent:
    """
    This is your agent's brain - it does the actual calendar work.
    Think of it as a helpful assistant that knows about your schedule.
    """
    
    async def invoke(self, message) -> str:
        """When someone asks your agent to do something, this method runs."""
        # For now, just return a simple message
        # Later, you'll add real calendar logic here
        return "Hello! I'm your calendar assistant. I can help with scheduling and availability."

# 🔄 PART 2: The Translator (Connects A2A to Your Brain)
class CalendarAgentExecutor(AgentExecutor):
    """
    This is like a translator - it takes A2A protocol messages
    and converts them into calls to your agent's brain.
    """
    
    def __init__(self):
        # Connect to your agent's brain
        self.agent = CalendarAgent()
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        When someone sends a request to your agent, this method handles it.
        """
        # Get what the user asked for
        user_message = context.get_user_input()
        
        # Ask your agent's brain to handle it
        result = await self.agent.invoke(user_message)
        
        # Send the result back through A2A
        await event_queue.enqueue_event(new_agent_text_message(result))
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle if someone wants to cancel a request."""
        raise Exception('Cancellation not supported in this example')

# 🎯 PART 3: Your Agent's Skills (What You Can Do)
calendar_skills = [
    AgentSkill(
        id="check_availability",           # Unique name for this skill
        name="Check Availability",        # Human-readable name
        description="Check if you're free at certain times",  # What it does
        tags=["calendar", "availability", "scheduling"],  # Categories for discovery
        examples=[  # Examples of how to use this skill
            "Am I free tomorrow at 3 PM?",
            "What's my availability this week?",
            "Check if Tuesday afternoon is open"
        ]
    ),
    AgentSkill(
        id="schedule_meeting",
        name="Schedule Meeting",
        description="Book new meetings and send invitations",
        tags=["calendar", "meeting", "scheduling"],
        examples=[
            "Schedule a team meeting for Friday at 2 PM",
            "Book a 1-hour call with John next Tuesday",
            "Set up a project review meeting"
        ]
    ),
    AgentSkill(
        id="find_conflicts",
        name="Find Conflicts",
        description="Spot scheduling problems and suggest fixes",
        tags=["calendar", "conflicts", "optimization"],
        examples=[
            "Check for conflicts in my schedule this week",
            "Find overlapping meetings",
            "Analyze my calendar for double-bookings"
        ]
    )
]

# 🏷️ PART 4: Your Agent's Business Card (How Others Find You)
calendar_agent_card = AgentCard(
    # Basic Information
    name="Personal Calendar Agent",
    description="A helpful AI assistant that manages your calendar and scheduling",
    url="http://localhost:8001/mcp",        # Where to find this agent
    version="1.0.0",                     # Version number

    # Who Built This
    provider=AgentProvider(
        organization="A2A Learning Lab",
        url="https://github.com/a2a-learning"
    ),

    # What Languages You Speak
    default_input_modes=["text/plain", "application/json"],   # What you can receive
    default_output_modes=["application/json", "text/plain"],  # What you can send

    # Advanced Features
    capabilities=AgentCapabilities(
        streaming=False,                 # Can you send real-time updates?
        push_notifications=True,          # Can you send alerts?
        state_transition_history=False     # Do you remember conversations?
    ),

    # Your Skills (What You Can Do)
    skills=calendar_skills
)

# 🚀 PART 5: Start Your Agent Server
if __name__ == "__main__":
    # Create the request handler with your agent
    request_handler = DefaultRequestHandler(
        agent_executor=CalendarAgentExecutor(),  # Your agent
        task_store=InMemoryTaskStore(),          # Memory for tasks
        queue_manager=InMemoryQueueManager()
    )

    # Create the A2A server
    server = A2AFastAPIApplication(
        agent_card=calendar_agent_card,  # Your business card
        http_handler=request_handler     # Your request processor
    )

    # Start the server
    print("🗓️ Starting your Calendar Agent on port 8001...")
    print("📋 Your Agent Card: http://localhost:8001/.well-known/agent-card.json")
    print("🔗 A2A Endpoint: http://localhost:8001/a2a")
    print("🛠️ Skills Available:", [skill.id for skill in calendar_skills])
    print("\n💡 Test it: curl http://localhost:8001/.well-known/agent-card.json")
    
    import uvicorn
    
    # Start the web server
    uvicorn.run(server.build(), host="localhost", port=8001)
```

## 🚀 Running Your Agent

### Step 1: Start Your Agent

```bash
# Make sure you're in the hello_a2a folder
cd hello_a2a

# Run your agent
uv run python calendar_agent.py
```

You should see output like:
```
🗓️ Starting your Calendar Agent on port 8001...
📋 Your Agent Card: http://localhost:8001/.well-known/agent-card.json
🔗 A2A Endpoint: http://localhost:8001/a2a
🛠️ Skills Available: ['check_availability', 'schedule_meeting', 'find_conflicts']
💡 Test it: curl http://localhost:8001/.well-known/agent-card.json
```

### Step 2: Test Your Agent

Open a **new terminal window** (keep your agent running in the first one) and test:

```bash
# See your agent's business card
curl http://localhost:8001/.well-known/agent-card.json

# Or if you have jq installed (for pretty formatting):
curl http://localhost:8001/.well-known/agent-card.json | jq
```

## 🔍 Understanding What You Built

### 1. **Agent Card** (Your Digital Business Card)
- **Purpose**: Tells other agents about you
- **Location**: `http://localhost:8001/.well-known/agent-card.json`
- **Contains**: Your name, skills, contact info, and capabilities

### 2. **Skills** (What You Can Do)
- **check_availability**: Check if you're free
- **schedule_meeting**: Book new meetings
- **find_conflicts**: Spot scheduling problems

### 3. **Discovery** (How Others Find You)
- Other agents can visit your agent card URL
- They can see what skills you offer
- They can send you requests for help

## 🧪 Practice Exercises

### Exercise 1: Add a New Skill

Add this skill to your `calendar_skills` list:

```python
AgentSkill(
    id="send_reminders",
    name="Send Reminders",
    description="Send meeting reminders via email or SMS",
    tags=["calendar", "reminders", "notifications"],
    examples=["Remind me about tomorrow's meeting", "Send a reminder 30 minutes before"]
)
```

**Restart your agent** and test again to see the new skill!

### Exercise 2: Test with a Simple Client

Create a file called `test_client.py`:

```python
# test_client.py - Test your agent
import asyncio
import httpx
import json

async def test_your_agent():
    """Test if your agent is working properly."""
    
    async with httpx.AsyncClient() as client:
        try:
            # Try to get your agent's business card
            response = await client.get("http://localhost:8001/.well-known/agent-card.json")
            agent_card = response.json()

            print("✅ Success! Your agent is working!")
            print(f"   Name: {agent_card['name']}")
            print(f"   Skills: {len(agent_card['skills'])}")

            for skill in agent_card['skills']:
                print(f"     • {skill['name']}: {skill['description']}")

        except Exception as e:
            print(f"❌ Something went wrong: {e}")
            print("💡 Make sure your agent is running!")

if __name__ == "__main__":
    asyncio.run(test_your_agent())
```

Run it:
```bash
uv run python test_client.py
```

## 🎯 What You've Accomplished

✅ **Created your first A2A agent** - A calendar assistant that can be discovered by other agents  
✅ **Defined agent skills** - Clear descriptions of what your agent can do  
✅ **Built an agent card** - A digital business card for discovery  
✅ **Started an A2A server** - Your agent is now online and accessible  
✅ **Tested agent discovery** - Other agents can find and learn about yours  

## 🔮 What This Means

Your calendar agent is now part of a **multi-agent ecosystem** where:

1. **Other agents can find you** by visiting your agent card
2. **They can see your skills** and know what you can help with
3. **They can send you requests** for calendar-related tasks
4. **You can work together** to solve complex problems

## 🚀 Next Steps

Now that you understand the basics, you can:

1. **Add real calendar logic** to your `CalendarAgent.invoke()` method
2. **Create more agents** with different specializations
3. **Build agent networks** where agents collaborate on tasks
4. **Learn advanced A2A features** like streaming responses and state management

## 📚 Key Concepts Summary

- **A2A** = System for AI agents to talk to each other
- **Agent Card** = Digital business card for discovery
- **Skills** = Specific tasks your agent can perform
- **Discovery** = How agents find each other
- **Protocol** = Standard language for agent communication

## 🎉 Congratulations!

You've built your first A2A agent! You now understand:
- How to create an AI agent that can be discovered by others
- How to define what your agent can do (skills)
- How to make your agent accessible via the A2A protocol
- How agents can find and learn about each other

**You're ready to build more sophisticated agents and create multi-agent ecosystems!**

---

**Time Investment**: ~45 minutes  
**Difficulty**: Beginner  
**What You Built**: A discoverable calendar agent with A2A skills  
**Next Level**: Adding real functionality and building agent networks
