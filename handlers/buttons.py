# handlers/buttons.py

from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ======================
# KEYBOARD UTAMA
# ======================

def main_menu():
    keyboard = [
        ["💖 Ngobrol", "💕 Manja"],
        ["📤 Post Channel", "📅 Jadwal"],
        ["📋 List Jadwal", "🧹 Hapus Semua"],
        ["⚙️ Persona", "ℹ️ Bantuan"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


# ======================
# INLINE MENU
# ======================

def inline_panel():
    keyboard = [
        [
            InlineKeyboardButton(
                "💖 Chat",
                callback_data="chat"
            ),
            InlineKeyboardButton(
                "⚙️ Setting",
                callback_data="setting"
            )
        ],
        [
            InlineKeyboardButton(
                "📅 Jadwal",
                callback_data="jadwal"
            ),
            InlineKeyboardButton(
                "📤 Post",
                callback_data="post"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)