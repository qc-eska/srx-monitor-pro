import re

ALLOWED_MIN_YEAR = 2004
ALLOWED_MAX_YEAR = 2009


def extract_year(text: str):
    if not text:
        return None
    match = re.search(r"(20\d{2})", text)
    return int(match.group(1)) if match else None


def is_valid_srx(item):
    text = (item.get("title", "") + " " + item.get("url", "")).lower()

    # szybki kill dla SRX II (2010+ często w URL / title)
    if "2010" in text or "2011" in text or "2012" in text or "2013" in text:
        return False

    year = extract_year(text)

    if year:
        return ALLOWED_MIN_YEAR <= year <= ALLOWED_MAX_YEAR

    # jeśli nie ma roku → NIE wysyłaj ślepo (ważne!)
    return False


def analyze_listings(listings):
    alerts = []

    for item in listings:

        if not is_valid_srx(item):
            continue

        alerts.append(
            f"🚗 SRX 2004–2009\n{item.get('title')}\n{item.get('price')}\n{item.get('url')}"
        )

    return alerts
