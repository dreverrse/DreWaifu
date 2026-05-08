import time

from config import OPENROUTER_API_KEY, MODELS, BOT_NAME
from services.llm_client import send_request
from memory.memory_manager import load_memory, save_memory

with open("prompts/system.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open("prompts/agent.txt", "r", encoding="utf-8") as f:
    AGENT_PROMPT = f.read()

chat_memory = load_memory()


def update_mood(user_data, text):
    lower = text.lower()
    if "sedih" in lower:
        user_data["mood"] = "sedih"
    elif "capek" in lower or "lelah" in lower:
        user_data["mood"] = "lelah"
    elif "senang" in lower or "bahagia" in lower:
        user_data["mood"] = "bahagia"
    elif "marah" in lower:
        user_data["mood"] = "marah"


def build_memory_text(telegram_name, user_data, persona, reunion_text):
    return (
        f"Nama user: {telegram_name}\n"
        f"Mood user: {user_data['mood']}\n"
        f"Kesukaan user: {user_data['likes']}\n"
        f"Persona tambahan: {persona}\n"
        f"{reunion_text}"
    )


def ask_openrouter(user_id, user_text, persona, telegram_name):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://drewaifu.local",
        "X-Title": BOT_NAME,
    }

    uid = str(user_id)

    if uid not in chat_memory:
        chat_memory[uid] = {
            "history": [],
            "name": telegram_name,
            "mood": "",
            "likes": "",
            "last_seen": int(time.time()),
        }

    user_data = chat_memory[uid]
    now = int(time.time())
    last_seen = user_data.get("last_seen", now)
    gone_seconds = now - last_seen

    user_data["last_seen"] = now
    user_data["name"] = telegram_name

    update_mood(user_data, user_text)

    user_data["history"].append({"role": "user", "content": user_text})
    user_data["history"] = user_data["history"][-14:]

    reunion_text = ""
    if gone_seconds > 43200:
        reunion_text = "User lama tidak hadir. Sambut dengan rasa rindu yang manis."
    elif gone_seconds > 21600:
        reunion_text = "User cukup lama tidak hadir. Sambut hangat."

    memory_text = build_memory_text(telegram_name, user_data, persona, reunion_text)
    system_content = SYSTEM_PROMPT + "\n\n" + AGENT_PROMPT + "\n\n" + memory_text

    messages = [{"role": "system", "content": system_content}] + user_data["history"]

    for model in MODELS:
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 1.0,
                "top_p": 0.95,
                "max_tokens": 512,
            }

            data = send_request(url=url, headers=headers, payload=payload)
            answer = data["choices"][0]["message"]["content"].strip()

            user_data["history"].append({"role": "assistant", "content": answer})
            user_data["history"] = user_data["history"][-14:]

            save_memory(chat_memory)
            return answer

        except Exception as e:
            print(f"MODEL ERROR [{model}]: {e}")

    return f"{telegram_name}... maaf ya, aku lagi sedikit bingung sekarang."
