import asyncio
import random
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from modules.voice_manager import text_to_voice
from modules.chatbot import chat_and_respond, handle_voice_request, OWNER_USERNAME
from modules.reactions import react_to_message, STICKERS
from modules.chat_control import is_chat_enabled, enable_chat, disable_chat

import config

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("RAUSHAN")

# --------------------------
# RAUSHAN Bot Client
# --------------------------
bot = Client(
    "SONALI",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    max_concurrent_transmissions=7,
)

# --------------------------
# Admin-only Chat Control
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
# Handle Text Messages
# --------------------------
@bot.on_message(filters.text)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = message.text

    if not await is_chat_enabled(chat_id):
        return

    # --------------------------
    # Mimic human typing
    # --------------------------
    typing_time = random.uniform(1.0, 2.5)
    async with client.send_chat_action(chat_id, ChatAction.TYPING):
        await asyncio.sleep(typing_time)

    # --------------------------
    # Owner / Developer / Papa Replies
    # --------------------------
    owner_keywords = [
        "owner", "developer", "father", "papa",
        "tere owner ka naam kya hai", "tera owner kaun hai",
        "owner ka naam kya hai", "apka owner kaun hai",
        "developer ka naam kya hai", "apka developer kaun hai",
        "papa ka naam kya hai", "father ka naam kya hai",
        "who is your owner", "who is your developer",
        "who is your papa", "who is your father"
    ]
    if any(k in text.lower() for k in owner_keywords):
        reply_text = f"Mera owner hai {OWNER_USERNAME} ❤️"
        audio_bytes = await text_to_voice(reply_text)

        await message.reply_text(reply_text)
        if audio_bytes:
            async with client.send_chat_action(chat_id, ChatAction.RECORD_VOICE):
                await asyncio.sleep(min(typing_time, 1.5))
                await message.reply_voice(audio_bytes)
        return

    # --------------------------
    # Voice Request Check
    # --------------------------
    audio_bytes = await handle_voice_request(chat_id, text)
    if audio_bytes:
        await message.reply_text("Yeh raha tumhara voice message 😘")
        async with client.send_chat_action(chat_id, ChatAction.RECORD_VOICE):
            await asyncio.sleep(min(typing_time, 2))
            await message.reply_voice(audio_bytes)
        return

    # --------------------------
    # Human-like chatbot reply
    # --------------------------
    bot_text, bot_audio = await chat_and_respond(chat_id, text, message.from_user.id)

    # Send text reply with typing indicator
    async with client.send_chat_action(chat_id, ChatAction.TYPING):
        await asyncio.sleep(min(typing_time, 2))
        await message.reply_text(bot_text)

    # Send voice reply with recording indicator
    if bot_audio:
        async with client.send_chat_action(chat_id, ChatAction.RECORD_VOICE):
            await asyncio.sleep(min(typing_time, 2))
            await message.reply_voice(bot_audio)

    # --------------------------
    # Automatic reactions
    # --------------------------
    await react_to_message(message)

# --------------------------
# Sticker Reply
# --------------------------
@bot.on_message(filters.sticker)
async def sticker_reply(client, message: Message):
    await message.reply_sticker(random.choice(STICKERS))
    await react_to_message(message)

# --------------------------
# Start Bot
# --------------------------
if __name__ == "__main__":
    print("Starting fully human-like RAUSHAN Bot...")
    bot.run()