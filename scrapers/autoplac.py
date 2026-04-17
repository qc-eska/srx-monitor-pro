import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT

urls = [
    "https://autoplac.pl/szukaj/cadillac/srx",
    "https://autoplac.pl/szukaj/honda/element"
]

BASE_URL = "https://autoplac.pl/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
}


def fetch_with_session(session, url):
    response = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    return response


def fetch_autoplac():
    listings = []
    session = requests.Session()
    session.headers.update(HEADERS)

    for URL in urls:
        try:
            r = fetch_with_session(session, URL)
        except requests.RequestException as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)

            if status_code == 403:
                try:
                    session.get(BASE_URL, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                    r = fetch_with_session(session, URL)
                except requests.RequestException as retry_exc:
                    print(f"Autoplac still blocked (403) for {URL}: {retry_exc}")
                    continue
            else:
                print(f"Autoplac fetch failed for {URL}: {exc}")
                continue

        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select("a"):
            href = item.get("href", "")
            text = item.get_text(" ", strip=True)

            # 🔥 filtr ogłoszeń
            if "/oferta/" not in href:
                continue

            if href and text:
                listings.append({
                    "title": text,
                    "price": "brak",
                    "url": href,
                })

    return listings
