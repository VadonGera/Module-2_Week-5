import uuid
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI(title="Ups Aps")
tasks = {}


class Task(BaseModel):
    duration: int


async def task_worker(task_id, duration):
    print()
    print(f'Запуск задачи {task_id}')
    await asyncio.sleep(duration)  # Спим
    tasks[task_id] = "done"  # Устанавливаем статус задачи как "done"
    print(f'Остановка задачи {task_id}')
    print("================================================")
    for key, value in tasks.items():  # После остановки какой либо задачи смотрим список завершенных и работающих задач
        print(f'{key} - {value}')


@app.post("/task", response_model=dict)
async def create_task(task: Task):
    task_id = str(uuid.uuid4())  # Генерируем уникальный идентификатор для задачи
    tasks[task_id] = "running"  # Устанавливаем статус задачи как "running"
    try:
        asyncio.create_task(task_worker(task_id, task.duration))
    except asyncio.CancelledError:
        print("Задача отменена.")
    return JSONResponse(content={"task_id": task_id})  # Возвращаем уникальный идентификатор задачи


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    return {"status": tasks[task_id]}  # Получаем статус задачи
