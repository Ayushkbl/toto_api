from sqlmodel import SQLModel
from pydantic import BaseModel, model_validator
from typing import Literal, Optional
from fastapi import HTTPException, status

class TaskRequest(SQLModel):
    title: str
    description: str

class TaskResponse(SQLModel):
    id: int | None
    title: str
    description: str
    user_id: int | None

class TaskSortParams(BaseModel):
    sort_by: Optional[Literal["title", "id"]] = None
    order_by: Optional[Literal["asc", "desc"]] = None

    @model_validator(mode="after")
    def check_sort_consistency(self) -> "TaskSortParams":
        # If sort_by is chosen order_by must not be None
        if self.sort_by is not None and self.order_by is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The 'order_by' parameter is required when 'sort_by' is provided"
            )
        return self