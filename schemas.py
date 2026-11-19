from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime
from typing import Literal

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: Literal['new', 'in_progress', 'done'] = 'new'
    priority: int = Field(default=0, ge=0)
    project_id: int = Field(gt=0)

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    status: str
    priority: int
    project_id: int

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: Literal['new', 'in_progress', 'done'] | None = None
    priority: int | None = Field(default=None, ge=0)
    project_id: int | None = Field(default=None, gt=0)

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    owner_id: int = Field(gt=0)
    is_archived: bool = False

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner_id: int
    is_archived: bool

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    owner_id: int | None = Field(default=None, gt=0)
    is_archived: bool | None = None

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    phone: str | None = Field(default=None, max_length=30)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None = None
    is_active: bool

class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool | None = None

class CommentCreate(BaseModel):
    comment: str = Field(min_length=1)

class CommentUpdate(BaseModel):
    comment: str | None = Field(default=None, min_length=1)

class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    comment: str
    created_at: datetime
    task_id: int

