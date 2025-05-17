from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, function_tool
from datetime import datetime,UTC
import httpx

from models import Message, Response, Metadata

app = FastAPI(
    title="DACA Chat Service",
    description="A FastAPI-based Chat Service for the DACA tutorial series",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@function_tool
def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

chat_agent = Agent(
    name="ChatAgent",
    instructions="You are a helpful chatbot. Respond to user messages in a friendly and informative way. If the user asks for the time, use the get_current_time tool. Personalize responses using user analytics (e.g., message count).",
    model="gpt-4o",
    tools=[get_current_time],
)

async def get_db():
    return {"connection": "Mock DB Connection"}

@app.get("/")
async def root():
    return {"message": "Welcome to the DACA Chat Service! Access /docs for the API documentation."}

@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

@app.post("/chat/", response_model=Response)
async def chat(message: Message, db: dict = Depends(get_db)):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    print(f"DB Connection: {db['connection']}")

    # Synchronously call the Analytics Service to get user analytics
    async with httpx.AsyncClient() as client:
        try:
            analytics_response = await client.get(f"http://localhost:8001/analytics/{message.user_id}")
            analytics_response.raise_for_status()
            analytics_data = analytics_response.json()
            message_count = analytics_data.get("message_count", 0)
        except httpx.HTTPStatusError as e:
            message_count = 0  # Fallback if Analytics Service fails
            print(f"Failed to fetch analytics: {e}")

    # Update the agent's instructions with user analytics
    personalized_instructions = (
        f"You are a helpful chatbot. Respond to user messages in a friendly and informative way. "
        f"If the user asks for the time, use the get_current_time tool. "
        f"The user has sent {message_count} messages so far, so personalize your response accordingly."
    )
    chat_agent.instructions = personalized_instructions

    # Use the OpenAI Agents SDK to process the message
    result = await Runner.run(chat_agent, input=message.text)
    reply_text = result.final_output

    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )