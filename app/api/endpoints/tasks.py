from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    # HTTPAuthorizationCredentials,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.user_utils import get_current_user
from app.api.schemas.tasks import TaskCreate, TaskDelete, TaskResponse, TaskUpdate
from app.db.database import get_db_session
from app.db.models import Task


# http_bearer = HTTPBearer(auto_error=False)



router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    # dependencies=[Depends(http_bearer)],
)



@router.post(
        "/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse
    )
async def create_task(
    task_in: TaskCreate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    return task


@router.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=list[TaskResponse],
    )
async def get_tasks(
    session: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    query = select(Task)
    result = await session.execute(query)
    tasks = result.scalars().all()

    return tasks


@router.get(
        "/{task_id}", response_model=TaskResponse
    )
async def get_task_id(
    task_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task_by_id = result.scalar_one_or_none()
    if task_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task_by_id


@router.put(
        "/{task_id}", response_model=TaskResponse
    )
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.model_dump().items():
        if key == "status" and value is None:
            continue
        setattr(db_task, key, value)
    await session.commit()

    return db_task


@router.delete(
        "/{task_id}", response_model=TaskDelete
    )
async def delete_task(
    task_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()

    return task
