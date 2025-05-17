from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime,UTC
from uuid import uuid4

class Metadata(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    session_id: str = Field(default_factory=lambda: str(uuid4()))

class Message(BaseModel):
    user_id: str
    text: str
    metadata: Metadata
    tags: Optional[List[str]] = None

class Response(BaseModel):
    user_id: str
    reply: str
    metadata: Metadata