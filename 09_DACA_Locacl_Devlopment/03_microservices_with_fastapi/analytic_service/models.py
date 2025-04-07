from pydantic import BaseModel

class Analytics(BaseModel):
    message_count: int