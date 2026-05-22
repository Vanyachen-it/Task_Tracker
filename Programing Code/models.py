from typing import Optional 
from database import DatabaseManager

class User:
    def __init__ (self, user_id: int, nickname: str, role: str, password_hash: str):
        self.id: int = user_id
        self.nickname: str = nickname
        self.role: str = role
        self.password: str = password_hash

    @staticmethod
    def get_role(user_id: int) -> str:
        db = DatabaseManager()
        query = "SELECT role FROM users WHERE id = ?"
        cursor - db.execute_secure(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else "user"
class Project:
    def __init__(self, project_id: int, project_name: str, owner_id: int):
        self.id = project_id
        self.project_name = project_nmae
        self.owner_id = owner_id

    @staticmethod
    def get_info_project(project_id: int) -> Optional[dict]:
        db = DatabaseManager()
        cursor = db.execute_secure("SELECT id, project_name, owner_id FROM projects WHERE id = ?")
        res = cursor.fetchone()
            if res:
                cursor.count = db.secure.execute("SELECT COUNT (DISTINCT executor_id) FROM tasks WHERE project_id = ?", (project_id())
                count= cursor_count.fetchone()[0] or 0
                return {"id": res[0], "name": res[1], "owner_id": res[2], "member_count": count}
            return None

class Task:
    def __init (self, task
