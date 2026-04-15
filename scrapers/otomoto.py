import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.otomoto.pl/osobowe/cadillac/srx/",
    "https://www.otomoto.pl/osobowe/honda/element/"
]


def fetch_otomoto():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    listings = []

    for URL in urls:
        r = requests.get(URL, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select("article"):
            title = item.select_one("h2")
            price = item.select_one("span")
            link = item.select_one("a")

            if title and link:
                listings.append({
                    "title": title.text.strip(),
                    "price": price.text.strip() if price else "brak",
                    "url": link["href"],
                })

    return listings
