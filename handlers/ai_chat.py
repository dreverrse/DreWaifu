import time
import traceback
from datetime import datetime
from config import TZ
from core.tool_executor import execute_tool
from core.react_agent import run_agent
from utils.markdown import safe_markdown

from utils.helpers import is_owner
from utils.message_formatter import split_message

from services.openrouter import ask_openrouter

from handlers.commands import (
    list_cmd,
    help_cmd,
    persona_cmd,
    post_cmd,
    schedule_cmd,
    clearjob_cmd,
)

COOLDOWN = 1
MISS_TIME = 21600
DAILY_LIMIT = 20

last_message_time = {}
daily_count = {}  # {user_id: {"date": "2025-05-06", "count": 0}}

ALL_BUTTONS = [
    "💖 Ngobrol", "💕 Manja", "ℹ️ Bantuan",
    "🪙 Cek Harga", "📊 Alert Crypto", "💪 Habit",
    "✅ Selesai Habit", "📤 Post Channel", "📅 Jadwal",
    "⚙️ Persona", "📋 List Jadwal", "🧹 Hapus Semua",
]


async def ai_reply(update, context):
    msg = update.effective_message

    if not msg or not msg.text:
        return

    text = msg.text.strip()
    if not text:
        return

    user = update.effective_user
    user_id = user.id
    telegram_name = user.first_name or user.full_name or "sayang"

    now = time.time()

    # ======================
    # STATE HANDLING
    # ======================

    state = context.user_data.get("state")

    # Reset state jika user tekan tombol menu lain
    if state and text in ALL_BUTTONS:
        context.user_data["state"] = None
        state = None

    if state:
        if not is_owner(update):
            await deny_access(msg, context)
            return

        if state == "waiting_post":
            context.args = text.split()
            await post_cmd(update, context)

        elif state == "waiting_persona":
            context.args = text.split()
            await persona_cmd(update, context)

        elif state == "waiting_schedule":
            parts = text.split()
            if len(parts) < 2:
                await msg.reply_text("Format salah.\nContoh:\n22:30 Halo semua")
                return
            context.args = parts
            await schedule_cmd(update, context)

        elif state == "waiting_addalert":
            context.args = text.split()
            from handlers.crypto import add_alert_cmd
            await add_alert_cmd(update, context)

        elif state == "waiting_addhabit":
            context.args = text.split()
            from handlers.habit import add_habit_cmd
            await add_habit_cmd(update, context)

        elif state == "waiting_done":
            context.args = text.split()
            from handlers.habit import done_habit_cmd
            await done_habit_cmd(update, context)

        context.user_data["state"] = None
        return

    # ======================
    # PUBLIC MENU
    # ======================

    if text == "💖 Ngobrol":
        await msg.reply_text("Aku di sini sayang 💖 Mau cerita apa hari ini?")
        return

    if text == "💕 Manja":
        await msg.reply_text("Sini dekat aku dulu 🤍 Aku temenin.")
        return

    if text == "ℹ️ Bantuan":
        await help_cmd(update, context)
        return

    if text == "🪙 Cek Harga":
        await msg.reply_text(
            "Mau cek harga coin apa?\n"
            "Ketik: /price BTC\n"
            "atau /price ETH, /price SOL, dll."
        )
        return

    if text == "📊 Alert Crypto":
        await msg.reply_text(
            "Mau set alert harga crypto?\n\n"
            "Format:\n"
            "/addalert BTC > 70000\n"
            "/addalert ETH < 2000\n\n"
            "Lihat alert: /listalert\n"
            "Hapus alert: /delalert alert_1"
        )
        return

    if text == "💪 Habit":
        await msg.reply_text(
            "Mau tambah habit harian?\n\n"
            "Format:\n"
            "/addhabit Olahraga 06:00\n"
            "/addhabit Baca buku 21:30\n\n"
            "Lihat habit: /listhabit\n"
            "Hapus habit: /delhabit habit_1"
        )
        return

    if text == "✅ Selesai Habit":
        context.user_data["state"] = "waiting_done"
        await msg.reply_text(
            "Habit mana yang sudah selesai?\n"
            "Kirim ID-nya, contoh: habit_1\n\n"
            "Atau ketik /listhabit untuk lihat ID."
        )
        return

    # ======================
    # ADMIN MENU
    # ======================

    admin_buttons = {
        "📤 Post Channel": (
            "waiting_post",
            "Tulis pesan yang ingin dikirim ke channel 💌",
        ),
        "📅 Jadwal": (
            "waiting_schedule",
            "Kirim format:\n22:30 Halo semuanya",
        ),
        "⚙️ Persona": (
            "waiting_persona",
            "Tulis persona baru 💖\nContoh:\nmanis, romantis, perhatian",
        ),
        "📋 List Jadwal": list_cmd,
        "🧹 Hapus Semua": clearjob_cmd,
    }

    if text in admin_buttons:
        if not is_owner(update):
            await deny_access(msg, context)
            return

        action = admin_buttons[text]

        if isinstance(action, tuple):
            state_key, reply_text = action
            context.user_data["state"] = state_key
            await msg.reply_text(reply_text)
        else:
            await action(update, context)

        return

    # ======================
    # SLASH FILTER
    # ======================

    if text.startswith("/"):
        return

    # ======================
    # COOLDOWN
    # ======================

    if user_id in last_message_time:
        diff = now - last_message_time[user_id]
        if diff < COOLDOWN:
            return

    extra_context = ""

    if user_id in last_message_time:
        gone = now - last_message_time[user_id]
        if gone > MISS_TIME:
            extra_context = (
                "User sudah lama tidak chat. "
                "Tunjukkan rasa rindu dan hangat."
            )

    last_message_time[user_id] = now

    # ======================
    # DAILY LIMIT
    # ======================

    today = datetime.now(TZ).strftime("%Y-%m-%d")

    if user_id not in daily_count:
        daily_count[user_id] = {"date": today, "count": 0}

    if daily_count[user_id]["date"] != today:
        daily_count[user_id] = {"date": today, "count": 0}

    if daily_count[user_id]["count"] >= DAILY_LIMIT:
        await msg.reply_text(
            "Aku udah banyak ngobrol hari ini sayang 🥺\n"
            "Besok kita lanjut ya 💖"
        )
        return

    daily_count[user_id]["count"] += 1

    # ======================
    # AI AGENT (ReAct Loop)
    # ======================

    data = context.bot_data.get("data", {})
    persona = data.get("persona", "manis, romantis, lembut")

    await context.bot.send_chat_action(chat_id=msg.chat_id, action="typing")

    try:
        user_input = text
        if extra_context:
            user_input = f"{extra_context}\nPesan user: {text}"

        answer = run_agent(
            ask_fn=ask_openrouter,
            user_id=user_id,
            user_text=user_input,
            persona=persona,
            telegram_name=telegram_name,
        )

        messages = split_message(answer)

        for part in messages:
            try:
                await msg.reply_text(safe_markdown(part), parse_mode="MarkdownV2")
            except Exception:
                await msg.reply_text(part)

    except Exception as e:
        traceback.print_exc()
        await msg.reply_text(f"ERROR:\n{e}")


async def deny_access(msg, context):
    context.user_data["state"] = None
    await msg.reply_text("Fitur ini khusus admin ya 💖")
