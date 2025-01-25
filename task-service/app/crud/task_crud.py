import httpx
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.core.config import get_db
from datetime import datetime
from typing import Optional, List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: TaskCreate) -> TaskResponse:
        new_task = Task(
            task_name=task.task_name,
            user_id=task.user_id,
            board_id=task.board_id,
            description=task.task_description,
            status=task.status,
        )
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return TaskResponse.from_orm(new_task)

    async def get_task_by_id(self, task_id: int) -> Optional[TaskResponse]:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalar_one_or_none()
        return TaskResponse.from_orm(task) if task else None

    async def get_tasks(self) -> Page[TaskResponse]:
        query = select(Task)
        return await paginate(query, self.db)

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(task)
        return TaskResponse.from_orm(task)

    async def delete_task(self, task_id: int) -> bool:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return False
        await self.db.delete(task)
        await self.db.commit()
        return True

def get_task_repository(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)
