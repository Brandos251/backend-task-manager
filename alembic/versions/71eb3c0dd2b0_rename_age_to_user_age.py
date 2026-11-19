"""rename age to user_age

Revision ID: 71eb3c0dd2b0
Revises: 0d5d7a9dbefd
Create Date: 2026-11-08 17:40:32.707270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71eb3c0dd2b0'
down_revision: Union[str, Sequence[str], None] = '0d5d7a9dbefd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'age', new_column_name='new_age')


def downgrade() -> None:
    op.alter_column('users', 'new_age', new_column_name='age')
