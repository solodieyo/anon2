"""settings_change

Revision ID: dc7958128b9a
Revises: db4eba9362cd
Create Date: 2024-07-15 15:20:17.026763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc7958128b9a'
down_revision: Union[str, None] = 'db4eba9362cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('settings', sa.Column('premium_price_day_stars', sa.Integer(), nullable=True, default=1))
    op.add_column('settings', sa.Column('premium_price_week_stars', sa.Integer(), nullable=True, default=1))
    op.add_column('settings', sa.Column('premium_price_month_stars', sa.Integer(), nullable=True, default=1))
    op.add_column('settings', sa.Column('premium_price_day_crypto', sa.Integer(), nullable=True, default=1))
    op.add_column('settings', sa.Column('premium_price_week_crypto', sa.Integer(), nullable=True, default=1))
    op.add_column('settings', sa.Column('premium_price_month_crypto', sa.Integer(), nullable=True, default=1))
    op.drop_column('settings', 'premium_price_day')
    op.drop_column('settings', 'premium_price_month')
    op.drop_column('settings', 'premium_price_week')
    op.add_column('users', sa.Column('premium_date', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'premium_date')
    op.add_column('settings', sa.Column('premium_price_week', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('settings', sa.Column('premium_price_month', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('settings', sa.Column('premium_price_day', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('settings', 'premium_price_month_crypto')
    op.drop_column('settings', 'premium_price_week_crypto')
    op.drop_column('settings', 'premium_price_day_crypto')
    op.drop_column('settings', 'premium_price_month_stars')
    op.drop_column('settings', 'premium_price_week_stars')
    op.drop_column('settings', 'premium_price_day_stars')
    # ### end Alembic commands ###
