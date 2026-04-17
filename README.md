# SRX Monitor Pro

Bot monitoruje nowe ogloszenia z kilku serwisow i wysyla dopasowania na Telegram.

## Wymagane zmienne srodowiskowe

- `TELEGRAM_TOKEN` - token bota Telegram
- `CHAT_ID` - docelowy chat lub kanal
- `CHECK_INTERVAL` - odstep miedzy kolejnymi skanami w sekundach, domyslnie `1800`
- `REQUEST_TIMEOUT` - timeout zapytan HTTP w sekundach, domyslnie `15`
- `SEEN_DB_PATH` - sciezka do pliku SQLite z juz widzianymi ogloszeniami

## Railway

Na Railway warto ustawic `SEEN_DB_PATH` na sciezke w wolumenie, na przyklad `/data/srx.db`.
Bez trwalego wolumenu plik SQLite moze zostac utracony po restarcie lub redeploymencie, co spowoduje ponowne wysylanie starszych ogloszen.

## Start

```bash
pip install -r requirements.txt
python main.py
```
