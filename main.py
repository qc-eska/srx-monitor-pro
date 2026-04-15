from telegram.bot import send_alert
import time

def run():
    send_alert("🚗 TEST: SRX monitor działa 24/7")
    print("TEST sent to Telegram")

    while True:
        print("Scan done... waiting 30 min")
        time.sleep(1800)

if __name__ == "__main__":
    run()
