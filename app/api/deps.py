from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.token import Token, TokenData
from app.schemas.users import UserRead
from app.core.security import decode_access_token, oauth2_scheme, hash_password, create_access_token
from app.db.session import engine

async def get_token_for_user(form_data: OAuth2PasswordRequestForm):

    print("Inside get_token_for_user function in deps")
    with Session(engine) as session:
        model_user = await AuthService.authenticate_user(session, form_data.username, form_data.password)
    
    response_user = await UserService.create_schema_from_model(model_user)
    token = create_access_token({"username": response_user.username})

    return Token(access_token=token, token_type="Bearer")

async def get_logged_in_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print("Inside get_logged_in_user dependecncy")
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    print("Returned from tokenUrl lines")
    try:
        payload = decode_access_token(token)
        username = payload.get("username")
        if username is None:
            raise credentials_exceptions
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exceptions
    
    with Session(engine) as session:
        model_user = await AuthService.authenticate_user(session, token_data.username)
    
    return await UserService.create_schema_from_model(model_user)


async def get_active_user(
    logged_in_user: Annotated[UserRead, Depends(get_logged_in_user)]
):
    print("Inside get_active_user dependency")
    if logged_in_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    
    return logged_in_user
