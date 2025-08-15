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
    ),
    AgentSkill(
    id="send_reminders",
    name="Send Reminders",
    description="Send meeting reminders via email or SMS",
    tags=["calendar", "reminders", "notifications"],
    examples=["Remind me about tomorrow's meeting", "Send a reminder 30 minutes before"]
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