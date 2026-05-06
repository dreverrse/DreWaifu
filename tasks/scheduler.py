# Alias dan helper untuk scheduler tasks
from tasks.crypto_monitor import start_crypto_monitor
from tasks.habit_notifier import start_habit_notifier
from config import CRYPTO_CHECK_INTERVAL


def start_all_tasks(job_queue):
    start_crypto_monitor(job_queue, interval=CRYPTO_CHECK_INTERVAL)
    start_habit_notifier(job_queue)
