import os
import json

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user_memory(memory, user_id, telegram_name):
    uid = str(user_id)
    if uid not in memory:
        memory[uid] = {
            "history": [],
            "name": telegram_name,
            "mood": "",
            "likes": "",
            "last_seen": 0,
        }
    return memory[uid]
