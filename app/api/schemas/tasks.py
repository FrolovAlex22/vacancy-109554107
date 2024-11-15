from typing import Optional
from pydantic import BaseModel

from app.db.models import StatusTaskEnum


class TaskCreate(BaseModel):
    title: str
    description: str
    status: Optional[StatusTaskEnum] = StatusTaskEnum.WAITING


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: Optional[StatusTaskEnum] = None


class TaskDelete(BaseModel):
    title: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
