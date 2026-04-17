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

conn.commit()


def is_seen(url):
    cursor.execute("SELECT url FROM seen WHERE url=?", (url,))
    return cursor.fetchone() is not None


def mark_seen(url):
    cursor.execute("INSERT OR IGNORE INTO seen VALUES (?)", (url,))
    conn.commit()
