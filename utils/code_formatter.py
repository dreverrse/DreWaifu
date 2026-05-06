import html
import re

CODE_BLOCK_PATTERN = r"```(\w+)?\n([\s\S]*?)```"


def convert_code_blocks(text):

    matches = re.finditer(CODE_BLOCK_PATTERN, text)

    for match in matches:

        language = match.group(1) or ""

        code = match.group(2)

        escaped = html.escape(code)

        replacement = f"<pre><code class='{language}'>" f"{escaped}" f"</code></pre>"

        text = text.replace(match.group(0), replacement)

    return text
