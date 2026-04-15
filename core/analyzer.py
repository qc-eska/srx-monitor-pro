import re

def extract_year(text: str):
    match = re.search(r"(20\d{2})", text)
    if match:
        return int(match.group(1))
    return None


def analyze_listings(listings):
    alerts = []

    for item in listings:
        title = item.get("title", "")

        year = extract_year(title)

        # 🚫 odrzucamy SRX po 2009
        if year and year > 2009:
            continue

        if item.get("new"):
            alerts.append(
                f"🚗 SRX 2004–2009\n{title}\n{item.get('price')}\n{item.get('url')}"
            )

    return alerts
