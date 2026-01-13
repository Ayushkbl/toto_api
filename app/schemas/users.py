from sqlmodel import SQLModel, Field
from pydantic import EmailStr, SecretStr

class UserBase(SQLModel):
    username: str
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: SecretStr

class UserRead(UserBase):
    id: int | None = None
    disabled: bool

class UserUpdate(UserBase):
    full_name: str | None = None
    email: EmailStr | None = None