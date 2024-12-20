from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.control.database.database import get_session
from api.control.models.models import Todo, User
from api.control.schemas.todos_schemas import (
  TodoList,
  TodoPublic,
  TodoSchema,
  TodoUpdate
) 
from api.control.schemas.utils_schemas import Message
from api.control.security.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', response_model=TodoPublic)
def create_todo(
  todo: TodoSchema,
  user: CurrentUser,
  session: T_Session
):
  
  todo_id = len(session.scalars(select(Todo).offset(0).limit(100)).all()) + 1
  db_todo: Todo = Todo(
    id=todo_id,
    title=todo.title,
    description=todo.description,
    state=todo.state,
    user_id=user.id,
  )
  session.add(db_todo)
  session.commit()
  session.refresh(db_todo)

  return db_todo

@router.get('/', response_model=TodoList)
def list_todos(
  session: T_Session,
  user: CurrentUser,
  title: str = Query(None),
  description: str = Query(None),
  state: str = Query(None),
  offset: int = Query(None),
  limit: int = Query(None),
):
  query = select(Todo).where(Todo.user_id == user.id)

  if title:
    query = query.filter(Todo.title.contains(title))

  if description:
    query = query.filter(Todo.description.contains(description))

  if state:
    query = query.filter(Todo.state == state)

  todos = session.scalars(query.offset(offset).limit(limit)).all()

  return {'todos': todos}
  

@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
  todo_id: str, session: T_Session, user: CurrentUser, todo: TodoUpdate
):
  db_todo = session.scalar(
    select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
  )

  if not db_todo:
    raise HTTPException(
      status_code=HTTPStatus.NOT_FOUND,
      detail='Task not found.'
    )
  
  for key, value in todo.model_dump(exclude_unset=True).items():
    setattr(db_todo, key, value)

  session.add(db_todo)
  session.commit()
  session.refresh(db_todo)

  return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: str, session: T_Session, user: CurrentUser):
  todo = session.scalar(
    select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
  )

  if not todo:
    raise HTTPException(
      status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
    )
  
  session.delete(todo)
  session.commit()

  return {'message': 'Task has been deleted successfully.'}