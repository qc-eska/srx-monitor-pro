import re

def extract_year(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


def is_valid_srx(item):
    text = (item.get("title", "") + " " + item.get("url", "")).lower()

    # 🚫 twarde blokady SRX II generacji
    blacklist = [
        "2010", "2011", "2012", "2013", "2014", "2015", "2016",
        "3.0",  # bardzo często SRX II
        "3.6"   # SRX II najczęściej
    ]

    if any(x in text for x in blacklist):
        return False

    # 🚫 dodatkowa heurystyka (SRX I ma V8 4.6)
    if "4.6" in text:
        return True

    year = extract_year(text)

    if year:
        return 2004 <= year <= 2009

    # 🔥 jeśli brak danych → NIE ufamy SRX II
    return False
