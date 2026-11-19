from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas import CommentResponse, CommentCreate, CommentUpdate
from database import get_session
from models import Task, Comment

router = APIRouter(prefix='/db/tasks', tags=['comments'])

@router.get('/{task_id}/comments', response_model=list[CommentResponse])
def get_task_comments(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )

    return task.comments

@router.get('/{task_id}/comments/{comment_id}', response_model=CommentResponse)
def get_comment_task(task_id: int, comment_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )
    
    comment = session.get(Comment, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комментарий не найден'
        )

    if comment.task_id != task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комментарий для этой задачи не найден'
        )

    return comment

@router.post('/{task_id}/comments', status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
def create_comment_task(task_id: int, comment_data: CommentCreate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )

    try:
        new_comment = Comment(**comment_data.model_dump(), task_id=task_id)

        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )

    return new_comment

@router.patch('/{task_id}/comments/{comment_id}', response_model=CommentResponse)
def update_comment_task(task_id: int, comment_id: int, comment_data: CommentUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )

    comment = session.get(Comment, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комментарий не найден'
        )

    if comment.task_id != task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комментарий для этой задачи не найден'
        )

    updated_data = comment_data.model_dump(exclude_unset=True)

    try:
        if 'comment' in updated_data:
            comment.comment = updated_data['comment']

        session.commit()
        session.refresh(comment)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Во время обработки операции в БД произошла ошибка'
        )

    return comment

@router.delete('/{task_id}/comments/{comment_id}')
def delete_comment_task(task_id: int, comment_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )

    comment = session.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комментарий не найден'
        )

    if comment.task_id != task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комментарий для этой задачи не найден'
        )

    session.delete(comment)
    session.commit()

    return{'message': 'Comment has been deleted'}
    