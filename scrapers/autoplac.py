import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT

urls = [
    "https://autoplac.pl/szukaj/cadillac/srx",
    "https://autoplac.pl/szukaj/honda/element"
]


def fetch_autoplac():
    headers = {"User-Agent": "Mozilla/5.0"}

    listings = []

    for URL in urls:
        try:
            r = requests.get(URL, headers=headers, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
        except requests.RequestException as exc:
            print(f"Autoplac fetch failed for {URL}: {exc}")
            continue

        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select("a"):
            href = item.get("href", "")
            text = item.get_text(" ", strip=True)

            # 🔥 filtr ogłoszeń
            if "/oferta/" not in href:
                continue

            if href and text:
                listings.append({
                    "title": text,
                    "price": "brak",
                    "url": href,
                })

    return listings
