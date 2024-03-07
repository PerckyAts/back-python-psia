"""Add new table

Revision ID: 45c8940623d5
Revises: bb597da9789c
Create Date: 2024-02-21 12:14:46.001517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45c8940623d5'
down_revision: Union[str, None] = 'bb597da9789c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
