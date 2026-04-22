from datetime import datetime
from zoneinfo import ZoneInfo
from handlers.buttons import main_menu
from telegram.constants import ParseMode

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from utils.storage import save_data
from utils.helpers import (
    is_owner,
    format_channel_text,
    next_job_id
)

from handlers.scheduler import add_daily_job
from config import CHANNEL_ID, BOT_NAME

TZ = ZoneInfo("Asia/Jakarta")


# ======================
# START PREMIUM
# ======================

async def start(update, context):
    msg = update.effective_message
    user = update.effective_user

    data = context.bot_data["data"]

    name = user.first_name or user.full_name or "sayang"

    hour = datetime.now(TZ).hour

    if 4 <= hour < 11:
        greet = "Selamat pagi"
        mood = "Semoga harimu menyenangkan ☀️"

    elif 11 <= hour < 15:
        greet = "Selamat siang"
        mood = "Jangan lupa makan ya 🍱"

    elif 15 <= hour < 18:
        greet = "Selamat sore"
        mood = "Kalau capek, cerita ke aku 🌤️"

    else:
        greet = "Selamat malam"
        mood = "Aku siap nemenin kamu malam ini 🌙"

    text = f"""
{greet}, {name} 💖

Aku {BOT_NAME}
Senang kamu datang lagi.

{mood}

Persona saat ini:
{data['persona']}

Silakan pilih menu di bawah ya ✨
"""

    await msg.reply_text(
        text.strip(),
        reply_markup=main_menu()
    )


# ======================
# HELP
# ======================

async def help_cmd(update, context):
    await update.message.reply_text(
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/persona teks - Ubah sifat bot\n"
        "/post teks - Kirim ke channel\n"
        "/schedule HH:MM teks - Jadwal post\n"
        "/list - Lihat jadwal\n"
        "/del ID - Hapus jadwal\n"
        "/clearjob - Hapus semua jadwal"
    )


# ======================
# PERSONA
# ======================

async def persona_cmd(update, context):
    if not is_owner(update):
        return

    text = " ".join(context.args).strip()

    if not text:
        await update.message.reply_text(
            "Contoh:\n/persona manis, romantis, perhatian"
        )
        return

    data = context.bot_data["data"]
    data["persona"] = text

    save_data(data)

    await update.message.reply_text(
        "Persona berhasil diubah 💖"
    )


# ======================
# POST CHANNEL
# ======================

async def post_cmd(update, context):
    if not is_owner(update):
        return

    text = " ".join(context.args).strip()

    if not text:
        await update.message.reply_text(
            "Contoh:\n/post Halo semuanya"
        )
        return

    data = context.bot_data["data"]

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=format_channel_text(data, text),
        parse_mode=ParseMode.HTML
    )

    await update.message.reply_text(
        "Pesan berhasil dikirim."
    )


# ======================
# SCHEDULE PRO
# ======================

async def schedule_cmd(update, context):
    if not is_owner(update):
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Contoh:\n/schedule 08:30 Selamat pagi"
        )
        return

    hhmm = context.args[0]
    text = " ".join(context.args[1:]).strip()

    try:
        hour, minute = map(int, hhmm.split(":"))

        if hour < 0 or hour > 23:
            raise ValueError

        if minute < 0 or minute > 59:
            raise ValueError

    except:
        await update.message.reply_text(
            "Format waktu salah. Gunakan HH:MM"
        )
        return

    data = context.bot_data["data"]

    for item in data["scheduled_posts"]:
        if item["time"] == hhmm and item["text"].lower() == text.lower():
            await update.message.reply_text(
                "Jadwal sama sudah ada."
            )
            return

    job_id = next_job_id(data)

    data["scheduled_posts"].append({
        "id": job_id,
        "time": hhmm,
        "text": text
    })

    save_data(data)

    add_daily_job(
        context.job_queue,
        job_id,
        hhmm,
        text
    )

    await update.message.reply_text(
        f"✅ Jadwal ditambahkan\n"
        f"ID: {job_id}\n"
        f"Jam: {hhmm}"
    )


# ======================
# LIST PREMIUM
# ======================

async def list_cmd(update, context):
    data = context.bot_data["data"]

    jobs = data["scheduled_posts"]

    if not jobs:
        await update.message.reply_text("Tidak ada jadwal.")
        return

    jobs = sorted(jobs, key=lambda x: x["time"])

    txt = "📅 Jadwal Aktif\n\n"

    for x in jobs:
        txt += (
            f"🆔 {x['id']}\n"
            f"🕒 {x['time']}\n"
            f"💬 {x['text']}\n\n"
        )

    await update.message.reply_text(txt)


# ======================
# DELETE JOB
# ======================

async def del_cmd(update, context):
    if not is_owner(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Contoh:\n/del job_1"
        )
        return

    job_id = context.args[0]

    data = context.bot_data["data"]

    before = len(data["scheduled_posts"])

    data["scheduled_posts"] = [
        x for x in data["scheduled_posts"]
        if x["id"] != job_id
    ]

    for job in context.job_queue.get_jobs_by_name(job_id):
        job.schedule_removal()

    save_data(data)

    after = len(data["scheduled_posts"])

    if before == after:
        await update.message.reply_text(
            "ID tidak ditemukan."
        )
    else:
        await update.message.reply_text(
            f"🗑 {job_id} dihapus."
        )

# ======================
# ABOUT DEV
# ======================

async def dev_cmd(update, context):
    text = """
About Developer

Hai👋 im @dreverrse,
This bot build with Python + Telegram API and AI Open Router.

"""

    keyboard = [
        [
            InlineKeyboardButton(
                "GitHub",
                url="https://github.com/dreverrse"
            ),
            InlineKeyboardButton(
                "Instagram",
                url="https://instagram.com/dreverrse"
            )
        ]
    ]

    await update.message.reply_text(
        text.strip(),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ======================
# CLEAR ALL JOBS
# ======================

async def clearjob_cmd(update, context):
    if not is_owner(update):
        return

    data = context.bot_data["data"]

    data["scheduled_posts"] = []

    for job in context.job_queue.jobs():
        job.schedule_removal()

    save_data(data)

    await update.message.reply_text(
        "🧹 Semua jadwal dihapus."
    )
    
    