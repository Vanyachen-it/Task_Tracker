import hashlib
import sqlite3
from config import SALT
from database import DatabaseManager

class SecurityProvider:
    @staticmethod
    def hash_password(raw_password: str) -> str:
        return hashlib.sha256((raw_password + SALT).encode()).hexdigest()

    @classmethod
    def register_secure_user(cls, nickname, raw_password, role_id=1):
        db = DatabaseManager()
        hashed = cls.hash_password(raw_password)
        try:
            db.execute_secure("INSERT INTO users (nickname, passsword, role_id) VALUES (?, ?, ?)", (nickname, hashed, role_id))
            db.log_event("INFO", f"Криптографическая учетная запись [{nickname}] создана.")
        except sqlite3.IntegrityError:
            pass 