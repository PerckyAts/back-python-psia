"""add new table pre_match_analisis

Revision ID: 2238c9f25e05
Revises: 45c8940623d5
Create Date: 2024-03-05 11:29:47.954039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2238c9f25e05'
down_revision: Union[str, None] = '45c8940623d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
