import re

def extract_year(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


def is_valid_srx(text: str):
    text = (text or "").lower()

    # 🚫 SRX II generacja (twarde blokady)
    blacklist = [
        "2010", "2011", "2012", "2013", "2014", "2015", "2016",
        "3.0",
        "3.6"
    ]

    if any(x in text for x in blacklist):
        return False

    # ✔ SRX I (mocny sygnał)
    if "4.6" in text:
        return True

    year = extract_year(text)

    if year:
        return 2004 <= year <= 2009

    return False
