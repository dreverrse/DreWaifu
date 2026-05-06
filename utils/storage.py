import os
import json

DATA_FILE = "bot_data.json"

default_data = {
    "persona": "manis, setia, sopan, sedikit genit",
    "prefix": "Hai sayang",
    "scheduled_posts": [],
    "crypto_alerts": {},   # {user_id: [{coin, condition, target, chat_id}]}
    "habits": {},          # {user_id: [{id, name, time, chat_id, streak, last_done}]}
}


def save_data(payload):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(default_data)
        return default_data.copy()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Pastikan key baru ada (upgrade safe)
    for key, val in default_data.items():
        if key not in data:
            data[key] = val

    return data
