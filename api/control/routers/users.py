from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.control.database.database import get_session
from api.control.models.models import User
from api.control.schemas.users_schemas import (
    UserCreate,
    UserList,
    UserPublic,
    UserUpdate,
)
from api.control.schemas.utils_schemas import Message
from api.control.security.security import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# CRUD Users
@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserCreate, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exists",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already exists",
            )

    hashed_password = get_password_hash(user.password)
    user_id = len(session.scalars(select(User).offset(0).limit(100)).all()) + 1
    db_user = User(
        id=f"{user_id}",
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=UserList)
def read_users(session: T_Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: str,
    user: UserUpdate,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, 
            detail="Not enough permissions"
        )
    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user



@router.delete("/{user_id}", response_model=Message)
def delete_user(
    user_id: str, 
    session: T_Session, 
    current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    session.delete(current_user)
    session.commit()

    return {"message": "User deleted."}
