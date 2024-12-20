"""new_tables

Revision ID: b97d70ed9d74
Revises: 6e59a244a53b
Create Date: 2024-08-12 02:19:12.509515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.src.infrastructure.database.models import Settings

# revision identifiers, used by Alembic.
revision: str = 'b97d70ed9d74'
down_revision: Union[str, None] = '6e59a244a53b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_updates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('before', sa.String(), nullable=True),
    sa.Column('after', sa.String(), nullable=True),
    sa.Column('update_type', sa.Enum('username', 'full_name', name='userupdate'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('settings', sa.Column('premium_price_forever_crypto', sa.Integer(), nullable=False))
    op.add_column('settings', sa.Column('premium_price_forever_stars', sa.Integer(), nullable=False))
    op.alter_column('settings', 'premium_price_day_stars',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('settings', 'premium_price_week_stars',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('settings', 'premium_price_month_stars',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('settings', 'premium_price_day_crypto',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('settings', 'premium_price_week_crypto',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('settings', 'premium_price_month_crypto',
               existing_type=sa.INTEGER(),
               nullable=False)

    op.execute(
        sa.insert(Settings).values(
            id=1,
            premium_price_day_stars=1,
            premium_price_week_stars=1,
            premium_price_month_stars=1,
            premium_price_day_crypto=1,
            premium_price_week_crypto=1,
            premium_price_month_crypto=1,
            premium_price_forever_crypto=1,
            premium_price_forever_stars=1,
            locale_ru=True,
            locale_en=True,
            locale_de=True,
            locale_uk=True
        )
    )
    op.add_column('users', sa.Column('referral_user_id', sa.BigInteger(), nullable=True))
    op.add_column('users', sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('show_premium_username', sa.Boolean(), default=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'show_premium_username')
    op.drop_column('users', 'last_activity')
    op.drop_column('users', 'referral_user_id')
    op.alter_column('settings', 'premium_price_month_crypto',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('settings', 'premium_price_week_crypto',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('settings', 'premium_price_day_crypto',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('settings', 'premium_price_month_stars',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('settings', 'premium_price_week_stars',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('settings', 'premium_price_day_stars',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('settings', 'premium_price_forever_stars')
    op.drop_column('settings', 'premium_price_forever_crypto')
    op.drop_table('user_updates')
    # ### end Alembic commands ###
