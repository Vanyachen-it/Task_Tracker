import sqlite3
from flask import Flask, render_template_string, request, redirect
from database import DatabaseManager
from security import SecurityProvider
from facade import TaskTrackerFacade

app = Flask(__name__)
db = DatabaseManager()
facade = TaskTrackerFacade()

try:
    db.execute_secure("INSERT OR IGNORE INTO roles (id, role_name) VALUES (1, 'Admin')")
    SecurityProvider.register_secure_user("Иван Кашко", "secure_root_2026", 1)
    db.execute_secure("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Архитектура ПО')")
    db.execute_secure("INSERT OR IGNORE INTO projects (id, project_name, owner_id, category_id) VALUES (1, 'Репозиторий Ивана Кашко', 1, 1)")
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
        button { background-color: #1f6aa5; border: none; font-weight: bold; cursor: pointer; transition: 0.2s; }
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
    def cb(success, msg): pass
    facade.async_add_task_pipeline(name, project_id, priority, cb)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
