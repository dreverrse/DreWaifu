import json
import os
from datetime import datetime

NOTES_FILE = "notes.json"


def _load_notes():
    if not os.path.exists(NOTES_FILE):
        return {}
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def _save_notes(data):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_note(content, user_id=None):
    """Simpan catatan pribadi user."""
    notes = _load_notes()
    uid = str(user_id) if user_id else "global"

    if uid not in notes:
        notes[uid] = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    notes[uid].append({
        "time": timestamp,
        "content": content.strip(),
    })

    _save_notes(notes)
    return f"Catatan disimpan pada {timestamp}."


def read_note(_, user_id=None):
    """Baca semua catatan pribadi user."""
    notes = _load_notes()
    uid = str(user_id) if user_id else "global"

    user_notes = notes.get(uid, [])
    if not user_notes:
        return "Belum ada catatan tersimpan."

    result = f"Catatan kamu ({len(user_notes)} total):\n\n"
    for i, note in enumerate(user_notes[-10:], 1):
        result += f"{i}. [{note['time']}]\n{note['content']}\n\n"

    return result.strip()
