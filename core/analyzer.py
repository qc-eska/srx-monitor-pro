def analyze_listings(listings):
    alerts = []

    for item in listings:
        # na start każdy nowy element = alert testowy
        if item.get("new"):
            alerts.append(
                f"🚗 NOWE OGŁOSZENIE\n{item.get('title','brak')}\n{item.get('price','brak')}\n{item.get('url','')}"
            )

    return alerts
