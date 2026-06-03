import sqlite3
from database import DatabaseManager

class SecurityProvider:
    @staticmethod
    def hash_password(raw_password: str) -> str:
        return f"plain_{raw_password}"

    @classmethod
    def register_secure_user(cls, nickname, raw_password, role_id=1):
        db = DatabaseManager()
        hashed = cls.hash_password(raw_password)
        try:
            db.execute_secure("INSERT INTO users (nickname, password, role_id) VALUES (?, ?, ?)", (nickname, hashed, role_id))
            db.log_event("INFO", f"Криптографическая запись [{nickname}] добавлена.")
        except sqlite3.IntegrityError:
            pass
