# A2A Fundamentals: Your First AI Agent (Super Beginner Friendly!)

**What You'll Learn**: How to create an AI assistant that can talk to other AI assistants using A2A (Agent-to-Agent).

## 🎯 What is A2A? (Super Simple Explanation)

Imagine you have a bunch of AI assistants, each good at different things:
- One that knows about calendars
- One that knows about weather
- One that knows about recipes

**A2A lets these AI assistants find each other and work together!**

Think of it like:
- **Facebook for AI** - AI assistants can find and connect with each other
- **Teamwork** - They can help each other solve problems
- **Sharing** - They can share information and work together

## 🚀 What You'll Build

You'll create a **Calendar Agent** - an AI assistant that can:
- Check if you're free at certain times
- Schedule meetings for you
- Find scheduling conflicts

**The cool part**: Other AI agents will be able to find your calendar agent and ask for help!

## 🛠️ What You Need to Get Started

- **Python 3.12+** (the programming language we'll use)
- **UV** (a tool to install Python packages - like an app store for code)
- Basic Python knowledge (variables, functions - we'll keep it simple!)

## 📁 Step 1: Create Your Project

Open your terminal/command prompt and type these commands one by one:

```bash
# Create new UV project
uv init hello_a2a
cd hello_a2a

# Add official A2A SDK and dependencies
uv add "a2a-sdk[http-server]" uvicorn
# After next released i.e: 3.1 it may change to uv add "a2a-sdk[http-server]"[http-server]
# see: https://github.com/a2aproject/a2a-python/pull/217
```

**What this does**: Creates a new project folder and installs the A2A toolkit.

## 🏗️ Step 2: Understanding How Your Agent Works

Your agent has **3 main parts** (don't worry, we'll explain each one):

1. **🧠 The Brain** - Does the actual work (like checking your calendar)
2. **🔄 The Translator** - Converts messages from other agents into work requests
3. **🏷️ The Business Card** - Tells other agents about you and what you can do

## 📝 Step 3: Create Your Agent

Create a new file called `calendar_agent.py` in your `hello_a2a` folder and copy this code:

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

## 🚀 Step 4: Run Your Agent

Now let's start your agent! In your terminal (make sure you're in the `hello_a2a` folder):

```bash
uv run python calendar_agent.py
```

**What you should see**:
```
🗓️ Starting your Calendar Agent on port 8001...
📋 Your Agent Card: http://localhost:8001/.well-known/agent-card.json
🔗 A2A Endpoint: http://localhost:8001/a2a
🛠️ Skills Available: ['check_availability', 'schedule_meeting', 'find_conflicts']
💡 Test it: curl http://localhost:8001/.well-known/agent-card.json
```

**Keep this terminal running!** Your agent is now working.

## 🧪 Step 5: Test Your Agent

Open a **new terminal window** (keep your agent running in the first one) and test:

```bash
# See your agent's business card
curl http://localhost:8001/.well-known/agent-card.json
```

**What this does**: Shows you the "business card" that other agents can see.

## 🔍 What You Just Built (Simple Explanation)

### 1. **Your Agent is Now Online!**
- It's running on your computer at `http://localhost:8001`
- Other agents can find it and talk to it
- It has a "business card" that tells others what it can do

### 2. **Your Agent Has Skills**
- **check_availability**: Can check if you're free
- **schedule_meeting**: Can book new meetings
- **find_conflicts**: Can spot scheduling problems

### 3. **Other Agents Can Find You**
- They visit your agent card URL
- They see what skills you offer
- They can ask you for help with calendar tasks

## 🎯 What This Means in Real Life

Imagine you have a team of AI assistants:
- **Weather Agent**: Knows about weather
- **Calendar Agent** (yours!): Knows about your schedule
- **Email Agent**: Knows about your emails

**With A2A, they can work together!**

Example scenario:
1. Someone asks: "Can I have a meeting tomorrow?"
2. **Email Agent** finds your **Calendar Agent**
3. **Calendar Agent** checks your availability
4. **Email Agent** sends a meeting invitation
5. **Calendar Agent** adds it to your schedule

**They just solved a complex problem by working together!**

## 🧪 Practice: Add a New Skill

Let's add another skill to your agent. In your `calendar_agent.py` file, add this to your `calendar_skills` list:

```python
AgentSkill(
    id="send_reminders",
    name="Send Reminders",
    description="Send meeting reminders via email or SMS",
    tags=["calendar", "reminders", "notifications"],
    examples=["Remind me about tomorrow's meeting", "Send a reminder 30 minutes before"]
)
```

**Then restart your agent** (stop it with Ctrl+C and run it again) to see the new skill!

## 🧪 Practice: Test with a Simple Client

Create a new file called `test_client.py` in your `hello_a2a` folder:

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

**Run it**:
```bash
uv run python test_client.py
```

## 🎉 What You've Accomplished!

✅ **Created your first A2A agent** - A calendar assistant that can be discovered by other agents  
✅ **Defined agent skills** - Clear descriptions of what your agent can do  
✅ **Built an agent card** - A digital business card for discovery  
✅ **Started an A2A server** - Your agent is now online and accessible  
✅ **Tested agent discovery** - Other agents can find and learn about yours  

## 🔮 The Big Picture

You've just created a **multi-agent ecosystem** where:

1. **AI agents can find each other** (like looking someone up in a phone book)
2. **They can see what each other can do** (like reading someone's resume)
3. **They can work together** (like humans collaborating on a project)
4. **They can solve complex problems** by combining their different skills

## 🚀 What You Can Do Next

Now that you understand the basics:

1. **Add real calendar logic** to your `CalendarAgent.invoke()` method
2. **Create more agents** with different specializations (weather, email, etc.)
3. **Build agent networks** where agents collaborate on tasks
4. **Learn advanced A2A features** like streaming responses and state management

## 📚 Key Concepts Summary (Simple Version)

- **A2A** = System for AI agents to talk to each other (like social media for AI)
- **Agent** = An AI program that can do specific tasks
- **Agent Card** = Digital business card that tells others about you
- **Skills** = Specific tasks your agent can perform
- **Discovery** = How agents find each other (like looking someone up)
- **Protocol** = Standard language for agent communication (like English for humans)

## 🎯 Real-World Examples

**Smart Home**: Your calendar agent talks to your smart thermostat agent to adjust temperature based on your schedule.

**Business**: Your calendar agent talks to your email agent to automatically schedule meetings from email requests.

**Personal Assistant**: Your calendar agent talks to your weather agent to reschedule outdoor meetings if it's going to rain.

## 🎉 Congratulations!

**You've built your first A2A agent!** You now understand:
- How to create an AI agent that can be discovered by others
- How to define what your agent can do (skills)
- How to make your agent accessible via the A2A protocol
- How agents can find and learn about each other

**You're ready to build more sophisticated agents and create multi-agent ecosystems!**

---

**Time Investment**: ~30 minutes  
**Difficulty**: Super Beginner  
**What You Built**: A discoverable calendar agent with A2A skills  
**Next Level**: Adding real functionality and building agent networks

## 🆘 Need Help?

If something doesn't work:
1. Make sure you're in the right folder (`hello_a2a`)
2. Make sure you installed the packages (`uv add a2a-sdk uvicorn`)
3. Check that your agent is running (you should see the startup messages)
4. Try the test commands to see what's happening

**Remember**: Every expert was once a beginner. You're doing great! 🚀
