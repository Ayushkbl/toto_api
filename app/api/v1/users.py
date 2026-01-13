from fastapi import APIRouter, Form, Depends
from typing import Annotated

from app.schemas.users import UserCreate, UserRead
from app.services.user_service import UserService
from app.api.deps import get_active_user
from app.core.security import oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post('', response_model=UserRead)
async def create_user(new_user: Annotated[UserCreate, Form()]):
    return await UserService.create_user(new_user)

@router.get('', response_model=list[UserRead])
async def get_all_users():
    return await UserService.get_all_users()

@router.get('/me', response_model=UserRead)
async def get_user_details(
    current_user: Annotated[UserRead, Depends(get_active_user)]
):
    print("Inside api endpoint get_logged_in_user")
    return current_user

@router.get('/{user_id}', response_model=UserRead)
async def get_specific_user(user_id: int):
    return await UserService.get_user_by_user_id(user_id)

