import sqlite3

class Manager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect('taskflow.db', check_sane_thread=False)
            