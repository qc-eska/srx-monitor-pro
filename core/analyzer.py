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
        text = (title + " " + url).lower()

        # 🔥 HARD BLOCK — SRX II (2010+)
        if "srx" in text:
            if any(x in text for x in ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]):
                continue

        # 🔥 standardowy filtr
        if not is_valid_listing(text):
            continue

        # 🔥 dokładny check (tylko SRX)
        if "srx" in text:
            year = fetch_listing_year(url)

            if year and (year < 2004 or year > 2009):
                continue

        mark_seen(url)

        alerts.append(
            f"🚗 MATCH\n{title}\n{item.get('price')}\n{url}"
        )

    return alerts
