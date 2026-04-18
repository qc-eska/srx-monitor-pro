import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import REQUEST_TIMEOUT

urls = [
    "https://autoplac.pl/oferty/samochody-osobowe/cadillac/srx",
    "https://autoplac.pl/oferty/samochody-osobowe/honda/element",
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
    "Referer": BASE_URL,
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}


def fetch_with_session(session, url):
    response = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    return response


def fetch_autoplac():
    listings = []
    seen_links = set()
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        session.get(BASE_URL, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except requests.RequestException:
        pass

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

        for item in soup.select("a[href]"):
            href = item.get("href", "")
            text = item.get_text(" ", strip=True)

            # 🔥 filtr ogłoszeń
            if "/oferta/" not in href:
                continue

            full_url = urljoin(BASE_URL, href.split("?")[0])

            if full_url in seen_links or not text:
                continue

            seen_links.add(full_url)
            listings.append({
                "title": text,
                "price": "brak",
                "url": full_url,
            })

    return listings
