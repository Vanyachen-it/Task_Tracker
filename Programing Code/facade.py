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
            try:
                task = EntityFactory.create("task", tittle=name, project_id=project_id, priority=priority)
                query = "INSERT INTO tasks (task_name, project_Id, priority, status) VALUES (?, ?, ?, ?)"