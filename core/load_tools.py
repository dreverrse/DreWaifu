from core.tool_registry import register_tool
from tools.web_search import web_search


def load_tools():
    register_tool(
        name="web_search",
        func=web_search,
        description="Read website content from URL",
    )
