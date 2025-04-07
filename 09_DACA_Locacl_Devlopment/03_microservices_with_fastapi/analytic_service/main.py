from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Analytics

app = FastAPI(
    title="DACA Analytics Service",
    description="A FastAPI-based Analytics Service for the DACA tutorial series",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Allow Chat Service
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock user analytics data (in future tutorials, this will come from a database)
MOCK_ANALYTICS = {
    "alice": {"message_count": 5},
    "bob": {"message_count": 3},
}

@app.get("/")
async def root():
    return {"message": "Welcome to the DACA Analytics Service! Access /docs for the API documentation."}

@app.get("/analytics/{user_id}", response_model=Analytics)
async def get_analytics(user_id: str):
    if user_id not in MOCK_ANALYTICS:
        raise HTTPException(status_code=404, detail="User not found")
    return Analytics(**MOCK_ANALYTICS[user_id])