# Helper untuk kirim pesan langsung via Telegram Bot API (tanpa context)
import requests
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text, parse_mode="HTML"):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"TELEGRAM SEND ERROR: {e}")
        return None
