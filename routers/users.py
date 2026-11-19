from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas import UserResponse, UserCreate, UserUpdate, ProjectResponse
from database import get_session
from models import User

router = APIRouter(prefix='/db/users', tags=['users'])

@router.get('/', response_model=list[UserResponse])
def get_users(session: Session = Depends(get_session)):
    stmt = select(User).order_by(User.id)

    users = session.scalars(stmt).all()

    return users

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    return user

@router.get('/{user_id}/projects', response_model=list[ProjectResponse])
def get_user_projects(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    return user.projects

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    new_user = User(**user_data.model_dump())

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )


    return new_user

@router.patch('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    update_data = user_data.model_dump(exclude_unset=True)

    try:
        for field, value in update_data.items():
            setattr(user, field, value)

        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )

    return user

@router.delete('/{user_id}')
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    try:
        session.delete(user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )
    
    return {'message': 'The user has been deleted'}