import time
import traceback

from core.tool_executor import execute_tool
from core.tool_parser import parse_tool_call

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

last_message_time = {}


async def ai_reply(update, context):

    msg = update.effective_message

    if not msg or not msg.text:
        return

    text = msg.text.strip()

    if not text:
        return

    user = update.effective_user

    user_id = user.id

    telegram_name = (
        user.first_name
        or user.full_name
        or "sayang"
    )

    now = time.time()

    # ======================
    # STATE HANDLING
    # ======================

    state = context.user_data.get("state")

    if state:

        if not is_owner(update):

            await deny_access(
                msg,
                context,
            )

            return

        if state == "waiting_post":

            context.args = text.split()

            await post_cmd(
                update,
                context,
            )

        elif state == "waiting_persona":

            context.args = text.split()

            await persona_cmd(
                update,
                context,
            )

        elif state == "waiting_schedule":

            parts = text.split()

            if len(parts) < 2:

                await msg.reply_text(
                    "Format salah.\n"
                    "Contoh:\n"
                    "22:30 Halo semua"
                )

                return

            context.args = parts

            await schedule_cmd(
                update,
                context,
            )

        context.user_data["state"] = None

        return

    # ======================
    # TOOL COMMAND
    # ======================

    if text.startswith("/read "):

        url = text.replace(
            "/read ",
            ""
        ).strip()

        result = execute_tool(
            "web_search",
            url,
        )

        await msg.reply_text(
            result[:4000]
        )

        return

    # ======================
    # PUBLIC MENU
    # ======================

    if text == "💖 Ngobrol":

        await msg.reply_text(
            "Aku di sini sayang 💖 "
            "Mau cerita apa hari ini?"
        )

        return

    if text == "💕 Manja":

        await msg.reply_text(
            "Sini dekat aku dulu 🤍 "
            "Aku temenin."
        )

        return

    if text == "ℹ️ Bantuan":

        await help_cmd(
            update,
            context,
        )

        return

    # ======================
    # ADMIN MENU
    # ======================

    admin_buttons = {

        "📤 Post Channel": (
            "waiting_post",
            "Tulis pesan yang ingin "
            "dikirim ke channel 💌",
        ),

        "📅 Jadwal": (
            "waiting_schedule",
            "Kirim format:\n"
            "22:30 Halo semuanya",
        ),

        "⚙️ Persona": (
            "waiting_persona",
            "Tulis persona baru 💖\n"
            "Contoh:\n"
            "manis, romantis, perhatian",
        ),

        "📋 List Jadwal":
            list_cmd,

        "🧹 Hapus Semua":
            clearjob_cmd,
    }

    if text in admin_buttons:

        if not is_owner(update):

            await deny_access(
                msg,
                context,
            )

            return

        action = admin_buttons[text]

        if isinstance(action, tuple):

            state_key, reply_text = action

            context.user_data["state"] = (
                state_key
            )

            await msg.reply_text(
                reply_text
            )

        else:

            await action(
                update,
                context,
            )

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

        diff = (
            now
            - last_message_time[user_id]
        )

        if diff < COOLDOWN:
            return

    extra_context = ""

    if user_id in last_message_time:

        gone = (
            now
            - last_message_time[user_id]
        )

        if gone > MISS_TIME:

            extra_context = (
                "User sudah lama "
                "tidak chat. "
                "Tunjukkan rasa "
                "rindu dan hangat."
            )

    last_message_time[user_id] = now

    # ======================
    # AI CHAT
    # ======================

    data = context.bot_data.get(
        "data",
        {},
    )

    persona = data.get(
        "persona",
        "manis, romantis, lembut",
    )

    await context.bot.send_chat_action(
        chat_id=msg.chat_id,
        action="typing",
    )

    try:

        user_input = text

        if extra_context:

            user_input = (
                f"{extra_context}\n"
                f"Pesan user: {text}"
            )

        # ======================
        # FIRST AI CALL
        # ======================

        answer = ask_openrouter(
            user_id=user_id,
            user_text=user_input,
            persona=persona,
            telegram_name=telegram_name,
        )

        # ======================
        # TOOL PARSING
        # ======================

        tool_call = parse_tool_call(
            answer
        )

        if (
            tool_call
            and "[TOOL:" not in user_input
        ):

            tool_result = execute_tool(
                tool_call["tool"],
                tool_call["argument"],
            )

            final_prompt = f"""
Tool Result:
{tool_result}

Jawab user secara natural,
jelas, dan ramah berdasarkan
hasil tool di atas.
"""

            answer = ask_openrouter(
                user_id=user_id,
                user_text=final_prompt,
                persona=persona,
                telegram_name=telegram_name,
            )

        # ======================
        # MESSAGE FORMATTER
        # ======================

        messages = split_message(
            answer
        )

        for part in messages:

            # CODE BLOCK
            if "```" in part:

                await msg.reply_text(part)

            # NORMAL TEXT
            else:

                await msg.reply_text(
                    part
                )

    except Exception as e:

        traceback.print_exc()

        await msg.reply_text(
            f"ERROR:\n{e}"
        )


async def deny_access(msg, context):

    context.user_data["state"] = None

    await msg.reply_text(
        "Fitur ini khusus admin ya 💖"
    )