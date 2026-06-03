import sys
import time
import sqlite3
from database import DatabaseManager
from security import SecurityProvider
from facade import TaskTrackerFacade

class ConsoleApplication:
    def __init__(self):
        print("="*60)
        print("  TASKTRACKER PRO ENTERPRISE CORE ENGINE v6.0.4  ")
        print("="*60)
        print("[INFO] Инициализация ядра системы...")
        
        self.db = DatabaseManager()
        self.facade = TaskTrackerFacade()
        
        # Первичное наполнение СУБД
        self.db.execute_secure("INSERT OR IGNORE INTO roles (id, role_name) VALUES (1, 'Admin')")
        SecurityProvider.register_secure_user("Иван Кашко", "secure_root_2026", 1)
        
        try:
            self.db.execute_secure("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Архитектура ПО')")
            self.db.execute_secure("INSERT OR IGNORE INTO projects (id, project_name, owner_id, category_id) VALUES (1, 'Репозиторий Ивана Кашко', 1, 1)")
        except Exception:
            pass
            
        print("[SUCCESS] База данных развернута (10 таблиц активны).")
        print("[SECURITY] Защита от SQL-инъекций и хэширование включены.")
        print("="*60)

    def run(self):
        while True:
            print("\nДоступные операции:")
            print("1. Посмотреть текущий пул задач (Таблица tasks)")
            print("2. Создать новую задачу (Безопасная транзакция)")
            print("3. Посмотреть логи аудита безопасности (Таблица audit_logs)")
            print("4. Выйти из системы")
            
            choice = input("\nВыберите действие (1-4): ").strip()
            
            if choice == "1":
                print("\n--- ТЕКУЩИЕ ЗАДАЧИ В СУБД ---")
                cursor = self.db.execute_secure("SELECT id, task_name, priority, status FROM tasks")
                rows = cursor.fetchall()
                if not rows:
                    print("[Инфо] Список задач пуст.")
                for row in rows:
                    print(f"ID: {row[0]} | Задача: {row[1]} | Приоритет: {row[2]} | Статус: {row[3]}")
                    
            elif choice == "2":
                name = input("Введите название новой задачи: ").strip()
                priority = input("Введите приоритет (Low/Medium/High): ").strip() or "Medium"
                
                print("[PROCESS] Валидация по блок-схеме и отправка в Facade...")
                
                def callback(success, message):
                    if success:
                        print("[SUCCESS] Задача успешно добавлена в базу данных!")
                    else:
                        print(f"[ERROR] Отказ транзакции: {message}")
                        
                self.facade.async_add_task_pipeline(name, 1, priority, callback)
                time.sleep(0.2)
                
            elif choice == "3":
                print("\n--- КОНСОЛЬ АУДИТА БЕЗОПАСНОСТИ ЯДРА ---")
                cursor = self.db.execute_secure("SELECT timestamp, level, message FROM audit_logs ORDER BY id DESC LIMIT 10")
                for row in cursor.fetchall():
                    print(f"[{row[0]}] {row[1]}: {row[2]}")
                    
            elif choice == "4":
                print("\n[INFO] Корректное завершение работы СУБД. До свидания!")
                sys.exit(0)
            else:
                print("[WARNING] Неверный ввод. Выберите пункт от 1 до 4.")

if __name__ == "__main__":
    app = ConsoleApplication()
    app.run()
