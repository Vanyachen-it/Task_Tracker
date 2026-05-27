class TaskEntity:
    def __init__(self, title, project_id, priority, status="New"):
        self.title = title
        self.project_id = project_id
        self.priority = priority
        self.status = status 

class EntityFactory:
    @staticmethod
    def create(entity_type: str, **kwargs):
        if entity_type == "task":
            return TaskEntity(kwargs.get("title"), kwargs.get("project_id"), kwargs.get("priority"))
        raise ValueError(f"Фабрика не может создать тип: {entity_type}")
