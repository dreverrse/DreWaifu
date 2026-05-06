import re

SPECIAL_CHARS = r"_*[]()~`>#+-=|{}.!"


def escape_markdown(text):

    return re.sub(f"([{re.escape(SPECIAL_CHARS)}])", r"\\\1", text)


def prepare_markdown(text):

    if "```" in text:
        return text

    return escape_markdown(text)
