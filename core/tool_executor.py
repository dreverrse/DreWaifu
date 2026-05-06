from core.tool_registry import get_tool


def execute_tool(tool_name, argument):
    tool = get_tool(tool_name)
    if not tool:
        return "Tool tidak ditemukan."
    try:
        return tool["function"](argument)
    except Exception as e:
        return f"TOOL ERROR: {e}"
