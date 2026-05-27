import threading
from database import DatabaseManager
from models import EntityFactory

class TaskTrackerFacade:
    def __init__(self):
        self.db = DatabaseManager()

    def async_add_task_pipeline (self, name, project_id, priority, callback):
        def worker():
            if nor name or not project_id:
                self.db.log_event("WARNING", "Валидация отклонена: Пустые входящие данные формы UI")
                callback(False, "Поля не могут быть пустыми")
                return
            try:
                task = EntityFactory.create("task", tittle=name, project_id=project_id, priority=priority)
                query = "INSERT INTO tasks (task_name, project_Id, priority, status) VALUES (?, ?, ?, ?)"
                self.db.execute_secure(query, (task.tittle, task.project_id, task.priority, task.status))
                self.db.log_event("INFO", f"Добавлен узел: '{name}' через паттерн Facade")
                callback(True, "Успешно")
            except Exception as e:
                callback(False, str(e))
                
        threading.Thread(target=worker, daemon=True).start()
    def fetch_bi_metrics(self):
        cursor = self.db.execute_secure ("SELECT status, COUNT(*) FROM tasks GROUP BY status")
        return cursor.fetchall()
