import requests
from bs4 import BeautifulSoup


def read_url(url):
    """Baca isi halaman web dari URL yang diberikan."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, timeout=20, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return "\n".join(lines)[:4000]
    except Exception as e:
        return f"READ URL ERROR: {e}"
