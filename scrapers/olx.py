import requests
from bs4 import BeautifulSoup

URL = "https://www.olx.pl/motoryzacja/samochody/q-srx/"

def fetch_olx():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    listings = []

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
