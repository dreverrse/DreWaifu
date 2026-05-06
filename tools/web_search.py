import requests
from bs4 import BeautifulSoup


def web_search(url):
    try:
        r = requests.get(url, timeout=20)

        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(separator="\n")

        return text[:5000]

    except Exception as e:
        return f"WEB ERROR: {e}"
