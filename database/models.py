"""
Models untuk struktur data bot.
Saat ini menggunakan JSON file (bot_data.json).
Bisa diupgrade ke SQLite atau PostgreSQL di masa depan.
"""

# Struktur crypto alert
ALERT_SCHEMA = {
    "id": str,           # "alert_1"
    "coin": str,         # "BTC"
    "condition": str,    # ">" atau "<"
    "target": float,     # 70000.0
    "chat_id": int,      # Telegram chat ID
    "triggered": bool,   # Sudah dikirim atau belum
}

# Struktur habit
HABIT_SCHEMA = {
    "id": str,           # "habit_1"
    "name": str,         # "Olahraga"
    "time": str,         # "06:00"
    "chat_id": int,      # Telegram chat ID
    "streak": int,       # Jumlah hari berturut-turut
    "last_done": str,    # "2025-05-06" atau None
}

# Struktur scheduled post
SCHEDULED_POST_SCHEMA = {
    "id": str,           # "job_1"
    "time": str,         # "22:30"
    "text": str,         # Isi pesan
}
