import time

from utils.helpers import is_owner
from services.openrouter import ask_openrouter
from handlers.commands import (
    list_cmd,
    help_cmd,
    persona_cmd,
    post_cmd,
    schedule_cmd,
    clearjob_cmd
)

COOLDOWN = 1
MISS_TIME = 21600

last_message_time = {}


async def ai_reply(update, context):
    msg = update.effective_message

    if not msg:
        return

    if not is_owner(update):
        return

    text = (msg.text or "").strip()

    if not text:
        return

    user = update.effective_user
    user_id = user.id

    telegram_name = user.first_name or user.full_name or "sayang"

    state = context.user_data.get("state")

    # ======================
    # SMART INPUT MODE
    # ======================

    if state == "waiting_post":
        context.args = text.split()
        await post_cmd(update, context)
        context.user_data["state"] = None
        return

    if state == "waiting_persona":
        context.args = text.split()
        await persona_cmd(update, context)
        context.user_data["state"] = None
        return

    if state == "waiting_schedule":
        parts = text.split()

        if len(parts) < 2:
            await msg.reply_text(
                "Format salah.\nContoh:\n22:30 Halo semua"
            )
            return

        context.args = parts
        await schedule_cmd(update, context)
        context.user_data["state"] = None
        return

    # ======================
    # BUTTON MENU
    # ======================

    if text == "💖 Ngobrol":
        await msg.reply_text(
            "Aku di sini sayang 💖 Mau cerita apa hari ini?"
        )
        return

    if text == "💕 Manja":
        await msg.reply_text(
            "Sini dekat aku dulu 🤍 Aku temenin."
        )
        return

    if text == "📤 Post Channel":
        context.user_data["state"] = "waiting_post"

        await msg.reply_text(
            "Tulis pesan yang ingin dikirim ke channel 💌"
        )
        return

    if text == "📅 Jadwal":
        context.user_data["state"] = "waiting_schedule"

        await msg.reply_text(
            "Kirim format:\n22:30 Halo semuanya"
        )
        return

    if text == "⚙️ Persona":
        context.user_data["state"] = "waiting_persona"

        await msg.reply_text(
            "Tulis persona baru 💖\nContoh:\nmanis, romantis, perhatian"
        )
        return

    if text == "📋 List Jadwal":
        await list_cmd(update, context)
        return

    if text == "🧹 Hapus Semua":
        await clearjob_cmd(update, context)
        return

    if text == "ℹ️ Bantuan":
        await help_cmd(update, context)
        return

    if text.startswith("/"):
        return

    # ======================
    # COOLDOWN
    # ======================

    now = time.time()

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
    # AI CHAT
    # ======================

    data = context.bot_data["data"]

    persona = data.get(
        "persona",
        "manis, romantis, lembut"
    )

    await context.bot.send_chat_action(
        chat_id=msg.chat_id,
        action="typing"
    )

    try:
        final_text = text

        if extra_context:
            final_text = extra_context + "\nPesan user: " + text

        answer = ask_openrouter(
            user_id=user_id,
            user_text=final_text,
            persona=persona,
            telegram_name=telegram_name
        )

        await msg.reply_text(answer)

    except Exception as e:
        await msg.reply_text(
            f"Aku bingung dulu ya {telegram_name}.\n{e}"
        )