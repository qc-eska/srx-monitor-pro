from database.db import is_seen, mark_seen
from core.filters import is_valid_listing
from core.details import fetch_listing_year


def normalize_url(url):
    if not url:
        return url
    return url.split("?")[0]


def analyze_listings(listings):
    alerts = []

    for item in listings:
        raw_url = item.get("url")
        if not raw_url:
            continue

        url = normalize_url(raw_url)

        if is_seen(url):
            continue

        title = item.get("title", "")
        text = title + " " + url

        # 🔥 szybki filtr (jak wcześniej)
        if not is_valid_listing(text):
            continue

        # 🔥 DODATKOWY CHECK TYLKO DLA SRX
        if "srx" in text.lower():
            year = fetch_listing_year(url)

            # jeśli znaleziony rok i poza zakresem → odrzucamy
            if year and (year < 2004 or year > 2009):
                continue

        mark_seen(url)

        alerts.append(
            f"🚗 MATCH\n{title}\n{item.get('price')}\n{url}"
        )

    return alerts
