import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("runs.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        passed INTEGER,
        failed INTEGER,
        error_rate REAL
    )""")
    conn.commit()
    conn.close()

def save_run(passed, failed):
    conn = sqlite3.connect("runs.db")
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    error_rate = failed / (passed + failed) if (passed + failed) > 0 else 0
    c.execute("INSERT INTO runs (timestamp, passed, failed, error_rate) VALUES (?, ?, ?, ?)",
              (timestamp, passed, failed, error_rate))
    conn.commit()
    conn.close()
