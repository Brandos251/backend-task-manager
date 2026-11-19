from fastapi import APIRouter,HTTPException, status, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas import ProjectResponse, ProjectCreate, ProjectUpdate, TaskResponse
from database import get_session
from models import Project, User

router = APIRouter(prefix='/db/projects', tags=['projects'])

@router.get('/', response_model=list[ProjectResponse])
def get_projects(is_archived: bool | None = None ,session: Session = Depends(get_session)):
    stmt = select(Project).order_by(Project.id)

    if is_archived is not None:
        stmt = stmt.where(Project.is_archived == is_archived)

    projects = session.scalars(stmt).all()

    return projects

@router.get('/{project_id}', response_model=ProjectResponse)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден'
        )

    return project

@router.get('/{project_id}/tasks', response_model=list[TaskResponse])
def get_project_tasks(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден'
        )

    return project.tasks
    

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, session: Session = Depends(get_session)):
    owner = session.get(User, project_data.owner_id)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    try:
        new_project = Project(**project_data.model_dump())

        session.add(new_project)
        session.commit()
        session.refresh(new_project)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )

    return new_project

@router.patch('/{project_id}', response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден'
        )

    update_data = project_data.model_dump(exclude_unset=True)

    if 'owner_id' in update_data:
        owner = session.get(User, update_data['owner_id'])

        if owner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Пользователь не найден'
            )

    try:
        for field, value in update_data.items():
            setattr(project, field, value)

        session.commit()
        session.refresh(project)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время операции в БД произошла ошибка'
        )

    return project

@router.delete('/{project_id}')
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден'
        )

    try:
        session.delete(project)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время операции в БД произошла ошибка'
        )

    return{"message": 'Project has been deleted'}