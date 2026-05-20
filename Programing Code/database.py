import sqlite3
import threading

class Manager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(
                'taskflow.db',
                check_sane_thread=False
            )
            cls._instance.create_tables()
            cls._instance.create_tables()
        return cls._instance
        
def create_table(self):
cursor = self.conn.cursor()

cursor.execute ("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
task_name TEXT MOT NULL,
status TEXT NOT NULL DEFAULT 'NEW',
project_id INTEGER NOT NULL,
executor_id INTEGER,
FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE,
FOREIGN KEY (executor_id) REFERENCES users(id)
);
""")

self.conn.commit()

def execute_secure(self, query, params =()):
    cursor = self.conn.cursor()
    try:
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(self.conn.rollback())
        raise e
