from sqlalchemy.orm import Session
from modules.database import SessionLocal
from modules.models import Tag
from modules.schemas import TagModel


def seed_tags(db: Session):
    # Updated predefined tags
    predefined_tags = [
        "emergencias", "infrastructura", "educacion", "pequeña y mediana empresa", "medio ambiente", "mujer",
        "empleo", "salud"
    ]

    # Add predefined tags to the database
    for tag_name in predefined_tags:
        if not db.query(Tag).filter(Tag.name == tag_name).first():
            tag = TagModel(name=tag_name)
            db_tag = Tag(**tag.dict())
            db.add(db_tag)

    db.commit()
    print("Tags seeded successfully")


if __name__ == "__main__":
    db: Session = SessionLocal()
    try:
        seed_tags(db)
    finally:
        db.close()
