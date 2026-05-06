"""
Crypto Alert Handler
Commands:
  /addalert BTC > 70000   - alert jika BTC di atas 70000 USD
  /addalert ETH < 2000    - alert jika ETH di bawah 2000 USD
  /listalert              - lihat semua alert aktif
  /delalert alert_1       - hapus alert berdasarkan ID
  /price BTC              - cek harga sekarang
"""

from utils.storage import save_data, load_data
from utils.helpers import next_alert_id
from services.crypto_price import get_price, COINGECKO_IDS


async def add_alert_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)
    chat_id = msg.chat_id

    if len(context.args) < 3:
        await msg.reply_text(
            "Format: /addalert COIN KONDISI TARGET\n"
            "Contoh:\n"
            "/addalert BTC > 70000\n"
            "/addalert ETH < 2000"
        )
        return

    coin = context.args[0].upper()
    condition = context.args[1]
    try:
        target = float(context.args[2].replace(",", ""))
    except ValueError:
        await msg.reply_text("Target harga harus berupa angka.")
        return

    if condition not in (">", "<"):
        await msg.reply_text("Kondisi harus > atau <")
        return

    coin_lower = coin.lower()
    from services.crypto_price import COINGECKO_IDS
    if coin_lower not in COINGECKO_IDS:
        await msg.reply_text(
            f"Coin '{coin}' tidak dikenali.\n"
            f"Contoh yang valid: BTC, ETH, BNB, SOL, XRP, DOGE"
        )
        return

    data = load_data()
    if user_id not in data["crypto_alerts"]:
        data["crypto_alerts"][user_id] = []

    alert_id = next_alert_id(data["crypto_alerts"][user_id])

    data["crypto_alerts"][user_id].append({
        "id": alert_id,
        "coin": coin,
        "condition": condition,
        "target": target,
        "chat_id": chat_id,
        "triggered": False,
    })

    save_data(data)

    symbol = "naik di atas" if condition == ">" else "turun di bawah"
    await msg.reply_text(
        f"✅ Alert ditambahkan!\n"
        f"🪙 {coin} {symbol} ${target:,.2f}\n"
        f"🆔 {alert_id}\n\n"
        f"Aku akan kabari kamu otomatis ya 💖"
    )


async def list_alert_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)

    data = load_data()
    alerts = data["crypto_alerts"].get(user_id, [])

    if not alerts:
        await msg.reply_text("Belum ada crypto alert aktif.")
        return

    text = "📊 Crypto Alert Aktif\n\n"
    for a in alerts:
        symbol = ">" if a["condition"] == ">" else "<"
        text += (
            f"🆔 {a['id']}\n"
            f"🪙 {a['coin']} {symbol} ${a['target']:,.2f}\n\n"
        )

    await msg.reply_text(text.strip())


async def del_alert_cmd(update, context):
    msg = update.effective_message
    user_id = str(update.effective_user.id)

    if not context.args:
        await msg.reply_text("Contoh: /delalert alert_1")
        return

    alert_id = context.args[0]
    data = load_data()
    alerts = data["crypto_alerts"].get(user_id, [])
    before = len(alerts)
    data["crypto_alerts"][user_id] = [a for a in alerts if a["id"] != alert_id]
    save_data(data)

    if len(data["crypto_alerts"][user_id]) < before:
        await msg.reply_text(f"🗑 Alert {alert_id} dihapus.")
    else:
        await msg.reply_text("ID tidak ditemukan.")


async def price_cmd(update, context):
    msg = update.effective_message

    if not context.args:
        await msg.reply_text("Contoh: /price BTC")
        return

    coin = context.args[0]
    await context.bot.send_chat_action(chat_id=msg.chat_id, action="typing")

    result, error = get_price(coin)

    if error:
        await msg.reply_text(f"❌ {error}")
        return

    change = result["change_24h"]
    arrow = "📈" if change >= 0 else "📉"
    sign = "+" if change >= 0 else ""

    await msg.reply_text(
        f"🪙 {coin.upper()}\n"
        f"💵 ${result['price']:,.4f}\n"
        f"{arrow} 24h: {sign}{change}%"
    )
