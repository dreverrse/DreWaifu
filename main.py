import logging
import traceback
import time

from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

from config import TOKEN
from utils.storage import load_data

from handlers.commands import (
    start,
    help_cmd,
    persona_cmd,
    post_cmd,
    schedule_cmd,
    list_cmd,
    del_cmd, 
    dev_cmd
)

from handlers.ai_chat import ai_reply
from handlers.scheduler import rebuild_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ======================
# RESET COMMAND MENU
# ======================

async def setup_commands(context):
    await context.bot.delete_my_commands()

    await context.bot.set_my_commands([
        BotCommand("start", "Open DreWaifu"),
        BotCommand("dev", "Developer")
    ])


def build_app():
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .http_version("1.1")
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .build()
    )

    app.bot_data["data"] = load_data()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("persona", persona_cmd))
    app.add_handler(CommandHandler("post", post_cmd))
    app.add_handler(CommandHandler("schedule", schedule_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("del", del_cmd))
    app.add_handler(CommandHandler("dev", dev_cmd))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_reply
        )
    )

    # Tambahan hapus command lama Telegram
    if app.job_queue:
        app.job_queue.run_once(setup_commands, 1)

    rebuild_jobs(app)

    return app


def main():
    while True:
        try:
            logging.info("DreWaifu starting...")

            app = build_app()

            app.run_polling(
                drop_pending_updates=True,
                close_loop=False
            )

        except KeyboardInterrupt:
            logging.info("Bot dihentikan manual.")
            break

        except Exception as e:
            logging.error("Crash: %s", e)
            traceback.print_exc()

            logging.info("Restart 5 detik...")
            time.sleep(5)


if __name__ == "__main__":
    main()