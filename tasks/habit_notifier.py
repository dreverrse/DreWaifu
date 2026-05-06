"""
Habit Notifier Task
Cek habit tiap menit, kirim pengingat jika jam cocok.
"""

import logging
from datetime import datetime
from config import TZ
from utils.storage import load_data

logger = logging.getLogger(__name__)

# Simpan track notif yang sudah dikirim hari ini {user_id: {habit_id: date}}
_sent_today = {}


async def send_habit_reminders(context):
    now = datetime.now(TZ)
    current_hhmm = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    data = load_data()

    for user_id, habits in data["habits"].items():
        for habit in habits:
            if habit["time"] != current_hhmm:
                continue

            # Cek apakah sudah dikirim hari ini
            sent = _sent_today.get(user_id, {})
            if sent.get(habit["id"]) == today:
                continue

            streak = habit.get("streak", 0)
            fire = "🔥" * min(streak, 5) if streak > 0 else ""

            text = (
                f"⏰ Waktunya habit!\n\n"
                f"📌 {habit['name']}\n"
                f"🏅 Streak saat ini: {streak} hari {fire}\n\n"
                f"Setelah selesai, ketik:\n"
                f"/done {habit['id']}"
            )

            try:
                await context.bot.send_message(
                    chat_id=habit["chat_id"],
                    text=text,
                )
                if user_id not in _sent_today:
                    _sent_today[user_id] = {}
                _sent_today[user_id][habit["id"]] = today
                logger.info(f"Habit reminder dikirim: {habit['id']} ke {user_id}")
            except Exception as e:
                logger.error(f"Gagal kirim habit reminder ke {habit['chat_id']}: {e}")


def start_habit_notifier(job_queue):
    if not job_queue:
        logger.warning("JobQueue tidak aktif, habit notifier tidak bisa dijalankan.")
        return

    job_queue.run_repeating(
        send_habit_reminders,
        interval=60,
        first=10,
        name="habit_notifier",
    )
    logger.info("Habit notifier aktif, cek setiap 60 detik.")
