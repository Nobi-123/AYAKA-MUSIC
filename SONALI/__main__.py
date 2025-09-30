import asyncio
import importlib
from pyrogram import idle

import config
from SONALI import LOGGER, app, userbot
from SONALI.core.call import RAUSHAN
from SONALI.misc import sudo
from SONALI.plugins import ALL_MODULES
from SONALI.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # Check if at least one string session is provided
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER("SONALI").error(
            "String Sessions not provided! Please fill at least one Pyrogram v2 string session."
        )
        return

    # Initialize sudo users
    await sudo()

    # Load banned users from DB
    try:
        gbanned_users = await get_gbanned()
        banned_users = await get_banned_users()
        for user_id in gbanned_users + banned_users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("SONALI").warning(f"Failed to load banned users: {e}")

    # Start main bot
    await app.start()

    # Load all plugin modules
    for module in ALL_MODULES:
        importlib.import_module("SONALI.plugins." + module)
    LOGGER("SONALI.plugins").info("All features loaded successfully 🎉")

    # Start userbot
    await userbot.start()

    # Start music client
    await RAUSHAN.start()
    await RAUSHAN.decorators()  # if any decorators or setup functions are needed

    LOGGER("SONALI").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ♨️ MADE BYE TNC ♨️\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Keep the bot running
    await idle()

    # Stop everything gracefully on exit
    await app.stop()
    await userbot.stop()
    LOGGER("SONALI").info("Bot stopped successfully.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())