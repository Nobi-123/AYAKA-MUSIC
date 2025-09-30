import asyncio
import random
import logging
from pyrogram import Client, filters, errors
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from modules.voice_manager import text_to_voice
from modules.chatbot import chat_and_respond, OWNER_USERNAME
from modules.reactions import react_to_message, STICKERS
from modules.chat_control import is_chat_enabled, enable_chat, disable_chat

import config

LOGGER = logging.getLogger("RAUSHAN")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# --------------------------
# RAUSHAN Bot Client
# --------------------------
class RAUSHAN(Client):
    def __init__(self):
        LOGGER.info("Starting Bot...")
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
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                     f"ɪᴅ : <code>{self.id}</code>\n"
                     f"ɴᴀᴍᴇ : {self.name}\n"
                     f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER.error("Bot cannot access the log group/channel. Add the bot there first.")
        except Exception as ex:
            LOGGER.error(f"Bot failed to access the log group/channel: {type(ex).__name__}")

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER.error("Promote the bot as an admin in your log group/channel.")

        LOGGER.info(f"Music & Chat Bot Started as {self.name}")

    async def stop(self):
        await super().stop()


bot = RAUSHAN()

# --------------------------
# Chatbot Enable / Disable
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
# Owner / Developer / Papa Keywords
# --------------------------
OWNER_KEYWORDS = [
    "owner", "developer", "father", "papa",
    "tere owner ka naam kya hai", "tera owner kaun hai",
    "owner ka naam kya hai", "apka owner kaun hai",
    "developer ka naam kya hai", "apka developer kaun hai",
    "papa ka naam kya hai", "father ka naam kya hai",
    "who is your owner", "who is your developer",
    "who is your papa", "who is your father"
]

VOICE_REQUEST_KEYWORDS = [
    "ye msg mujhe voice msg mai bhejo",
    "send this in voice",
    "voice me bhejo"
]


# --------------------------
# Handle Text Messages
# --------------------------
@bot.on_message(filters.text)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = message.text.lower()

    # Only respond if chatbot is enabled
    if not await is_chat_enabled(chat_id):
        return

    # Owner / Developer / Papa Replies
    if any(keyword in text for keyword in OWNER_KEYWORDS):
        reply_text = f"Mera owner hai {OWNER_USERNAME} ❤️"
        await message.reply_text(reply_text)
        audio_bytes = await text_to_voice(reply_text)
        if audio_bytes:
            await message.reply_voice(audio_bytes)
        return

    # Check for voice request keywords
    if any(k in text for k in VOICE_REQUEST_KEYWORDS):
        from modules.chatbot import last_bot_message
        last_text = last_bot_message.get(chat_id)
        if last_text:
            audio_bytes = await text_to_voice(last_text)
            await message.reply_text("Here's your message in voice 😘")
            if audio_bytes:
                await message.reply_voice(audio_bytes)
            return
        else:
            await message.reply_text("No previous message to convert to voice 😅")
            return

    # Chatbot reply (girlfriend-style Hinglish)
    bot_text, bot_audio = await chat_and_respond(chat_id, message.text, message.from_user.id)
    await message.reply_text(bot_text)
    if bot_audio:
        await message.reply_voice(bot_audio)

    # Automatic reactions
    await react_to_message(message)


# --------------------------
# Sticker Reply
# --------------------------
@bot.on_message(filters.sticker)
async def sticker_reply(client, message: Message):
    await message.reply_sticker(random.choice(STICKERS))
    await react_to_message(message)  # also run reactions for stickers


# --------------------------
# Music Commands Placeholder
# --------------------------
# Import your music player commands here if needed


# --------------------------
# Start Bot
# --------------------------
if __name__ == "__main__":
    print("Starting RAUSHAN Bot...")
    bot.run()