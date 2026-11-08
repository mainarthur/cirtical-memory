"""Database layer configured according to ADR-003 (SQLite)."""
import sqlite3


class Database:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        return self
