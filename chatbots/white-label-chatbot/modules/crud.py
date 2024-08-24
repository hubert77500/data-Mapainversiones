from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from modules import models, schemas


# Get messages ordered by date
def get_messages(db: Session, sender_id: str, session_id: int):
    return (db.query(models.ChatMessage)
            .filter(models.ChatMessage.conversation_sender_id == sender_id, models.ChatMessage.session_id == session_id)
            .order_by(models.ChatMessage.date).all())


def create_message(db: Session, message: schemas.ChatMessageModel):
    db_message = models.ChatMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def create_csv_file(db: Session, file: schemas.CsvFileModel):
    db_file = models.CsvFile(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_all_csv_files(db: Session):
    return db.query(models.CsvFile).all()


def delete_csv_file(db: Session, file_id: int):
    db.query(models.CsvFile).filter(models.CsvFile.id == file_id).delete()
    db.commit()
    return file_id


def add_allowed_number(db: Session, number: schemas.AllowedNumberModel):
    db_number = models.AllowedNumber(**number.dict())
    db.add(db_number)
    db.commit()
    db.refresh(db_number)
    return db_number


def remove_allowed_number(db: Session, number_id: int):
    db.query(models.AllowedNumber).filter(models.AllowedNumber.id == number_id).delete()
    db.commit()
    return number_id


def check_allowed_number(db: Session, number: str):
    return db.query(models.AllowedNumber).filter(models.AllowedNumber.number == number).first() is not None


def get_session(db: Session, sender_id: str):
    return db.query(models.ChatSession).filter(models.ChatSession.sender_id == sender_id).first()


def create_session(db: Session, session: schemas.SessionModel):
    db_session = models.ChatSession(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def update_session_last_message_at(db: Session, session: models.ChatSession):
    session.last_message_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


def get_tags(db: Session):
    return db.query(models.Tag).all()


def get_tag_by_name(db: Session, name: str):
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def create_sender_tag(db: Session, sender_tag: schemas.SenderTagModel):
    db_sender_tag = models.SenderTag(**sender_tag.dict())
    db.add(db_sender_tag)
    db.commit()
    db.refresh(db_sender_tag)
    return db_sender_tag


def get_conversations_by_date(db: Session, sender_id: str, date: datetime):
    next_day = date + timedelta(days=1)
    return db.query(models.ChatMessage).filter(
        models.ChatMessage.conversation_sender_id == sender_id,
        models.ChatMessage.date >= date,
        models.ChatMessage.date < next_day
    ).all()
