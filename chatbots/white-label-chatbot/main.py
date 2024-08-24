from fastapi import FastAPI, HTTPException, Query, Request, Depends, BackgroundTasks
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from modules import models, crud, schemas
from modules.config import FACEBOOK_WEBHOOK_VERIFY_TOKEN
from modules.database import SessionLocal, engine
from modules.process_message import process_message
from modules.tags import assign_tags
from modules.seeder import seed_tags

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to receive messages from Whatsapp
@app.post("/whatsapp-webhook/", response_class=PlainTextResponse, status_code=200)
async def receive_whatsapp_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Endpoint to receive messages from Whatsapp.
    """
    data = await request.json()
    if 'contacts' not in data['entry'][0]['changes'][0]['value'] or 'messages' not in data['entry'][0]['changes'][0][
        'value']:
        return "Skipped"
    sender_id = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
    message_text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    message_id = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    background_tasks.add_task(process_message, message_text, message_id, sender_id, db)
    return "Message received"


# Endpoint to verify the webhook with Facebook
@app.get("/whatsapp-webhook/", response_class=PlainTextResponse)
async def verify_token(hub_mode: str = Query(..., alias="hub.mode"),
                       hub_challenge: str = Query(..., alias="hub.challenge"),
                       hub_verify_token: str = Query(..., alias="hub.verify_token")):
    """
    Endpoint to verify the webhook with Facebook.
    """
    if hub_mode == "subscribe" and hub_verify_token == FACEBOOK_WEBHOOK_VERIFY_TOKEN:
        return hub_challenge
    else:
        raise HTTPException(status_code=403, detail="Invalid verification token")


# Endpoint to run the seeder
@app.post("/run-seeder/", response_class=PlainTextResponse)
async def run_seeder(db: Session = Depends(get_db)):
    """
    Endpoint to run the seeder and populate the database with predefined tags.
    """
    seed_tags(db)
    return "Tags seeded successfully"


# Endpoint to run the tag assignment
@app.get("/assign-tags/", response_class=PlainTextResponse)
async def run_assign_tags():
    """
    Endpoint to run the tag assignment process.
    """
    assign_tags()
    return "Tags assigned successfully"
