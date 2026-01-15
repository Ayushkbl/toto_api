from fastapi import HTTPException,status
from sqlmodel import Session, select, or_
from app.db.session import engine

from app.schemas.todos import TaskRequest, TaskResponse, TaskSortParams
from app.models.todos import Todo
from app.schemas.users import UserRead

class TodoService:

    @staticmethod
    async def create_task_service(new_task: TaskRequest, current_user: UserRead) -> TaskResponse:

        with Session(engine) as session:
            model_task = await TodoService.create_model_from_schema(session, new_task, current_user)
            session.add(model_task)
            session.commit()
            session.refresh(model_task)
        
        return await TodoService.create_schema_from_model(model_task)
    
    @staticmethod
    async def create_model_from_schema(session: Session, schema_task: TaskRequest, current_user: UserRead):

        model_task = Todo(
            title=schema_task.title,
            description=schema_task.description,
            user_id=current_user.id
        )

        return model_task
    
    @staticmethod
    async def create_schema_from_model(model_task: Todo):

        return TaskResponse(
            id=model_task.id,
            title=model_task.title,
            description=model_task.description,
            user_id=model_task.user_id
        )
    
    @staticmethod
    async def check_user_access(task: TaskResponse, current_user: UserRead):

        if task.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
        return True
    
    @staticmethod
    async def get_all_tasks_service(current_user: UserRead, sort_params: TaskSortParams, filter_text: str | None = None):

        with Session(engine) as session:
            tasks_by_user: list[Todo] = await TodoService.get_tasks_by_user(session, current_user, sort_params, filter_text)

        tasks_schema_by_user = []

        for task in tasks_by_user:
            tasks_schema_by_user.append(await TodoService.create_schema_from_model(task))
        
        return tasks_schema_by_user
    
    @staticmethod
    async def get_tasks_by_user(session: Session, current_user: UserRead, sort_params: TaskSortParams, filter_text: str | None = None):

        statement = select(Todo).where(Todo.user_id == current_user.id)

        if filter_text:
            statement = statement.where(or_(
                Todo.title.ilike(f"%{filter_text}%"),
                Todo.description.ilike(f"%{filter_text}%")
            ))
        
        if sort_params.sort_by:
            column = getattr(Todo, sort_params.sort_by)
            if sort_params.order_by == "asc":
                statement = statement.order_by(column.asc())
            else:
                statement = statement.order_by(column.desc())
        
        tasks_by_user: list[Todo] = session.exec(statement).all()

        if not tasks_by_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message" : f"There is no task for the username : {current_user.username}"}
            )

        return tasks_by_user
        
    @staticmethod
    async def get_task_by_task_id(session: Session, task_id: int, user_id: int):

        statement = select(Todo).where(Todo.id == task_id)
        model_task: Todo = session.exec(statement).first()

        if not model_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message" : f"There is no task with task id : {task_id}"}
            )

        if model_task.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return model_task

    @staticmethod
    async def get_specific_task_service(task_id: int, current_user: UserRead):

        with Session(engine) as session:
            model_task = await TodoService.get_task_by_task_id(session, task_id, current_user.id)
        
        return await TodoService.create_schema_from_model(model_task)     

    @staticmethod
    async def delete_specific_task_service(task_id: int, current_user: UserRead):

        with Session(engine) as session:
            model_task = await TodoService.get_task_by_task_id(session, task_id, current_user.id)
            session.delete(model_task)
            session.commit()
        
        return
    
    @staticmethod
    async def update_specific_task_service(task_id: int, modify_task: TaskRequest, current_user: UserRead):

        with Session(engine) as session:
            model_task: Todo = await TodoService.get_task_by_task_id(session, task_id, current_user.id)
            model_task.title = modify_task.title
            model_task.description = modify_task.description
            session.add(model_task)
            session.commit()
            session.refresh(model_task)
        
        return await TodoService.create_schema_from_model(model_task)
