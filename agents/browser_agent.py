from tools.browser import browse


def run_browser_agent(url):
    content = browse(url)
    return content
