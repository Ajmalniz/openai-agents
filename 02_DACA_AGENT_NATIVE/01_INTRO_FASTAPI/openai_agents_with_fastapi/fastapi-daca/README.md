# DACA Chatbot API

A FastAPI-based API for a chatbot implementation using OpenAI Agents SDK with Gemini integration. This project demonstrates how to build a modern chatbot API with streaming capabilities and proper error handling.

## Features

- FastAPI-based REST API
- Integration with Gemini AI model
- Streaming chat responses
- CORS support for frontend integration
- Structured request/response models using Pydantic
- Built-in time tool for agent responses
- Session management with unique IDs
- Error handling for invalid requests

## Prerequisites

- Python 3.8+
- Gemini API key

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv openai-agents
   ```

## Running the Application

Start the server using uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

#### GET /
- Returns a welcome message
- Response: `{"message": "Welcome to the DACA Chatbot API! Access /docs for the API documentation."}`

#### GET /users/{user_id}
- Get user information
- Query Parameters:
  - `role` (optional): User role
- Response: `{"user_id": "string", "role": "string"}`

#### POST /chat/
- Send a chat message and get a response
- Request Body:
  ```json
  {
    "user_id": "string",
    "text": "string",
    "metadata": {
      "timestamp": "datetime",
      "session_id": "string"
    },
    "tags": ["string"]
  }
  ```
- Response: Chat response with metadata

#### POST /chat/stream
- Stream chat responses in real-time
- Uses Server-Sent Events (SSE)
- Same request body as `/chat/`
- Returns streaming response chunks

## CORS Configuration

The API is configured to accept requests from `http://localhost:3000` for frontend integration. You can modify the CORS settings in `main.py` to allow different origins.

## Error Handling

The API includes proper error handling for:
- Empty messages
- Missing API keys
- Invalid requests

## License

This project is part of the DACA tutorial series.
