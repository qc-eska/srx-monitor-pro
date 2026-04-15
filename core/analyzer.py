from database.db import is_seen, mark_seen
from core.filters import is_valid_listing


def analyze_listings(listings):
    alerts = []

    for item in listings:
        url = item.get("url")

        if not url:
            continue

        if is_seen(url):
            continue

        text = item.get("title", "") + " " + url

        if not is_valid_listing(text):
            continue

        mark_seen(url)

        alerts.append(
            f"🚗 MATCH\n{item.get('title')}\n{item.get('price')}\n{url}"
        )

    return alerts
