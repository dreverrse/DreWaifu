import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
BOT_NAME = os.getenv("BOT_NAME", "DreWaifu")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

TZ = ZoneInfo("Asia/Jakarta")

MODELS = [
    "openai/gpt-4o-mini",
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemma-2-9b-it:free",
    "mistralai/mistral-7b-instruct:free",
]

# Interval cek harga crypto (detik)
CRYPTO_CHECK_INTERVAL = 300  # 5 menit
