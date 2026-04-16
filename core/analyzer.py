from database.db import is_seen, mark_seen
from core.filters import is_valid_listing


def normalize_url(url):
    if not url:
        return url

    # usuwa parametry typu ?utm=...
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

        text = item.get("title", "") + " " + url

        if not is_valid_listing(text):
            continue

        mark_seen(url)

        alerts.append(
            f"🚗 MATCH\n{item.get('title')}\n{item.get('price')}\n{url}"
        )

    return alerts
