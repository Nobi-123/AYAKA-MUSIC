# bot.py
import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from logging import getLogger

import config
from modules.voice_manager import text_to_voice
from modules.chatbot import samba_chat_reply
from modules.reactions import get_reaction
from modules.stickers import STICKERS
from utils.helpers import is_chat_enabled, enable_chat, disable_chat

from pyrogram import Client, errors

LOGGER = getLogger("RAUSHAN")

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
            LOGGER.error(
                "Bot failed to access the log group/channel. "
                "Make sure you have added your bot to the log group/channel."
            )
        except Exception as ex:
            LOGGER.error(
                f"Bot failed to access the log group/channel.\nReason: {type(ex).__name__}."
            )

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER.error(
                "Please promote your bot as an admin in your log group/channel."
            )

        LOGGER.info(f"Music Bot Started as {self.name}")

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

# --------------------------
# Handle Messages
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
        reply_text = f"Mera owner hai {config.OWNER_USERNAME} ❤️"
        await message.reply_text(reply_text)
        audio_bytes = await text_to_voice(reply_text)
        if audio_bytes:
            await message.reply_voice(audio_bytes)
        return

    # SambaNova Chatbot Reply
    reply_text = await samba_chat_reply(message.text, chat_id)
    await message.reply_text(reply_text)
    audio_bytes = await text_to_voice(reply_text)
    if audio_bytes:
        await message.reply_voice(audio_bytes)

    # Reactions
    reaction = await get_reaction(reply_text)
    if reaction:
        await message.reply_text(reaction)

# --------------------------
# Sticker Reply
# --------------------------
@bot.on_message(filters.sticker)
async def sticker_reply(client, message: Message):
    await message.reply_sticker(random.choice(STICKERS))

# --------------------------
# Music Commands Placeholder
# --------------------------
# You can import your music player modules here, e.g.,
# from music.player import play, pause, skip

# --------------------------
# Start Bot
# --------------------------
if __name__ == "__main__":
    print("Starting RAUSHAN Bot...")
    bot.run()