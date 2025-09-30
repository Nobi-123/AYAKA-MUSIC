# SONALI/modules/chat_control.py
"""
Chat control module to enable/disable chatbot in specific chats.
"""

from config import BANNED_USERS
from pymongo import MongoClient
import config

# Connect to MongoDB
mongo_client = MongoClient(config.MONGO_DB_URI)
db = mongo_client["SONALI_DB"]
chat_collection = db["enabled_chats"]

async def is_chat_enabled(chat_id: int) -> bool:
    """Check if chatbot is enabled in a chat."""
    if chat_id in BANNED_USERS:
        return False
    return chat_collection.find_one({"chat_id": chat_id}) is not None

async def enable_chat(chat_id: int):
    """Enable chatbot in a chat."""
    if not await is_chat_enabled(chat_id):
        chat_collection.insert_one({"chat_id": chat_id})

async def disable_chat(chat_id: int):
    """Disable chatbot in a chat."""
    chat_collection.delete_one({"chat_id": chat_id})