import sqlite3
from pathlib import Path
from typing import Iterable

DB_FILE = Path(__file__).resolve().parent / 'coi.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant TEXT NOT NULL,
    file_path TEXT NOT NULL,
    issue_date TEXT,
    expiration_date TEXT,
    raw_text TEXT
);
"""

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def insert_certificate(tenant: str, file_path: str, issue_date: str = None, expiration_date: str = None, raw_text: str = None) -> int:
    conn = get_connection()
    cur = conn.execute(
        'INSERT INTO certificates (tenant, file_path, issue_date, expiration_date, raw_text) VALUES (?, ?, ?, ?, ?)',
        (tenant, file_path, issue_date, expiration_date, raw_text)
    )
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def fetch_certificates() -> Iterable[sqlite3.Row]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM certificates').fetchall()
    conn.close()
    return rows
