import os
import json

DATA_FILE = "bot_data.json"

default_data = {
    "persona": "manis, setia, sopan, sedikit genit",
    "prefix": "Hai sayang",
    "scheduled_posts": []
}

def save_data(payload):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(default_data)
        return default_data.copy()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)