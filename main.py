FORCE_RESEND_ONCE = False

from scrapers.olx import fetch_olx
from scrapers.otomoto import fetch_otomoto
from scrapers.autoplac import fetch_autoplac
from scrapers.sprzedajemy import fetch_sprzedajemy
from core.analyzer import scan_listings
from core.status import build_status_message, mark_status_sent, should_send_status
from telegram.bot import send_message
from database.db import mark_seen
from config import CHECK_INTERVAL
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
                scan_result = scan_listings(listings)
                alerts = scan_result["alerts"]

                for alert in alerts:
                    send_message(alert)

                print(
                    "Scan summary:",
                    f"scanned={len(listings)}",
                    f"active_matches={scan_result['matching_count']}",
                    f"new_alerts={scan_result['new_alerts_count']}",
                )

                if should_send_status():
                    sent = send_message(
                        build_status_message(
                            active_matches=scan_result["matching_count"],
                            scanned_count=len(listings),
                            new_alerts_count=scan_result["new_alerts_count"],
                        )
                    )
                    if sent:
                        mark_status_sent()

            print(f"Scan done: {len(listings)} listings")

        except Exception as e:
            print("ERROR:", e)
            send_message(f"⚠️ Błąd: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
