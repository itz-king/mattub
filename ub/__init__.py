from telethon.sync import TelegramClient
from config import API_ID , API_HASH , BOT_TOKEN

ultroid=TelegramClient('ult',api_id=API_ID,api_hash=API_HASH).start(bot_token=BOT_TOKEN)