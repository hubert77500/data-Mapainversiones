from datetime import datetime

from sqlalchemy.orm import Session

from modules.crud import get_session, create_session
from modules.schemas import SessionModel


def get_or_create_session(db: Session, sender_id: str):
    session = get_session(db, sender_id)
    session_expire_time_minutes = 60 * 24
    if session is None or (datetime.utcnow() - session.last_message_at).total_seconds() > session_expire_time_minutes * 60:
        session = create_session(db, SessionModel(id=None, sender_id=sender_id, created_at=datetime.utcnow(), last_message_at=datetime.utcnow()))
    return session