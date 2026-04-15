import sqlite3

conn = sqlite3.connect("srx.db", check_same_thread=False)
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
