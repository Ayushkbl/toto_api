from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.v1.users import router as user_router
from app.api.v1.auth import router as auth_router
from app.api.v1.todos import router as todo_router

app = FastAPI()
add_pagination(app)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(todo_router)