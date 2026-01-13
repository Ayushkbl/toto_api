from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db.session import engine
from app.schemas.users import UserCreate, UserRead
from app.models.users import User
from app.core.security import hash_password

class UserService:

    @staticmethod
    async def create_user(new_user: UserCreate):
        print(f"New User password: {new_user.password.get_secret_value()}")
        print(f"Type of New User Passsword: {type(new_user.password.get_secret_value())}")
        
        model_user: User = await UserService.create_model_from_schema(new_user)

        with Session(engine) as session:
            session.add(model_user)
            session.commit()
            session.refresh(model_user)

        return await UserService.create_schema_from_model(model_user)
        
    @staticmethod
    async def create_model_from_schema(schema_user):
        return User(
            username=schema_user.username,
            full_name=schema_user.full_name,
            email=schema_user.email,
            hashed_password=hash_password(schema_user.password.get_secret_value()),
            disabled=False
        )
    
    @staticmethod
    async def create_schema_from_model(model_user: User):
        print("Inside create_schema_from_model")
        return UserRead(
            id=model_user.id,
            username=model_user.username,
            full_name=model_user.full_name,
            email=model_user.email,
            disabled=model_user.disabled
        )
    
    @staticmethod
    async def get_user_by_user_id(user_id: int):
        
        with Session(engine) as session:
            model_user: User = session.exec(select(User).where(User.id == user_id)).first()
        
        if not model_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"There are no user in the db with the user id: {user_id}"
            )
        
        return await UserService.create_schema_from_model(model_user)
    
    @staticmethod
    async def get_all_users():

        with Session(engine) as session:
            all_users: list[User] = session.exec(select(User)).all()
        
        if not all_users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Please create a new user through the User Create API"
            )

        all_schema_users: list[UserRead] = []

        for user in all_users:
            all_schema_users.append(await UserService.create_schema_from_model(user))
        
        return all_schema_users
