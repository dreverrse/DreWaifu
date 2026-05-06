from config import CHANNEL_ID
from utils.storage import load_data, save_data
from utils.helpers import is_owner, format_channel_text
from telegram.ext import CommandHandler


async def post_cmd(update, context):
    if not is_owner(update):
        await update.message.reply_text("Fitur ini khusus admin ya 💖")
        return

    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Contoh:\n/post Halo semuanya")
        return

    data = load_data()
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=format_channel_text(data, text),
        parse_mode="HTML",
    )
    await update.message.reply_text("Terkirim 💌")


def register_admin(app):
    app.add_handler(CommandHandler("post", post_cmd))
