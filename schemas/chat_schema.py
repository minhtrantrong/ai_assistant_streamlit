from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class Message(BaseModel):
    user_message: str
    bot_message: str
class ChatSchema(BaseModel):
    user_id: str 
    message: list[Message]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

