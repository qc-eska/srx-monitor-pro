import sqlite3
from pathlib import Path

from config import SEEN_DB_PATH


db_path = Path(SEEN_DB_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS seen (
    url TEXT PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

conn.commit()


def is_seen(url):
    cursor.execute("SELECT url FROM seen WHERE url=?", (url,))
    return cursor.fetchone() is not None


def mark_seen(url):
    cursor.execute("INSERT OR IGNORE INTO seen VALUES (?)", (url,))
    conn.commit()


def get_meta(key):
    cursor.execute("SELECT value FROM meta WHERE key=?", (key,))
    row = cursor.fetchone()
    return row[0] if row else None


def set_meta(key, value):
    cursor.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()
