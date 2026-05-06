from telegram.ext import CommandHandler


async def start(update, context):
    await update.message.reply_text("Bot aktif")


async def help_cmd(update, context):
    await update.message.reply_text("/help /post /schedule")


def register_basic(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
