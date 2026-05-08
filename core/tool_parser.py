import re

TOOL_PATTERN = r"\[TOOL:([^\|]+)\|([^\]]*)\]"


def parse_tool_call(text):
    match = re.search(TOOL_PATTERN, text)
    if not match:
        return None
    return {
        "tool": match.group(1).strip(),
        "argument": match.group(2).strip(),
    }


def has_tool_call(text):
    return bool(re.search(TOOL_PATTERN, text))


def strip_tool_call(text):
    return re.sub(TOOL_PATTERN, "", text).strip()
