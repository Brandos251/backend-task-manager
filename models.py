from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Identity, String, Text, Integer, Index, text

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    new_age: Mapped[int | None] = mapped_column(
        Integer
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner",
    )

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text('false'),
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    owner: Mapped["User"] = relationship(
        back_populates="projects",
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
    )

class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        Index('idx_tasks_project_id', 'project_id'),
    )

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default=text("'new'"),
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text('0'),        
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        back_populates="tasks",
    )

    comments: Mapped[list['Comment']] = relationship(
        back_populates='task'
    ) 

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True
    )

    comment: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    task: Mapped["Task"] = relationship(
        back_populates="comments"
    )