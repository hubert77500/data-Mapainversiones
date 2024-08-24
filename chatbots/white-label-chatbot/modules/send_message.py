import json
import requests
from modules.config import FACEBOOK_WHATSAPP_TOKEN, FACEBOOK_WHATSAPP_API_URL

async def send_response_message(sender_id: str, response_json_str: str):
    print(response_json_str)

    to_number = sender_id

    # Attempt to parse the response as JSON
    try:
        response_dict = json.loads(response_json_str, strict=False)
        response_text = response_dict.get("text")
        response_image = response_dict.get("image")
        response_location = response_dict.get("location")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        response_text = response_json_str  # Fallback to sending the raw response as text
        response_image = None
        response_location = None

    print("tonumber: " + to_number)

    try:
        if response_text:
            await send_text_message(to_number, response_text)

        if response_image:
            print('sending image:' + response_image)
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "image",
                "image": {
                    "link": response_image
                }
            }
            await send_json_response_message(payload)

        if response_location:
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "location",
                "location": {
                    "longitude": response_location.get("longitude"),
                    "latitude": response_location.get("latitude"),
                    "name": response_location.get("name"),
                    "address": response_location.get("address")
                }
            }
            await send_json_response_message(payload)
    except Exception as e:
        print(f"Error sending message: {e}")

async def send_text_message(to_number: str, text: str):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "body": text
        }
    }
    await send_json_response_message(payload)

async def send_json_response_message(payload: dict):
    headers = {
        "Authorization": f"Bearer {FACEBOOK_WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(FACEBOOK_WHATSAPP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
