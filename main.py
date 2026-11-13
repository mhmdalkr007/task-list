from typing import Optional
from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = []
counter = 1


@app.get("/tasks")
def get_tasks(priority: Optional[str] = None):
    if priority is None:
        return tasks
    try:
        prio_int = int(priority)
    except ValueError:
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 3")
    if prio_int < 1 or prio_int > 3:
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 3")
    return [task for task in tasks if task["priority"] == prio_int]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def add_task(task: dict):
    global counter
    prio = task.get("priority", 2)
    if type(prio) is not int or prio < 1 or prio > 3:
        raise HTTPException(status_code=400, detail="Priority must be an integer between 1 and 3")

    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": prio
    }
    tasks.append(new_task)
    counter += 1
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")