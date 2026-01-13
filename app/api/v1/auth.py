from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import Token
from app.api.deps import get_token_for_user
from app.core.security import oauth2_scheme


router = APIRouter(
    prefix="",
    tags=["Auth"],
)

@router.post("/token")
async def login_for_access_token(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    print("Inside the endpoint to fetch token from /token")
    return await get_token_for_user(form_data)