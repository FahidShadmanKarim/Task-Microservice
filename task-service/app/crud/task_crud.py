from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from app.models.task_model import Task
from app.schemas.user_schemas import TaskCreate,TaskUpdate,TaskResponse
from datetime import datetime
from typing import Optional,List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate


def create_task(db:Session,task:TaskCreate)->TaskResponse:

    task = Task(
        task_name = task.task_name,
        desciption = task.task_description,
        status=task.status,
        user_id = task.user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return TaskResponse(
        id = task.id,
        task_name = task.task_name,
        description = task.desciption,
        status = task.status,
    )

def get_task_by_id(db:Session, task_id:int)->Optional[TaskResponse]:

    task = db..query(Task).filter(Task.id == task.id).first()
    return TaskResponse.from_orm(task) if task else None

def get_tasks(db:Session) -> Page[TaskResponse]:

    query = db.query(Task)
    task = paginate(query)
    return task


#update task to be implemented




def delete_users(db:Session,task_id:int) -> bool:

    task = db.query(Task).filter(Task.id == task.id).first()
    if not task:
        return False
    db.delete(db_user)
    db.commit()
    return True


