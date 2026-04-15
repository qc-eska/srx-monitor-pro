import re
from database.db import is_seen, mark_seen

ALLOWED_MIN_YEAR = 2004
ALLOWED_MAX_YEAR = 2009


def extract_year(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


def is_valid_srx(item):
    text = (item.get("title", "") + " " + item.get("url", "")).lower()

    # blokada SRX II (pewna)
    if any(x in text for x in ["2010", "2011", "2012", "2013"]):
        return False

    year = extract_year(text)

    # 🔥 KLUCZOWA ZMIANA:
    # jeśli NIE ma roku → NIE blokujemy
    if year is None:
        return True

    return ALLOWED_MIN_YEAR <= year <= ALLOWED_MAX_YEAR


def analyze_listings(listings):
    alerts = []

    for item in listings:
        url = item.get("url")

        if not url:
            continue

        if is_seen(url):
            continue

        if not is_valid_srx(item):
            continue

        mark_seen(url)

        alerts.append(
            f"🚗 SRX 2004–2009\n{item.get('title')}\n{item.get('price')}\n{url}"
        )

    return alerts
