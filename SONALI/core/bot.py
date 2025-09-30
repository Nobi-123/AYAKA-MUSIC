import asyncio
import random
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from modules.voice_manager import text_to_voice
from modules.chatbot import chat_and_respond, handle_voice_request
from modules.reactions import react_to_message, STICKERS
from modules.chat_control import is_chat_enabled, enable_chat, disable_chat

import config

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("RAUSHAN")

bot = Client(
    "SONALI",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    max_concurrent_transmissions=7,
)

# --------------------------
# Admin-only commands
# --------------------------
@bot.on_message(filters.command("enablechat") & filters.user(config.OWNER_ID))
async def enable_chat_cmd(client, message: Message):
    await enable_chat(message.chat.id)
    await message.reply_text("✅ Chatbot enabled in this chat.")

@bot.on_message(filters.command("disablechat") & filters.user(config.OWNER_ID))
async def disable_chat_cmd(client, message: Message):
    await disable_chat(message.chat.id)
    await message.reply_text("❌ Chatbot disabled in this chat.")

# --------------------------
# Handle all text messages
# --------------------------
@bot.on_message(filters.text)
async def human_chat(client, message: Message):
    chat_id = message.chat.id
    text = message.text

    if not await is_chat_enabled(chat_id):
        return

    # Mimic typing delay like human
    await asyncio.sleep(random.uniform(1.0, 2.5))

    # Check if user wants last bot message in voice
    audio_bytes = await handle_voice_request(chat_id, text)
    if audio_bytes:
        await message.reply_text("Yeh raha tumhara voice message 😘")
        await message.reply_voice(audio_bytes)
        return

    # Chatbot reply (fully human-like)
    bot_text, bot_audio = await chat_and_respond(chat_id, text, message.from_user.id)

    # Send reply text
    await message.reply_text(bot_text)

    # Send reply voice automatically
    if bot_audio:
        await message.reply_voice(bot_audio)

    # React to user message
    await react_to_message(message)

# --------------------------
# Sticker reply
# --------------------------
@bot.on_message(filters.sticker)
async def sticker_reply(client, message: Message):
    await message.reply_sticker(random.choice(STICKERS))
    await react_to_message(message)

# --------------------------
# Start bot
# --------------------------
if __name__ == "__main__":
    print("Starting fully human-like RAUSHAN Bot...")
    bot.run()