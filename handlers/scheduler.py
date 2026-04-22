from datetime import time
from config import TZ, CHANNEL_ID
from telegram.constants import ParseMode
from utils.helpers import format_channel_text


async def send_scheduled_post(context):
    data = context.bot_data["data"]
    text = context.job.data["text"]

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=format_channel_text(data, text),
        parse_mode=ParseMode.HTML
    )


def add_daily_job(job_queue, job_id, hhmm, text):
    if not job_queue:
        return

    try:
        hour, minute = map(int, hhmm.split(":"))

        job_queue.run_daily(
            send_scheduled_post,
            time=time(hour=hour, minute=minute, tzinfo=TZ),
            data={"text": text},
            name=str(job_id)
        )

    except Exception as e:
        print("JOB ERROR:", e)


def rebuild_jobs(app):
    if not app.job_queue:
        print("JobQueue tidak aktif")
        return

    data = app.bot_data["data"]

    for item in data.get("scheduled_posts", []):
        add_daily_job(
            app.job_queue,
            item["id"],
            item["time"],
            item["text"]
        )