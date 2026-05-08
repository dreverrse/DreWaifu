import os
import mimetypes


ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".json",
    ".csv", ".html", ".css", ".yaml", ".yml", ".env",
    ".xml", ".log", ".sh", ".bat",
}

MAX_SIZE_BYTES = 100_000  # 100KB


def read_file(path):
    """Baca isi file yang dikirim user."""
    try:
        path = path.strip()

        if not os.path.exists(path):
            return f"File tidak ditemukan: {path}"

        ext = os.path.splitext(path)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return f"Tipe file '{ext}' tidak didukung. Yang didukung: {', '.join(sorted(ALLOWED_EXTENSIONS))}"

        size = os.path.getsize(path)
        if size > MAX_SIZE_BYTES:
            return f"File terlalu besar ({size // 1024}KB). Maksimal 100KB."

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        return content[:4000]

    except Exception as e:
        return f"FILE READER ERROR: {e}"
