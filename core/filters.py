def is_valid_srx(text: str) -> bool:
    text = (text or "").lower()

    # MUST HAVE
    if "srx" not in text:
        return False

    # BLOCKLIST (tu masz Ford C-Max fix)
    blocklist = [
        "c-max",
        "c max",
        "focus",
        "fiesta",
        "mondeo",
        "escort",
        "ka",
        "kuga",
        "s-max",
        "s max"
    ]

    for b in blocklist:
        if b in text:
            return False

    return True
