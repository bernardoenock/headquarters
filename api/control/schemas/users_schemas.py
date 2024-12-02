from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]


class UserDb(UserCreate):
    id: str


class UserPublic(BaseModel):
    id: str
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]

