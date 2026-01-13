from sqlmodel import Field, SQLModel
from app.models.users import User


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    user_id: int | None = Field(default=None, foreign_key="users.id")