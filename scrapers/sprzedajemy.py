import requests
from bs4 import BeautifulSoup

URL = "https://sprzedajemy.pl/motoryzacja/samochody?q=srx"

def fetch_sprzedajemy():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    listings = []

    for item in soup.select("a"):
        href = item.get("href", "")
        text = item.get_text(" ", strip=True)

        if "srx" in text.lower() and href:
            listings.append({
                "title": text,
                "price": "brak",
                "url": href,
            })

    return listings
