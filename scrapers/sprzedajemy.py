import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT

urls = [
    "https://sprzedajemy.pl/motoryzacja/samochody?q=srx",
    "https://sprzedajemy.pl/motoryzacja/samochody?q=honda+element"
]


def fetch_sprzedajemy():
    headers = {"User-Agent": "Mozilla/5.0"}

    listings = []

    for URL in urls:
        try:
            r = requests.get(URL, headers=headers, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
        except requests.RequestException as exc:
            print(f"Sprzedajemy fetch failed for {URL}: {exc}")
            continue

        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select("a"):
            href = item.get("href", "")
            text = item.get_text(" ", strip=True)

            # 🔥 KLUCZ: tylko realne ogłoszenia
            if "/oferta/" not in href and "/ogloszenie/" not in href:
                continue

            if href and text:
                listings.append({
                    "title": text,
                    "price": "brak",
                    "url": href,
                })

    return listings
