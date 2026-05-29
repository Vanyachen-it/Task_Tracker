import sqlite3
import threading
import datetime
from config import DATABASE_NAME

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

def __new__(cls):
    with cls._lock:
        if cls._instance is None:
            cls._instance = super (DatabaseManager, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
            cls._instance.conn = execute("PRAGMA foreign_keys = ON;")
            cls._instance.conn = execute("PRAGMA journal_mode = WAL;")
            cls._instance.create_tables()
        return cls._instance

def create_tables(self):
    with self._lock:
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS roles(id INTEGER PRIMATY KEY AUTOINCREMENT, role_name TEXT UNIQUE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMATY KEY AUTOINCREMENT, nickname TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role_id INTEGER, FOREIGN KEY (role_id) REFERENCES roles(id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS user_profiles (id INTEGER PRIMATY KEY AUTOINCREMENT, user_id INTEGER UNIQUE NOT NULL, full_name TEXT, enail TEXT, FOREIGN KEY (user_id) REFERENCES  users(id) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMATY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMATY KEY AUTOINCREMENT, project_name TEXT NOT NULL, owner_id INTEGER NOT NULL, category_id INTEGER, FOREIGHN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY (catery_id) REFERENCES categories(id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMATY KEY AUTOINCREMENT, task_name TEXT NO NULL, status TEXT NOT NULL DEFAULT 'New', project_id INTEGER NOT NULL, executor_id INTEGER, priority TETX DEFAULT 'Medium', created_at TEXT DEFAULT (date('now')), FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE, FOREIGN KEY (executor_id) REFERENCES users(id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS
        cursor.execute("CREATE TABLE IF NOT EXISTS
        cursor.execute("CREATE TABLE IF NOT EXISTS
        cursor.execute("CREATE TABLE IF NOT EXISTS
            
