from fastapi import APIRouter, Depends, status, Body
from typing import Annotated
from fastapi_pagination import paginate, Page


from app.schemas.todos import TaskRequest, TaskResponse, TaskSortParams
from app.schemas.users import UserRead
from app.services.todo_service import TodoService
from app.api.deps import get_active_user

router = APIRouter(
    prefix="/task",
    tags=["Tasks"]
)

@router.post("", response_model=TaskResponse)
async def create_task(
    new_task: TaskRequest,
    current_user: Annotated[UserRead, Depends(get_active_user)]
):
    return await TodoService.create_task_service(new_task, current_user)

@router.get("", response_model=Page[TaskResponse])
async def get_all_tasks(
    current_user: Annotated[UserRead, Depends(get_active_user)],
    sort_params: Annotated[TaskSortParams, Depends()],
    filter_text: str | None = None
):
    return paginate(await TodoService.get_all_tasks_service(current_user, sort_params, filter_text))

@router.get("/{task_id}", response_model=TaskResponse)
async def get_specific_task(
    task_id: int,
    current_user: Annotated[UserRead, Depends(get_active_user)]
):
    return await TodoService.get_specific_task_service(task_id, current_user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specific_task(
    task_id: int,
    current_user: Annotated[UserRead, Depends(get_active_user)]
):
    return await TodoService.delete_specific_task_service(task_id, current_user)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_specific_task(
    task_id: int,
    modify_task: Annotated[TaskRequest, Body()],
    current_user: Annotated[UserRead, Depends(get_active_user)]
):
    return await TodoService.update_specific_task_service(
        task_id,
        modify_task,
        current_user
    )