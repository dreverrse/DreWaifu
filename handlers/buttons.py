from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = [
        ["💖 Ngobrol", "💕 Manja"],
        ["📤 Post Channel", "📅 Jadwal"],
        ["📋 List Jadwal", "🧹 Hapus Semua"],
        ["⚙️ Persona", "ℹ️ Bantuan"],
        ["🪙 Cek Harga", "📊 Alert Crypto"],
        ["💪 Habit", "✅ Selesai Habit"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def inline_panel():
    keyboard = [
        [
            InlineKeyboardButton("💖 Chat", callback_data="chat"),
            InlineKeyboardButton("⚙️ Setting", callback_data="setting"),
        ],
        [
            InlineKeyboardButton("📅 Jadwal", callback_data="jadwal"),
            InlineKeyboardButton("📤 Post", callback_data="post"),
        ],
        [
            InlineKeyboardButton("🪙 Crypto", callback_data="crypto"),
            InlineKeyboardButton("💪 Habit", callback_data="habit"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
