import re


def extract_year(text: str):
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else None


PREFERRED_SRX_MARKERS = [
    "4.6",
    "4,6",
    "v8",
    "northstar",
]

GEN2_SRX_MARKERS = [
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "ii gen",
    "2 gen",
    "second gen",
    "second generation",
    "2010+",
]


# ========================
# SRX — tylko SRX jako model
# ========================
def is_valid_srx(text: str):
    text = (text or "").lower()

    # 🔥 musi być dokładnie "srx" jako słowo
    if not re.search(r"\bsrx\b", text):
        return False

    # 🔥 SRX II OUT
    if any(marker in text for marker in GEN2_SRX_MARKERS):
        return False

    # 🔥 SRX I V8 / 4.6 — najwyzszy priorytet
    if any(marker in text for marker in PREFERRED_SRX_MARKERS):
        return True

    # 🔥 3.6 przepuszczamy, ale tylko dla SRX I
    if "3.6" in text or "3,6" in text:
        year = extract_year(text)
        if year:
            return 2004 <= year <= 2009
        return True

    year = extract_year(text)

    if year:
        return 2004 <= year <= 2009

    # 🔥 bez rocznika i bez oznaczen silnika wolimy byc ostrozni
    return False


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
