import html
import re

CODE_BLOCK_PATTERN = r"```(\w+)?\n([\s\S]*?)```"


def convert_code_blocks(text):
    matches = list(re.finditer(CODE_BLOCK_PATTERN, text))
    for match in reversed(matches):
        language = match.group(1) or ""
        code = match.group(2)
        escaped = html.escape(code)
        replacement = f"<pre><code class='{language}'>{escaped}</code></pre>"
        text = text[: match.start()] + replacement + text[match.end() :]
    return text
