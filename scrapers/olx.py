import requests
from bs4 import BeautifulSoup

base_urls = [
    "https://www.olx.pl/motoryzacja/samochody/q-cadillac-srx/",
    "https://www.olx.pl/motoryzacja/samochody/q-honda-element/"
]


def fetch_olx():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    listings = []
    seen_links = set()

    for base in base_urls:
        for page in range(1, 4):
            url = f"{base}?page={page}"

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")

            # 🔥 łapiemy wszystkie linki do ogłoszeń
            for a in soup.select("a[href]"):
                href = a.get("href")

                if not href:
                    continue

                # 🔥 tylko realne ogłoszenia OLX
                if "/d/oferta/" not in href:
                    continue

                full_url = "https://www.olx.pl" + href.split("?")[0]

                if full_url in seen_links:
                    continue

                seen_links.add(full_url)

                title_tag = a.find("h6")
                price_tag = a.find("p")

                listings.append({
                    "title": title_tag.text.strip() if title_tag else "brak tytułu",
                    "price": price_tag.text.strip() if price_tag else "brak",
                    "url": full_url,
                })

    return listings
