"""
Habit Reminder Handler
Commands:
  /addhabit Olahraga 06:00   - tambah habit harian jam 06:00
  /listhabit                 - lihat semua habit
  /delhabit habit_1          - hapus habit
  /done habit_1              - tandai habit selesai hari ini
"""

from datetime import datetime, time
from zoneinfo import ZoneInfo
from utils.storage import save_data, load_data
from utils.helpers import next_habit_id
from config import TZ

DAYS_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


async def add_habit_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)
    chat_id = msg.chat_id

    if len(context.args) < 2:
        await msg.reply_text(
            "Format: /addhabit NAMA JAM\n"
            "Contoh:\n"
            "/addhabit Olahraga 06:00\n"
            "/addhabit Baca buku 21:00"
        )
        return

    hhmm = context.args[-1]
    name = " ".join(context.args[:-1])

    try:
        hour, minute = map(int, hhmm.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except ValueError:
        await msg.reply_text("Format waktu salah. Gunakan HH:MM contoh: 06:30")
        return

    data = load_data()
    if user_id not in data["habits"]:
        data["habits"][user_id] = []

    habit_id = next_habit_id(data["habits"][user_id])

    data["habits"][user_id].append({
        "id": habit_id,
        "name": name,
        "time": hhmm,
        "chat_id": chat_id,
        "streak": 0,
        "last_done": None,
    })

    save_data(data)

    await msg.reply_text(
        f"✅ Habit ditambahkan!\n"
        f"📌 {name}\n"
        f"⏰ Pengingat setiap hari jam {hhmm}\n"
        f"🆔 {habit_id}\n\n"
        f"Aku akan ingatkan kamu ya 💪"
    )


async def list_habit_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)

    data = load_data()
    habits = data["habits"].get(user_id, [])

    if not habits:
        await msg.reply_text("Belum ada habit yang terdaftar.\nGunakan /addhabit untuk menambah.")
        return

    text = "📋 Habit Kamu\n\n"
    for h in habits:
        streak = h.get("streak", 0)
        fire = "🔥" * min(streak, 5) if streak > 0 else ""
        text += (
            f"🆔 {h['id']}\n"
            f"📌 {h['name']}\n"
            f"⏰ {h['time']}\n"
            f"🏅 Streak: {streak} hari {fire}\n\n"
        )

    await msg.reply_text(text.strip())


async def del_habit_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)

    if not context.args:
        await msg.reply_text("Contoh: /delhabit habit_1")
        return

    habit_id = context.args[0]
    data = load_data()
    habits = data["habits"].get(user_id, [])
    before = len(habits)
    data["habits"][user_id] = [h for h in habits if h["id"] != habit_id]
    save_data(data)

    if len(data["habits"][user_id]) < before:
        await msg.reply_text(f"🗑 Habit {habit_id} dihapus.")
    else:
        await msg.reply_text("ID tidak ditemukan.")


async def done_habit_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)

    if not context.args:
        await msg.reply_text("Contoh: /done habit_1")
        return

    habit_id = context.args[0]
    today = datetime.now(TZ).strftime("%Y-%m-%d")

    data = load_data()
    habits = data["habits"].get(user_id, [])
    found = False

    for h in habits:
        if h["id"] == habit_id:
            found = True
            if h.get("last_done") == today:
                await msg.reply_text(
                    f"Kamu sudah tandai '{h['name']}' selesai hari ini 🎉\n"
                    f"Streak: {h['streak']} hari 🔥"
                )
                return

            # Cek apakah kemarin juga done (streak tidak putus)
            from datetime import timedelta
            yesterday = (datetime.now(TZ) - timedelta(days=1)).strftime("%Y-%m-%d")
            if h.get("last_done") == yesterday:
                h["streak"] = h.get("streak", 0) + 1
            else:
                h["streak"] = 1

            h["last_done"] = today
            break

    if not found:
        await msg.reply_text("Habit ID tidak ditemukan.")
        return

    save_data(data)
    streak = next(h["streak"] for h in data["habits"][user_id] if h["id"] == habit_id)
    fire = "🔥" * min(streak, 5)

    await msg.reply_text(
        f"✅ Mantap! Habit selesai!\n"
        f"📌 {next(h['name'] for h in data['habits'][user_id] if h['id'] == habit_id)}\n"
        f"🏅 Streak: {streak} hari {fire}"
    )
