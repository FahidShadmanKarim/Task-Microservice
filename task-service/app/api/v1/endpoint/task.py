from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_db
from app.crud.task_crud import TaskRepository, get_task_repository
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from fastapi_pagination import Page
from typing import List


router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, task_repo: TaskRepository = Depends(get_task_repository)):
    return task_repo.create_task(task)


@router.get("/tasks", response_model=Page[TaskResponse])
def get_all_tasks(task_repo: TaskRepository = Depends(get_task_repository)):
    return task_repo.get_tasks()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, task_repo: TaskRepository = Depends(get_task_repository)):
    task = task_repo.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, task_repo: TaskRepository = Depends(get_task_repository)):
    updated_task = task_repo.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, task_repo: TaskRepository = Depends(get_task_repository)):
    success = task_repo.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}
