import re

TOOL_PATTERN = r"\[TOOL:(.*?)\|(.*?)\]"


def parse_tool_call(text):

    match = re.search(TOOL_PATTERN, text)

    if not match:
        return None

    tool_name = match.group(1).strip()

    argument = match.group(2).strip()

    return {"tool": tool_name, "argument": argument}
