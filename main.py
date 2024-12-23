from fastapi import FastAPI, HTTPException  # Основной модуль для создания API
from pydantic import BaseModel  # Для валидации данных моделей
import json  # Для работы с файлами JSON
import os  # Для проверки существования файлов
from contextlib import asynccontextmanager  # Для управления ресурсами в FastAPI

"""
Чтобы проверить API (задеплоенное на сервер) на безопасность:
1. Поменяйте значение API_KEY = '' на ваше значение API-ключа VirusTotal.
2. Введите в консоли: from api_healthcheck import check_url_safety либо импортируйте в зависимости основного модуля и при запуске ваша ссылка будет автоматически проверяться,
   но перед этим убедитесь, что вы поменяли ссылку в переменной result,
   например result = check_url_safety("тут должна быть ссылка на проверяемый сайт/API")
"""

TASKS_FILE = "tasks.txt"  # Имя файла для хранения задач
tasks = []  # Список задач

# Модель задачи
class Task(BaseModel):
    title: str  # Название задачи
    priority: str  # Приоритет задачи (low, normal, high)
    id: int = 0  # Уникальный идентификатор задачи
    isDone: bool = False  # Статус выполнения задачи

# Загрузка задач из файла
def load_tasks():
    """
    Загружает список задач из файла TASKS_FILE aka tasks.txt
    Если файл существует и не пустой, его содержимое добавляется в список tasks
    """
    global tasks
    if os.path.exists(TASKS_FILE) and os.path.getsize(TASKS_FILE) > 0:
        with open(TASKS_FILE, "r") as file:
            tasks.extend(json.load(file))

# Сохранение задач в файл
def save_tasks():
    """
    Сохраняет текущий список задач в файл TASKS_FILE в формате JSON
    """
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Генерация уникального ID
def generate_id():
    """
    Генерирует уникальный идентификатор для новой задачи
    Возвращает максимальный текущий ID + 1 или 1, если список задач пуст
    """
    return max([task["id"] for task in tasks], default=0) + 1

# Контекстный менеджер для работы приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Загружает задачи при старте приложения и сохраняет их при завершении
    """
    load_tasks()
    yield
    save_tasks()

# Создание приложения FastAPI
app = FastAPI(lifespan=lifespan)

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    """
    Создаёт новую задачу и добавляет её в список
    Пример POST-запроса:
    {
        "title": "New Task",
        "priority": "high"
    }
    """
    task.id = generate_id()  # Генерация ID
    task.isDone = False  # Установка статуса по умолчанию
    tasks.append(task.dict())  # Добавление задачи в список
    save_tasks()  # Сохранение в файл
    return task  # Возврат созданной задачи

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """
    Возвращает список всех задач
    Пример ответа:
    [
        {
            "title": "Task 1",
            "priority": "low",
            "id": 1,
            "isDone": false
        }
    ]
    """
    return tasks

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    """
    Отмечает задачу с заданным ID как выполненную
    Возвращает сообщение об успешной операции или ошибку 404, если задача не найдена
    """
    for task in tasks:
        if task["id"] == task_id:
            task["isDone"] = True
            save_tasks()
            return {"message": "Task marked as completed"}
    raise HTTPException(status_code=404, detail="Task not found")  # Если задача не найдена

if __name__ == "__main__":
    import uvicorn  # Сервер для запуска приложения
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Запуск приложения


