from database.db import is_seen, mark_seen
from core.filters import is_valid_listing
from core.details import fetch_listing_year


def normalize_url(url):
    if not url:
        return url
    return url.split("?")[0]


def build_srx_alert(title, price, url):
    text = f"{title} {url}".lower()

    if any(marker in text for marker in ["4.6", "4,6", "v8", "northstar"]):
        prefix = "🚗 SRX V8 PRIORYTET"
    else:
        prefix = "🚗 MATCH"

    return f"{prefix}\n{title}\n{price}\n{url}"


def classify_listing(item):
    raw_url = item.get("url")
    if not raw_url:
        return None

    url = normalize_url(raw_url)
    title = item.get("title", "")
    text = (title + " " + url).lower()

    # 🔥 HARD BLOCK — SRX II (2010+)
    if "srx" in text:
        if any(x in text for x in ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]):
            return None

    # 🔥 standardowy filtr
    if not is_valid_listing(text):
        return None

    # Dla SRX działamy fail-closed:
    # alert wysyłamy tylko wtedy, gdy rocznik z tekstu lub z podstrony
    # potwierdza zakres SRX I (2004-2009).
    if "srx" in text:
        year = fetch_listing_year(url)

        if year is None:
            return None

        if year < 2004 or year > 2009:
            return None

    return {
        "title": title,
        "price": item.get("price"),
        "url": url,
    }


def scan_listings(listings):
    alerts = []
    matching_count = 0

    for item in listings:
        matched = classify_listing(item)
        if not matched:
            continue

        matching_count += 1

        url = matched["url"]
        if is_seen(url):
            continue

        mark_seen(url)
        alerts.append(build_srx_alert(
            matched["title"],
            matched["price"],
            url,
        ))

    return {
        "alerts": alerts,
        "matching_count": matching_count,
        "new_alerts_count": len(alerts),
    }


def analyze_listings(listings):
    return scan_listings(listings)["alerts"]
