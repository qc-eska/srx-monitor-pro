FORCE_RESEND_ONCE = True

from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from scrapers.autoplac import fetch_autoplac
from scrapers.sprzedajemy import fetch_sprzedajemy
from core.analyzer import analyze_listings
from telegram.bot import send_message
from database.db import mark_seen
import time


def run():
    global FORCE_RESEND_ONCE

    send_message("🚗 SRX monitor uruchomiony (PRO 24/7)")

    while True:
        try:
            listings = []

            listings += fetch_olx()
            listings += fetch_otomoto()
            listings += fetch_autoplac()
            listings += fetch_sprzedajemy()

            print("TOTAL:", len(listings))

            # 🔥 TRYB JEDNORAZOWEGO RESEND
            if FORCE_RESEND_ONCE:
                print("🔥 FORCE RESEND ACTIVE")

                for item in listings:
                    url = item.get("url")

                    if not url:
                        continue

                    send_message(
                        f"🔁 RESEND\n{item.get('title')}\n{item.get('price')}\n{url}"
                    )

                    # oznacz jako seen
                    mark_seen(url)

                FORCE_RESEND_ONCE = False

            else:
                alerts = analyze_listings(listings)

                for alert in alerts:
                    send_message(alert)

            print(f"Scan done: {len(listings)} listings")

        except Exception as e:
            print("ERROR:", e)
            send_message(f"⚠️ Błąd: {e}")

        time.sleep(1800)


if __name__ == "__main__":
    run()
