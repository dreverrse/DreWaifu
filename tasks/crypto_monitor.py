"""
Crypto Monitor Task
Cek harga setiap CRYPTO_CHECK_INTERVAL detik.
Kirim notifikasi jika kondisi alert terpenuhi.
Alert hanya dikirim sekali (triggered=True) sampai user reset.
"""

import logging
from utils.storage import load_data, save_data
from services.crypto_price import get_price

logger = logging.getLogger(__name__)


async def check_crypto_alerts(context):
    data = load_data()
    alerts_changed = False

    for user_id, alerts in data["crypto_alerts"].items():
        for alert in alerts:
            if alert.get("triggered"):
                continue

            result, error = get_price(alert["coin"])
            if error or result is None:
                logger.warning(f"Gagal ambil harga {alert['coin']}: {error}")
                continue

            current_price = result["price"]
            condition = alert["condition"]
            target = alert["target"]

            triggered = False
            if condition == ">" and current_price > target:
                triggered = True
            elif condition == "<" and current_price < target:
                triggered = True

            if triggered:
                symbol = "naik di atas" if condition == ">" else "turun di bawah"
                change = result.get("change_24h", 0)
                arrow = "📈" if change >= 0 else "📉"
                sign = "+" if change >= 0 else ""

                text = (
                    f"🚨 CRYPTO ALERT!\n\n"
                    f"🪙 {alert['coin']} {symbol} ${target:,.2f}\n"
                    f"💵 Harga sekarang: ${current_price:,.4f}\n"
                    f"{arrow} 24h: {sign}{change}%\n\n"
                    f"Alert ID {alert['id']} telah terpenuhi.\n"
                    f"Gunakan /delalert {alert['id']} jika ingin hapus."
                )

                try:
                    await context.bot.send_message(
                        chat_id=alert["chat_id"],
                        text=text,
                    )
                    alert["triggered"] = True
                    alerts_changed = True
                    logger.info(f"Alert triggered: {alert['id']} untuk user {user_id}")
                except Exception as e:
                    logger.error(f"Gagal kirim alert ke {alert['chat_id']}: {e}")

    if alerts_changed:
        save_data(data)


def start_crypto_monitor(job_queue, interval=300):
    if not job_queue:
        logger.warning("JobQueue tidak aktif, crypto monitor tidak bisa dijalankan.")
        return

    job_queue.run_repeating(
        check_crypto_alerts,
        interval=interval,
        first=30,
        name="crypto_monitor",
    )
    logger.info(f"Crypto monitor aktif, interval {interval} detik.")
