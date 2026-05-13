from typing import Optional 

class User:
    def __init__ (self, user_id: int, nickname: str, role: str, password_hash: str):
        self.id: int = user_id
        self.nickname: str = nickname
        self.role: str = role
        self.password: str = password_hash
    def login(self) -> bool:
        return True
    def get_role(self) -> str:
        return self.role
        
class Project:
    def __init__(self, project_id: int, project_name: str, owned_id: int):
    self.id: int = project_id
    self.project_name: str = project_name
    self.owner_id: int = owner_id

class Task:
    def __init__(self, task_id: int, title: str, project_id: int, executor_id: Optional[int] = None, status: str = "New"):
        self.id: int = task_id
        self.title: str = title
        self.project_id: int = project_id
        self.executor_id: Optional[int]
        self.status: str = status
