import re


def extract_year(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


# ========================
# SRX — tylko SRX jako model
# ========================
def is_valid_srx(text: str):
    text = (text or "").lower()

    # 🔥 musi być dokładnie "srx" jako słowo
    if not re.search(r"\bsrx\b", text):
        return False

    # 🔥 SRX II OUT
    if any(x in text for x in ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]):
        return False

    # 🔥 SRX I pewniak
    if "4.6" in text:
        return True

    year = extract_year(text)

    if year:
        return 2004 <= year <= 2009

    return True


# ========================
# HONDA ELEMENT — dokładna fraza
# ========================
def is_valid_element(text: str):
    text = (text or "").lower()

    # 🔥 musi być dokładnie "honda element"
    if "honda element" not in text:
        return False

    return True


# ========================
# GLOBAL
# ========================
def is_valid_listing(text: str):
    return (
        is_valid_srx(text)
        or is_valid_element(text)
    )
