# DACA Microservices with FastAPI

A microservices-based chat application built with FastAPI, featuring separate services for chat, analytics, and memory management.

## Project Structure

```
.
├── chat_service/           # Main chat service with OpenAI integration
│   ├── main.py            # FastAPI application and chat endpoints
│   ├── models.py          # Pydantic models for request/response
│   └── requirements.txt   # Python dependencies
├── analytic_service/      # Analytics service for user metrics
│   ├── main.py           # FastAPI application and analytics endpoints
│   ├── models.py         # Pydantic models for analytics data
│   └── requirements.txt  # Python dependencies
└── memory_service/       # Memory service for user context
    ├── main.py          # FastAPI application and memory endpoints
    ├── models.py        # Pydantic models for memory data
    └── requirements.txt # Python dependencies
```

## Features

- **Chat Service**: 
  - OpenAI-powered chat functionality
  - Customizable agent instructions
  - Time-based tool integration
  - User context awareness

- **Analytics Service**:
  - Message count tracking
  - User activity monitoring
  - Mock data storage (can be extended to use a database)

- **Memory Service**:
  - User action history tracking
  - Context preservation
  - Personalized responses based on past interactions

## Prerequisites

- Python 3.8+
- OpenAI API key
- FastAPI
- Uvicorn
- httpx
- python-dotenv

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies for each service:
```bash
cd chat_service
pip install -r requirements.txt
cd ../analytic_service
pip install -r requirements.txt
cd ../memory_service
pip install -r requirements.txt
```

4. Create a `.env` file in the chat_service directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Services

1. Start the Analytics Service:
```bash
cd analytic_service
uvicorn main:app --reload --port 8001
```

2. Start the Memory Service:
```bash
cd memory_service
uvicorn main:app --reload --port 8002
```

3. Start the Chat Service:
```bash
cd chat_service
uvicorn main:app --reload --port 8000
```

## API Documentation

Once the services are running, you can access the API documentation at:

- Chat Service: http://localhost:8000/docs
- Analytics Service: http://localhost:8001/docs
- Memory Service: http://localhost:8002/docs

## Example Usage

### Chat Endpoint
```bash
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "alice", "text": "What time is it?"}'
```

### Analytics Endpoint
```bash
curl "http://localhost:8001/analytics/alice"
```

### Memory Endpoint
```bash
curl "http://localhost:8002/memories/alice"
```

## Development

- The project uses FastAPI for building the APIs
- Pydantic models for data validation
- OpenAI Agents SDK for chat functionality
- CORS middleware for cross-origin requests
- Async HTTP client for inter-service communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
