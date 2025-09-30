import asyncio
import importlib
from pyrogram import idle

from SONALI import LOGGER, app, userbot
from SONALI.core.bot import RAUSHAN
from SONALI.misc import sudo
from SONALI.plugins import ALL_MODULES
from SONALI.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # --------------------------
    # Check for String Sessions
    # --------------------------
    if not any([getattr(__import__("config"), f"STRING{i}") for i in range(1, 6)]):
        LOGGER("SONALI").error(
            "𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 V2 𝐒𝐞𝐬𝐬𝐢𝐨𝐧!"
        )

    # --------------------------
    # Load Sudo Users
    # --------------------------
    await sudo()

    # --------------------------
    # Load Banned Users
    # --------------------------
    try:
        gbanned_users = await get_gbanned()
        for user_id in gbanned_users:
            BANNED_USERS.add(user_id)

        banned_users = await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # --------------------------
    # Start Core App & Userbot
    # --------------------------
    await app.start()
    await userbot.start()

    # --------------------------
    # Load All Plugins
    # --------------------------
    for module in ALL_MODULES:
        importlib.import_module(f"SONALI.plugins.{module}")

    LOGGER("SONALI.plugins").info("✅ All features loaded successfully!")

    # --------------------------
    # Start RAUSHAN bot
    # --------------------------
    await RAUSHAN.start()
    if hasattr(RAUSHAN, "decorators"):
        await RAUSHAN.decorators()

    LOGGER("SONALI").info("╔═════ஜ۩۞۩ஜ════╗\n  ♨️ MADE BY ALPHA ♨️\n╚═════ஜ۩۞۩ஜ════╝")

    # --------------------------
    # Idle Mode
    # --------------------------
    await idle()

    # --------------------------
    # Shutdown
    # --------------------------
    await app.stop()
    await userbot.stop()
    LOGGER("SONALI").info("Bot stopped successfully.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())