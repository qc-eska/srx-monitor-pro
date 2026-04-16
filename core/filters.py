import re


def extract_year(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


# ========================
# SRX (2004–2009)
# ========================
def is_valid_srx(text: str):
    text = (text or "").lower()

    blacklist = [
        "2010", "2011", "2012", "2013", "2014", "2015", "2016",
        "3.0",
        "3.6"
    ]

    if any(x in text for x in blacklist):
        return False

    if "4.6" in text:
        return True

    year = extract_year(text)

    if year:
        return 2004 <= year <= 2009

    return False


# ========================
# HONDA ELEMENT
# ========================
def is_valid_element(text: str):
    text = (text or "").lower()

    if "element" not in text:
        return False

    if "honda" not in text:
        return False

    blacklist = [
        "diesel",
        "2.2",
        "cdti"
    ]

    if any(x in text for x in blacklist):
        return False

    return True


# ========================
# GLOBAL FILTER
# ========================
def is_valid_listing(text: str):
    return (
        is_valid_srx(text)
        or is_valid_element(text)
    )
