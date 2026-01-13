from sqlmodel import SQLModel

class TaskRequest(SQLModel):
    title: str
    description: str

class TaskResponse(SQLModel):
    id: int | None
    title: str
    description: str
    user_id: int | None