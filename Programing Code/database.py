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
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance = super(DatabaseManager, cls).new(cls)
                cls._instance.conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
                cls._instance.conn.execute("PRAGMA foreign_keys = ON;")
                cls._instance.conn.execute("PRAGMA journal_mode = WAL;")
                cls._instance.create_tables()
        return cls._instance

    def create_tables(self):
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS roles (id INTEGER PRIMARY KEY AUTOINCREMENT, role_name TEXT UNIQUE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role_id INTEGER, FOREIGN KEY (role_id) REFERENCES roles(id));")
            cursor.execute("CREATE TABLE IF NOT EXISTS user_profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE NOT NULL, full_name TEXT, email TEXT, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT NOT NULL, owner_id INTEGER NOT NULL, category_id INTEGER, FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY (category_id) REFERENCES categories(id));")
            cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'New', project_id INTEGER NOT NULL, executor_id INTEGER, priority TEXT DEFAULT 'Medium', created_at TEXT DEFAULT (date('now')), FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE, FOREIGN KEY (executor_id) REFERENCES users(id));")
            cursor.execute("CREATE TABLE IF NOT EXISTS time_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id INTEGER NOT NULL, hours REAL, FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS task_comments (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id INTEGER NOT NULL, text TEXT, FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, msg TEXT, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, level TEXT, message TEXT, timestamp TEXT);")
            self.conn.commit()

    def execute_secure(self, query, params=()):
        with self._lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                self.conn.commit()
                return cursor
            except sqlite3.Error as e:
                self.conn.rollback()
                self.log_event("CRITICAL", f"Database Error: {str(e)}")
                raise e

    def log_event(self, level, message):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO audit_logs (level, message, timestamp) VALUES (?, ?, ?)", (level, message, now))
            self.conn.commit()                  