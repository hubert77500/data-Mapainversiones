import os
import requests
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from modules import crud, schemas
from modules.config import USE_PHONE_NUMBER_WHITELIST
from modules.crud import check_allowed_number
from modules.send_message import send_response_message, send_text_message
from modules.sessions import get_or_create_session

# Load environment variables from .env
load_dotenv()

# Get the QUERY_RESOLVER_API from environment variables
API_URL = os.getenv("QUERY_RESOLVER_API")

# Define a constant for maximum message length
MAX_MESSAGE_LENGTH = 4096  # Adjust this as per WhatsApp's limits

async def process_message(message_text, message_id, sender_id, db: Session):
    print(f"Sender ID: {sender_id}, Message: {message_text}, Message ID: {message_id}")

    if USE_PHONE_NUMBER_WHITELIST == "True":
        if not check_allowed_number(db, sender_id):
            await send_text_message(sender_id, "Lo sentimos, no tienes permiso para usar este servicio.")
            return

    # Prepare the payload for the API call
    country = "Republica Dominicana"  # Set the country based on your logic
    payload = {
        "prompt": message_text,
        "country": country
    }

    # Make the API call to generate the SQL query and explanation
    try:
        response = requests.post(API_URL, json=payload)
        print(f"API Status Code: {response.status_code}")
        print(f"API Raw Response: {response.text}")

        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        explanation = response_data.get('explanation', "No explanation provided.")
        result = response_data.get('result', {})
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        explanation = "Failed to generate a response due to an error with the API request."
        result = {}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        explanation = "Received an invalid JSON response."
        result = {}

    # Construct the final message
    final_message = f"{explanation}\n\n"

    # Check if the result is in the expected format and not empty
    if isinstance(result, dict) and result:
        # Convert the result dictionary to a more readable format
        for i in range(len(next(iter(result.values())))):  # Iterate over the number of rows
            for key in result:
                final_message += f"{key}: {result[key].get(str(i), '')}\n"
            final_message += "\n"  # Add a blank line between rows
    else:
        final_message += "Ask a question / Haz una pregunta."

    # Truncate message if too long
    if len(final_message) > MAX_MESSAGE_LENGTH:
        final_message = final_message[:MAX_MESSAGE_LENGTH - 3] + "..."

    try:
        # Send a response message to the user via WhatsApp
        await send_response_message(sender_id, final_message.strip())  # Use strip to remove any trailing newline
    except Exception as e:
        print(f"Failed to send message: {e}")

    print('Response message sent')

    # Save the response message to the database
    session = get_or_create_session(db, sender_id)
    crud.create_message(db, schemas.ChatMessageModel(conversation_sender_id=sender_id, content=final_message.strip(), is_system=True,
                                                     session_id=session.id))
    crud.update_session_last_message_at(db, session)
