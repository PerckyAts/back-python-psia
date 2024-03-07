"""Add new table

Revision ID: bb597da9789c
Revises: ea4eb887867a
Create Date: 2024-02-21 12:14:01.186634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb597da9789c'
down_revision: Union[str, None] = 'ea4eb887867a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
