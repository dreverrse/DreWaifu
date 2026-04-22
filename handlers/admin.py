from telegram.ext import CommandHandler
from storage import load_data, save_data
from utils import is_owner, format_channel_text
from config import CHANNEL_ID

async def post_cmd(update,context):
    if not is_owner(update): return
    text=' '.join(context.args)
    await context.bot.send_message(chat_id=CHANNEL_ID,text=format_channel_text(text),parse_mode='HTML')
    await update.message.reply_text('Terkirim')

def register_admin(app):
    app.add_handler(CommandHandler('post',post_cmd))