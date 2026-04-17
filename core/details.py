import re
import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract_year_from_text(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


def fetch_listing_year(url: str):
    """
    Wchodzi w ogłoszenie i próbuje wyciągnąć rok produkcji.
    Zwraca int lub None.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "lxml")

        # 🔥 1. Spróbuj znaleźć po labelach (Otomoto / OLX style)
        labels = soup.find_all(text=re.compile("Rok produkcji", re.I))
        for label in labels:
            parent = label.parent
            if parent:
                value = parent.find_next(text=True)
                year = extract_year_from_text(value)
                if year:
                    return year

        # 🔥 2. fallback: cały tekst strony
        full_text = soup.get_text(" ", strip=True)
        return extract_year_from_text(full_text)

    except requests.RequestException:
        return None
