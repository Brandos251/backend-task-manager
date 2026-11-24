"""baseline existing database

Revision ID: 948c56c29ae7
Revises: 
Create Date: 2026-11-05 15:46:18.139787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '948c56c29ae7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database schema."""

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "phone",
            sa.String(length=30),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "projects",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "owner_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(always=True),
            nullable=False
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default=sa.text("'new'"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False
        ),
        sa.Column(
            "project_id",
            sa.Integer(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "idx_tasks_project_id",
        "tasks",
        ["project_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop initial database schema."""

    op.drop_index(
        "idx_tasks_project_id",
        table_name="tasks"
    )

    op.drop_table("tasks")
    op.drop_table("projects")
    op.drop_table("users")
