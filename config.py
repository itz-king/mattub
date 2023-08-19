import os
from dotenv import load_dotenv

load_dotenv(".env")

API_ID=os.environ.get("API_ID")
API_HASH=os.environ.get("API_HASH")
BOT_TOKEN=os.environ.get("BOT_TOKEN")
DATABASE_URL=os.environ.get("DATABASE_URL")
OWNER=int(os.environ.get("OWNER"))
HNDLR=os.environ.get('HANDLERS')