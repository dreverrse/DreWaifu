TOOLS = {}


def register_tool(name, func, description):
    TOOLS[name] = {"function": func, "description": description}


def get_tool(name):
    return TOOLS.get(name)


def get_all_tools():
    return TOOLS
