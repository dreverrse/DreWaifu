"""
SQLite backend (opsional, siap digunakan jika ingin migrasi dari JSON).
"""
import sqlite3
import os

DB_FILE = "drewaifu.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS crypto_alerts (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            coin TEXT NOT NULL,
            condition TEXT NOT NULL,
            target REAL NOT NULL,
            chat_id INTEGER NOT NULL,
            triggered INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            streak INTEGER DEFAULT 0,
            last_done TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_posts (
            id TEXT PRIMARY KEY,
            time TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
