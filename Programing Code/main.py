import sqlite3
import threading
import datetime
from flask import Flask, render_template_string, request, redirect

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance.conn = sqlite3.connect('taskflow.db', check_same_thread=False)
                cls._instance.conn.execute("PRAGMA foreign_keys = ON;")
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
            cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'New', project_id INTEGER NOT NULL, priority TEXT DEFAULT 'Medium', created_at TEXT DEFAULT (date('now')), FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE, FOREIGN KEY (executor_id) REFERENCES users(id));")
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

class TaskEntity:
    def __init__(self, title, project_id, priority, status="New"):
        self.title = title
        self.project_id = project_id
        self.priority = priority
        self.status = status

class EntityFactory:
    @staticmethod
    def create(**kwargs):
        return TaskEntity(kwargs.get("title"), kwargs.get("project_id"), kwargs.get("priority"))

class TaskTrackerFacade:
    def __init__(self):
        self.db = DatabaseManager()

    def add_task_pipeline(self, name, project_id, priority):
        if not name or not project_id:
            self.db.log_event("WARNING", "Валидация отклонена: пустые поля UI формы.")
            return False
        try:
            task = EntityFactory.create(title=name, project_id=project_id, priority=priority)
            query = "INSERT INTO tasks (task_name, project_id, priority, status) VALUES (?, ?, ?, ?)"
            self.db.execute_secure(query, (task.title, task.project_id, task.priority, task.status))
            self.db.log_event("INFO", f"Добавлен узел: '{name}' через паттерн Facade")
            return True
        except Exception as e:
            self.db.log_event("CRITICAL", f"Ошибка СУБД: {str(e)}")
            return False

app = Flask(__name__)
db = DatabaseManager()
facade = TaskTrackerFacade()

# Первичный запуск данных ядра
db.execute_secure("INSERT OR IGNORE INTO roles (id, role_name) VALUES (1, 'Admin')")
try:
    db.execute_secure("INSERT OR IGNORE INTO users (id, nickname, password, role_id) VALUES (1, 'Иван Кашко', 'plain_root_2026', 1)")
    db.execute_secure("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Архитектура ПО')")
    db.execute_secure("INSERT OR IGNORE INTO projects (id, project_name, owner_id, category_id) VALUES (1, 'Репозиторий Ивана Кашко', 1, 1)")
    db.log_event("INFO", "Система успешно инициализирована.")
except Exception:
    pass

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>TaskTracker Pro Enterprise</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #1e1e1e; color: #fff; margin: 30px; }
        .container { display: flex; gap: 30px; max-width: 1200px; margin: 0 auto; }
        .panel { flex: 1; background: #2d2d2d; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        h1, h2 { color: #58a6ff; margin-top: 0; }
        input, select, button { width: 100%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #444; background: #1f1f1f; color: white; box-sizing: border-box; }
        button { background-color: #1f6aa5; border: none; font-weight: bold; cursor: pointer; }
        button:hover { background-color: #144871; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #444; }
        th { background-color: #383838; color: #58a6ff; }
        .console { background-color: #101010; color: #2ecc71; font-family: 'Courier New', monospace; padding: 15px; border-radius: 6px; height: 200px; overflow-y: auto; font-size: 13px; }
    </style>
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 40px;">TaskTracker Enterprise System v6.0</h1>
    <div class="container">
        <div class="panel">
            <h2>Регистрация задач (Валидация по Блок-схеме)</h2>
            <form action="/add" method="POST">
                <input type="text" name="name" placeholder="Спецификация новой задачи..." required>
                <input type="number" name="project_id" value="1" placeholder="ID Проекта">
                <select name="priority">
                    <option value="Low">Low</option>
                    <option value="Medium" selected>Medium</option>
                    <option value="High">High</option>
                </select>
                <button type="submit">Выполнить безопасную транзакцию</button>
            </form>
            <h2>Локальный пул задач из SQLite</h2>
            <table>
                <tr><th>ID</th><th>Узел задачи</th><th>Приоритет</th><th>Статус</th></tr>
                {% for row in tasks %}
                <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td></tr>
                {% endfor %}
            </table>
        </div>
        <div class="panel">
            <h2>Аналитическое ядро (Data Science)</h2>
            <p style="color: #8b949e; font-style: italic">Статус СУБД: <span style="color: #2ecc71">Активна (10 Таблиц)</span></p>
            <div style="background: #383838; height: 10px; border-radius: 5px; margin-bottom: 25px;"><div style="background: #2ecc71; width: 85%; height: 100%; border-radius: 5px;"></div></div>
            <h2>Консоль аудита безопасности (Лог транзакций)</h2>
            <div class="console">
                {% for log in logs %}
                <div>[{{ log[0] }}] {{ log[1] }}: {{ log[2] }}</div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    cursor = db.execute_secure("SELECT id, task_name, priority, status FROM tasks")
    tasks = cursor.fetchall()
    cursor_logs = db.execute_secure("SELECT timestamp, level, message FROM audit_logs ORDER BY id DESC LIMIT 15")
    logs = cursor_logs.fetchall()
    return render_template_string(HTML_TEMPLATE, tasks=tasks, logs=logs)

@app.route('/add', methods=['POST'])
def add_task():
    name = request.form.get('name')
    project_id = int(request.form.get('project_id', 1))
    priority = request.form.get('priority')
    facade.add_task_pipeline(name, project_id, priority)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
