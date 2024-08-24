from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ChatMessageModel(BaseModel):
    conversation_sender_id: str
    content: str
    is_system: bool
    session_id: int

    class Config:
        from_attributes = True

class SessionModel(BaseModel):
    id: Optional[int]
    sender_id: str
    created_at: datetime
    last_message_at: datetime

    class Config:
        from_attributes = True

class CsvFileModel(BaseModel):
    id: int
    name: str
    content: str
    date: datetime

    class Config:
        from_attributes = True

class AllowedNumberModel(BaseModel):
    id: int
    name: str
    number: str

    class Config:
        from_attributes = True

class TagModel(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

class SenderTagModel(BaseModel):
    id: Optional[int] = None
    sender_id: str
    tag_id: int
    assigned_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
