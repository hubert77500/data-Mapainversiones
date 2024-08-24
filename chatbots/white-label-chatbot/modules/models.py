from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship

from modules.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    conversation_sender_id = Column(String(255))
    content = Column(String(4000))
    is_system = Column(Boolean)
    session_id = Column(Integer)
    date = Column(DateTime, server_default=func.now(), default=datetime.utcnow)


class CsvFile(Base):
    __tablename__ = "csv_files"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    content = Column(Text())
    date = Column(DateTime, server_default=func.now(), default=datetime.utcnow)


class AllowedNumber(Base):
    __tablename__ = "allowed_numbers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    number = Column(String(20), unique=True)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True)
    sender_id = Column(String(255))
    created_at = Column(DateTime, server_default=func.now(), default=datetime.utcnow)
    last_message_at = Column(DateTime, server_default=func.now(), default=datetime.utcnow)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)


class SenderTag(Base):
    __tablename__ = "sender_tags"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    assigned_at = Column(DateTime, default=datetime.utcnow)

    tag = relationship("Tag")
