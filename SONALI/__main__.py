# SONALI/__main__.py

import asyncio
import importlib
from pyrogram import idle

from SONALI import LOGGER
from SONALI.core.bot import RAUSHAN
from SONALI.core.userbot import Userbot
from SONALI.core.dir import dirr
from SONALI.core.git import git
from SONALI.misc import sudo, dbb, heroku
from SONALI.plugins import ALL_MODULES
from SONALI.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


# Create instances here, not in __init__.py
app = RAUSHAN()
userbot = Userbot()

async def init():
    # Setup directories and misc services
    dirr()
    git()
    dbb()
    heroku()

    # --------------------------
    # Check for String Sessions
    # --------------------------
    if not any([getattr(__import__("config"), f"STRING{i}") for i in range(1, 6)]):
        LOGGER("SONALI").error(
            "String session not filled, please add at least one Pyrogram V2 session."
        )

    # Load Sudo Users
    await sudo()

    # Load Banned Users
    try:
        gbanned_users = await get_gbanned()
        for user_id in gbanned_users:
            BANNED_USERS.add(user_id)

        banned_users = await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # Start Core App & Userbot
    await app.start()
    await userbot.start()

    # Load All Plugins
    for module in ALL_MODULES:
        importlib.import_module(f"SONALI.plugins.{module}")
    LOGGER("SONALI.plugins").info("✅ All features loaded successfully!")

    # Start RAUSHAN bot
    await RAUSHAN.start()
    if hasattr(RAUSHAN, "decorators"):
        await RAUSHAN.decorators()

    LOGGER("SONALI").info("Bot is running...")

    # Idle Mode
    await idle()

    # Shutdown
    await app.stop()
    await userbot.stop()
    LOGGER("SONALI").info("Bot stopped successfully.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
