import os
from dotenv import load_dotenv

# load .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")