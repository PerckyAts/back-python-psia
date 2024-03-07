"""Migration de la table 'user'

Revision ID: 3550e2675853
Revises: 2238c9f25e05
Create Date: 2024-03-05 11:43:10.388286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3550e2675853'
down_revision: Union[str, None] = '2238c9f25e05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
