# SONALI/modules/chatbot.py
import aiohttp
import asyncio
import random
import config

# Store last bot message per chat
last_bot_message = {}
# Store last few user messages per chat to give context
chat_context = {}

# Small human-like fillers
HUMAN_FILLERS = [
    "Hmm…", "Let me see…", "Oh okay…", "Ah! I see…", "Interesting…", "Haha 😄"
]

OWNER_USERNAME = config.OWNER_USERNAME

async def chat_and_respond(chat_id, message_text, user_id):
    """
    Send user message to SambaNova API with context memory,
    add small human-like filler delays, and return bot response.
    """
    # Add user message to context
    if chat_id not in chat_context:
        chat_context[chat_id] = []
    chat_context[chat_id].append(f"User: {message_text}")
    # Keep only last 6 messages
    chat_context[chat_id] = chat_context[chat_id][-6:]

    # Random filler to feel human
    if random.random() < 0.3:
        filler = random.choice(HUMAN_FILLERS)
        await asyncio.sleep(random.uniform(0.5, 1.5))  # short pause
        filler_response = filler
    else:
        filler_response = ""

    # Build input for API including context
    api_input_text = "\n".join(chat_context[chat_id]) + f"\nBot:"

    headers = {"Authorization": f"Bearer {config.CHATBOT_API_KEY}"}
    data = {"input_text": api_input_text, "user_id": str(user_id)}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(config.CHATBOT_API_URL, headers=headers, json=data) as resp:
                if resp.status == 200:
                    response_json = await resp.json()
                    bot_text = response_json.get("response", "Sorry, I didn't understand 😅")
                else:
                    bot_text = "Hmm… API not responding 😢"
    except Exception:
        bot_text = "Oops… something went wrong 😔"

    # Append bot message to context
    chat_context[chat_id].append(f"Bot: {bot_text}")
    # Keep last 6 messages only
    chat_context[chat_id] = chat_context[chat_id][-6:]

    # Save last bot message
    last_bot_message[chat_id] = bot_text

    # Combine filler + actual bot text
    final_text = f"{filler_response} {bot_text}".strip()
    
    # Add small thinking delay
    await asyncio.sleep(random.uniform(0.8, 2.0))

    return final_text, None  # Audio handled separately in voice_manager