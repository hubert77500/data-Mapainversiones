from sqlalchemy.orm import Session
from modules.database import SessionLocal
from modules import crud, schemas, models
from modules.config import OPENAI_API_KEY
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage


def assign_tags():
    db: Session = SessionLocal()
    try:
        tags = crud.get_tags(db)
        tag_names = [tag.name for tag in tags]

        # Get yesterday's conversations
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        senders = db.query(models.ChatMessage.conversation_sender_id).distinct().all()

        for sender_tuple in senders:
            sender = sender_tuple[0]
            conversations = crud.get_conversations_by_date(db, sender, yesterday)
            conversation_text = " ".join([msg.content for msg in conversations])

            if not conversation_text:
                continue

            # Construct the prompt for the LLM
            prompt = f"""
                Analyze the following conversation and assign one of the following tags: {', '.join(tag_names)}.
                Conversation: {conversation_text}
                Tag:
            """

            message = [
                SystemMessage(content=prompt),
            ]

            # Initialize the LLM
            llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4-turbo")

            # Invoke the LLM
            print('invoking LLM...')
            response = llm.invoke(message).content.strip()
            print('LLM invoked')

            # Get the tag ID
            tag = crud.get_tag_by_name(db, response)
            if tag:
                sender_tag = schemas.SenderTagModel(sender_id=sender, tag_id=tag.id)
                crud.create_sender_tag(db, sender_tag)

    finally:
        db.close()
