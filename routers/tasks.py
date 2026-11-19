from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas import TaskResponse, TaskUpdate, TaskCreate
from database import get_session
from models import Task, Project

router = APIRouter(prefix='/db/tasks', tags=['tasks'])

@router.get("/", response_model=list[TaskResponse])
def get_tasks(session: Session = Depends(get_session)):
    stmt = select(Task).order_by(Task.id)
    tasks = session.scalars(stmt).all()

    return tasks

@router.get('/{task_id}', response_model=TaskResponse)
def get_task(task_id: int, session: Session=Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Задача не найдена")        
    return task

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    project = session.get(Project, task_data.project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден')

    try:
        new_task = Task(**task_data.model_dump())

        session.add(new_task)
        session.commit()
        session.refresh(new_task)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка')

    return new_task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int,task_data: TaskUpdate,session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    if "project_id" in update_data:
        project = session.get(Project, update_data["project_id"])

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )

    try:
        for field, value in update_data.items():
            setattr(task, field, value)

        session.commit()
        session.refresh(task)
    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )
    return task

@router.delete('/{task_id}')
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )

    session.delete(task)
    session.commit()

    return {"message": "Task has been deleted"}


    