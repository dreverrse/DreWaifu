import logging
import traceback
import time

from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TOKEN
from utils.storage import load_data
from core.load_tools import load_tools

from handlers.commands import (
    start,
    help_cmd,
    persona_cmd,
    post_cmd,
    schedule_cmd,
    list_cmd,
    del_cmd,
    dev_cmd,
    clearjob_cmd,
)

from handlers.ai_chat import ai_reply
from handlers.scheduler import rebuild_jobs

from handlers.crypto import (
    add_alert_cmd,
    list_alert_cmd,
    del_alert_cmd,
    price_cmd,
)

from handlers.habit import (
    add_habit_cmd,
    list_habit_cmd,
    del_habit_cmd,
    done_habit_cmd,
)

from tasks.crypto_monitor import start_crypto_monitor
from tasks.habit_notifier import start_habit_notifier
from config import CRYPTO_CHECK_INTERVAL

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


# ======================
# COMMAND MENU
# ======================


async def setup_commands(context):
    await context.bot.delete_my_commands()
    await context.bot.set_my_commands([
        BotCommand("start", "Open DreWaifu"),
        BotCommand("price", "Cek harga crypto"),
        BotCommand("addalert", "Set alert harga crypto"),
        BotCommand("listalert", "Lihat semua alert"),
        BotCommand("delalert", "Hapus alert"),
        BotCommand("addhabit", "Tambah habit harian"),
        BotCommand("listhabit", "Lihat semua habit"),
        BotCommand("delhabit", "Hapus habit"),
        BotCommand("done", "Tandai habit selesai"),
        BotCommand("dev", "Developer info"),
    ])


# ======================
# BUILD APPLICATION
# ======================


def build_app():
    load_tools()

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

    # ======================
    # COMMAND HANDLERS
    # ======================

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("persona", persona_cmd))
    app.add_handler(CommandHandler("post", post_cmd))
    app.add_handler(CommandHandler("schedule", schedule_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("del", del_cmd))
    app.add_handler(CommandHandler("dev", dev_cmd))
    app.add_handler(CommandHandler("clearjob", clearjob_cmd))

    # Crypto
    app.add_handler(CommandHandler("price", price_cmd))
    app.add_handler(CommandHandler("addalert", add_alert_cmd))
    app.add_handler(CommandHandler("listalert", list_alert_cmd))
    app.add_handler(CommandHandler("delalert", del_alert_cmd))

    # Habit
    app.add_handler(CommandHandler("addhabit", add_habit_cmd))
    app.add_handler(CommandHandler("listhabit", list_habit_cmd))
    app.add_handler(CommandHandler("delhabit", del_habit_cmd))
    app.add_handler(CommandHandler("done", done_habit_cmd))

    # ======================
    # MESSAGE HANDLER
    # ======================

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    # ======================
    # JOB QUEUE
    # ======================

    if app.job_queue:
        app.job_queue.run_once(setup_commands, 1)
        rebuild_jobs(app)
        start_crypto_monitor(app.job_queue, interval=CRYPTO_CHECK_INTERVAL)
        start_habit_notifier(app.job_queue)

    return app


# ======================
# MAIN LOOP
# ======================


def main():
    while True:
        try:
            logging.info("DreWaifu starting...")
            app = build_app()
            app.run_polling(drop_pending_updates=True, close_loop=False)

        except KeyboardInterrupt:
            logging.info("Bot dihentikan manual.")
            break

        except Exception as e:
            logging.error("Crash: %s", e)
            traceback.print_exc()
            logging.info("Restart dalam 5 detik...")
            time.sleep(5)


if __name__ == "__main__":
    main()
