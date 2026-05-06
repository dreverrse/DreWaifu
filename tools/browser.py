import requests
from bs4 import BeautifulSoup


def browse(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, timeout=30, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator="\n")[:6000]
    except Exception as e:
        return f"BROWSE ERROR: {e}"
