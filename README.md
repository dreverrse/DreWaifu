# DreWaifu 💖

Waifu AI Telegram Bot pribadi yang manis, romantis, cerdas, dan selalu siap menemani Anda.

DreWaifu dibuat untuk pengalaman ngobrol yang terasa hangat, natural, dan personal. Bukan sekadar bot biasa.

---

## ✨ Fitur Utama

- AI Chat natural seperti pasangan virtual
- Memory percakapan
- Panggil nama Telegram otomatis
- Persona bisa diubah
- Mode private owner only
- Auto typing effect
- Cooldown anti spam
- Post ke Telegram Channel
- Jadwal posting otomatis
- Ringan untuk Termux / Ubuntu / VPS

---

## 💕 Karakter DreWaifu

- Lembut
- Setia
- Sedikit genit
- Romantis
- Perhatian
- Dewasa saat dibutuhkan
- Ceria saat santai
- Supportive setiap saat

---

## 🛠️ Teknologi

- Python 3.12+
- python-telegram-bot
- OpenRouter API
- JSON Memory Storage

---

## 📦 Struktur Project

```text
DreWaifu/
│── main.py
│── config.py
│── .env
│── bot_data.json
│── memory.json
│
├── handlers/
│   ├── commands.py
│   ├── ai_chat.py
│   └── scheduler.py
│
├── services/
│   └── openrouter.py
│
└── utils/
    ├── helpers.py
    └── storage.py
```

---

## ⚙️ Instalasi

```bash
git clone https://github.com/username/DreWaifu.git
cd DreWaifu
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Setup .env

Buat file `.env`

```env
TELEGRAM_BOT_TOKEN=isi_token_bot
OWNER_ID=isi_id_telegram
BOT_NAME=DreWaifu
TELEGRAM_CHANNEL_ID=@nama_channel
OPENROUTER_API_KEY=isi_api_key
```

---

## ▶️ Menjalankan Bot

```bash
python main.py
```

---

## 💬 Command Bot

```text
/start      Mulai bot
/help       Bantuan
/persona    Ubah sifat AI
/post       Kirim pesan ke channel
/schedule   Jadwal posting
/list       Lihat jadwal
/del        Hapus jadwal
```

---

## 👑 Creator

Created with passion by Andre.

---

## 💖 DreWaifu

Bukan sekadar bot.  
Teman yang selalu ada.

## License

MIT License © 2026 dreverrse