import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://html.duckduckgo.com/html/"


def web_search(query):
    """Cari informasi dari internet menggunakan DuckDuckGo."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": query, "kl": "id-id"}
        r = requests.post(SEARCH_URL, data=params, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        for result in soup.select(".result__body")[:5]:
            title = result.select_one(".result__title")
            snippet = result.select_one(".result__snippet")
            link = result.select_one(".result__url")

            if snippet:
                t = title.get_text(strip=True) if title else ""
                s = snippet.get_text(strip=True)
                l = link.get_text(strip=True) if link else ""
                results.append(f"{t}\n{s}\n{l}")

        if not results:
            return "Tidak ada hasil ditemukan."

        return "\n\n".join(results)[:3000]

    except Exception as e:
        return f"WEB SEARCH ERROR: {e}"
