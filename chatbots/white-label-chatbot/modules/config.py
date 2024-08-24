import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


LUNARY_API_URL = os.environ.get("LUNARY_API_URL")
LUNARY_PUBLIC_KEY = os.environ.get("LUNARY_PUBLIC_KEY")


FACEBOOK_WHATSAPP_TOKEN = os.environ.get("FACEBOOK_WHATSAPP_TOKEN")
FACEBOOK_WEBHOOK_VERIFY_TOKEN = os.environ.get("FACEBOOK_WEBHOOK_VERIFY_TOKEN")
FACEBOOK_WHATSAPP_API_URL = os.environ.get("FACEBOOK_WHATSAPP_API_URL")


CHATBOT_DATABASE_URL = os.environ.get("CHATBOT_DATABASE_URL")

USE_PHONE_NUMBER_WHITELIST = os.environ.get("USE_PHONE_NUMBER_WHITELIST")