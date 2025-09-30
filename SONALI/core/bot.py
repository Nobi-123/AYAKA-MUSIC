# SONALI/bot.py
import asyncio
import random
import logging
from pyrogram import Client, filters, errors
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

import config
from modules.voice_manager import text_to_voice
from modules.chatbot import chat_and_respond, OWNER_USERNAME
from modules.reactions import react_to_message
from modules.stickers import get_context_sticker
from modules.chat_control import is_chat_enabled, enable_chat, disable_chat

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger("RAUSHAN")


# --------------------------
# RAUSHAN Bot Client
# --------------------------
class RAUSHAN(Client):
    def __init__(self):
        LOGGER.info("Starting SONALI Bot...")
        super().__init__(
            "SONALI",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<b>» {self.mention} Bot Started</b>\nID: <code>{self.id}</code>\nUsername: @{self.username}"
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER.error("Bot cannot access the log group/channel. Add the bot there first.")
        except Exception as ex:
            LOGGER.error(f"Bot failed to access log group: {type(ex).__name__}")

        LOGGER.info(f"SONALI Bot Started as {self.name}")

    async def stop(self):
        await super().stop()


bot = RAUSHAN()


# --------------------------
# Chatbot Enable / Disable (Admins Only)
# --------------------------
@bot.on_message(filters.command("enablechat") & filters.group)
async def enable_chat_cmd(client, message: Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await enable_chat(message.chat.id)
        await message.reply_text("✅ Chatbot enabled in this chat.")
    else:
        await message.reply_text("❌ Only admins can enable the chatbot.")


@bot.on_message(filters.command("disablechat") & filters.group)
async def disable_chat_cmd(client, message: Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await disable_chat(message.chat.id)
        await message.reply_text("❌ Chatbot disabled in this chat.")
    else:
        await message.reply_text("❌ Only admins can disable the chatbot.")


# --------------------------
# Owner / Developer / Papa Keywords
# --------------------------
OWNER_KEYWORDS = [
    "owner", "developer", "father", "papa",
    "tera owner kaun hai", "owner ka naam kya hai",
    "developer ka naam kya hai", "papa ka naam kya hai",
    "who is your owner", "who is your developer",
]

VOICE_REQUEST_KEYWORDS = [
    "ye msg mujhe voice msg mai bhejo",
    "send this in voice",
    "voice me bhejo"
]


# --------------------------
# Human-like typing + voice simulation
# --------------------------
async def human_reply(message: Message, bot_text: str, audio_bytes: bytes = None):
    """Simulate human typing and recording before sending reply."""
    typing_time = min(max(len(bot_text) * 0.05, 1), 5)  # 1-5 sec delay
    try:
        await message.chat.send_chat_action("typing")
        await asyncio.sleep(typing_time)
        await message.reply_text(bot_text)
    except Exception:
        await message.reply_text(bot_text)

    if audio_bytes:
        try:
            await message.chat.send_chat_action("record_audio")
            await asyncio.sleep(typing_time)
            await message.reply_voice(audio_bytes)
        except Exception:
            await message.reply_voice(audio_bytes)


# --------------------------
# Handle Text Messages
# --------------------------
@bot.on_message(filters.text)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = message.text.lower()

    if not await is_chat_enabled(chat_id):
        return

    # Owner replies
    if any(k in text for k in OWNER_KEYWORDS):
        reply_text = f"Mera owner hai {OWNER_USERNAME} ❤️"
        audio_bytes = await text_to_voice(reply_text)
        await human_reply(message, reply_text, audio_bytes)
        return

    # Voice request
    if any(k in text for k in VOICE_REQUEST_KEYWORDS):
        from modules.chatbot import last_bot_message
        last_text = last_bot_message.get(chat_id)
        if last_text:
            audio_bytes = await text_to_voice(last_text)
            await message.reply_text("Here's your message in voice 😘")
            if audio_bytes:
                await message.reply_voice(audio_bytes)
        else:
            await message.reply_text("No previous message to convert to voice 😅")
        return

    # Chatbot reply
    bot_text, _ = await chat_and_respond(chat_id, message.text, message.from_user.id)
    audio_bytes = await text_to_voice(bot_text)
    await human_reply(message, bot_text, audio_bytes)

    # Automatic reactions
    await react_to_message(message)


# --------------------------
# Sticker Reply
# --------------------------
@bot.on_message(filters.sticker)
async def sticker_reply(client, message: Message):
    sticker_id = get_context_sticker(message.text or "")
    await message.reply_sticker(sticker_id)
    await react_to_message(message)


# --------------------------
# Start Bot
# --------------------------
if __name__ == "__main__":
    print("Starting SONALI Bot...")
    bot.run()