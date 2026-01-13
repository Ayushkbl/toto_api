from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.users import User
from app.core.security import verify_password

class AuthService:

    @staticmethod
    async def authenticate_user(session: Session, username: str, password: str | None = None):

        print(f"username: {username}")
        print("Inside authenticate_user function")
        statement = select(User).where(User.username == username)
        model_user: User | None = session.exec(statement).first()

        if not model_user or (password != None and not verify_password(password, model_user.hashed_password)):
            print("Raising exception")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return model_user
    
    
    