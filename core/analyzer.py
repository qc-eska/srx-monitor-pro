from core.filters import is_valid_srx


def analyze_listings(listings):
    alerts = []
    seen = set()

    for item in listings:
        title = (item.get("title") or "").lower()
        url = item.get("url")

        if not url:
            continue

        # 🔴 DEDUPLICATION
        if url in seen:
            continue
        seen.add(url)

        # 🔴 TWARDY SRX FILTER (to brakowało!)
        if not is_valid_srx(title):
            continue

        alerts.append(
            f"🚗 SRX ALERT\n{item.get('title')}\n{item.get('url')}"
        )

    return alerts
