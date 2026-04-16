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

    # 🔥 bierzemy 3 strony (możesz zwiększyć do 5)
    for base in base_urls:
        for page in range(1, 4):
            url = f"{base}?page={page}"

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")

            for item in soup.select("div[data-cy='l-card']"):
                title = item.select_one("h6")
                price = item.select_one("p[data-testid='ad-price']")
                link = item.select_one("a")

                if title and link:
                    listings.append({
                        "title": title.text.strip(),
                        "price": price.text.strip() if price else "brak",
                        "url": "https://www.olx.pl" + link["href"],
                    })

    return listings
