import requests
from bs4 import BeautifulSoup


def web_search(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, timeout=20, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return "\n".join(lines)[:5000]
    except Exception as e:
        return f"WEB ERROR: {e}"
