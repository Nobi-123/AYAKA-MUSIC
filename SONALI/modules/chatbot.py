import aiohttp
import config

last_bot_message = {}

OWNER_USERNAME = config.OWNER_USERNAME

async def chat_and_respond(chat_id, message_text, user_id):
    """
    Sends user message to SambaNova API and returns text response.
    """
    headers = {"Authorization": f"Bearer {config.CHATBOT_API_KEY}"}
    data = {"input_text": message_text, "user_id": str(user_id)}

    async with aiohttp.ClientSession() as session:
        async with session.post(config.CHATBOT_API_URL, headers=headers, json=data) as resp:
            if resp.status == 200:
                response = await resp.json()
                bot_text = response.get("response", "Sorry, I didn't understand that 😅")
            else:
                bot_text = "Sorry, API is not responding 😢"

    last_bot_message[chat_id] = bot_text
    return bot_text, None  # audio handled separately by voice_manager