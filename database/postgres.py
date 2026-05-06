"""
PostgreSQL backend (opsional, untuk production scale).
Butuh: pip install psycopg2-binary
"""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "")


def get_connection():
    try:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except ImportError:
        raise ImportError("Install psycopg2-binary: pip install psycopg2-binary")
    except Exception as e:
        raise Exception(f"Koneksi PostgreSQL gagal: {e}")
