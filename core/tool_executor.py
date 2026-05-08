from core.tool_registry import get_tool
import traceback


def execute_tool(tool_name, argument, user_id=None):
    tool = get_tool(tool_name)
    if not tool:
        return f"Tool '{tool_name}' tidak ditemukan."
    try:
        func = tool["function"]
        import inspect
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        # Beberapa tool butuh user_id
        if "user_id" in params and user_id is not None:
            return func(argument, user_id=user_id)
        return func(argument)
    except Exception as e:
        traceback.print_exc()
        return f"Tool error [{tool_name}]: {e}"
