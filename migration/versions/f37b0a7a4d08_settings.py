"""settings

Revision ID: f37b0a7a4d08
Revises: dc7958128b9a
Create Date: 2024-07-19 17:45:34.159077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.src.infrastructure.database.models import Settings

# revision identifiers, used by Alembic.
revision: str = 'f37b0a7a4d08'
down_revision: Union[str, None] = 'dc7958128b9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass