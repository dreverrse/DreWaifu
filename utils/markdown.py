import re

SPECIAL_CHARS = r"_*[]()~`>#+-=|{}.!"


def escape_markdown(text):
    return re.sub(f"([{re.escape(SPECIAL_CHARS)}])", r"\\\1", text)


def convert_to_markdownv2(text):
    # Konversi **bold** ke *bold*
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)
    # Konversi __italic__ ke _italic_
    text = re.sub(r"__(.+?)__", r"_\1_", text)
    # Escape karakter khusus yang bukan bagian dari format
    text = re.sub(r"(?<!\*)\*(?!\*|[^*]+\*)([^*]+)(?<!\*)(?!\*)", r"*\1*", text)
    return text


def safe_markdown(text):
    # Konversi dulu, lalu escape karakter berbahaya di luar format
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)
    text = re.sub(r"__(.+?)__", r"_\1_", text)
    # Escape karakter MarkdownV2 yang tidak dalam konteks format
    text = re.sub(r"(?<!\\)([.!?()\-#=+|{}])", r"\\\1", text)
    return text