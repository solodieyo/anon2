"""create_tables

Revision ID: e0c52799d8f6
Revises: 
Create Date: 2024-07-05 01:39:18.779342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.src.infrastructure.database.models import Settings

# revision identifiers, used by Alembic.
revision: str = 'e0c52799d8f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content_type', sa.Enum('UNKNOWN', 'ANY', 'TEXT', 'ANIMATION', 'AUDIO', 'DOCUMENT', 'PHOTO', 'STICKER', 'STORY', 'VIDEO', 'VIDEO_NOTE', 'VOICE', 'CONTACT', 'DICE', 'GAME', 'POLL', 'VENUE', 'LOCATION', 'NEW_CHAT_MEMBERS', 'LEFT_CHAT_MEMBER', 'NEW_CHAT_TITLE', 'NEW_CHAT_PHOTO', 'DELETE_CHAT_PHOTO', 'GROUP_CHAT_CREATED', 'SUPERGROUP_CHAT_CREATED', 'CHANNEL_CHAT_CREATED', 'MESSAGE_AUTO_DELETE_TIMER_CHANGED', 'MIGRATE_TO_CHAT_ID', 'MIGRATE_FROM_CHAT_ID', 'PINNED_MESSAGE', 'INVOICE', 'SUCCESSFUL_PAYMENT', 'USERS_SHARED', 'CHAT_SHARED', 'CONNECTED_WEBSITE', 'WRITE_ACCESS_ALLOWED', 'PASSPORT_DATA', 'PROXIMITY_ALERT_TRIGGERED', 'BOOST_ADDED', 'CHAT_BACKGROUND_SET', 'FORUM_TOPIC_CREATED', 'FORUM_TOPIC_EDITED', 'FORUM_TOPIC_CLOSED', 'FORUM_TOPIC_REOPENED', 'GENERAL_FORUM_TOPIC_HIDDEN', 'GENERAL_FORUM_TOPIC_UNHIDDEN', 'GIVEAWAY_CREATED', 'GIVEAWAY', 'GIVEAWAY_WINNERS', 'GIVEAWAY_COMPLETED', 'VIDEO_CHAT_SCHEDULED', 'VIDEO_CHAT_STARTED', 'VIDEO_CHAT_ENDED', 'VIDEO_CHAT_PARTICIPANTS_INVITED', 'WEB_APP_DATA', 'USER_SHARED', name='contenttype'), nullable=False),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    table_settings = op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('premium_price_day', sa.Integer(), nullable=False),
    sa.Column('premium_price_week', sa.Integer(), nullable=False),
    sa.Column('premium_price_month', sa.Integer(), nullable=False),
    sa.Column('locale_ru', sa.Boolean(), nullable=False),
    sa.Column('locale_en', sa.Boolean(), nullable=False),
    sa.Column('locale_de', sa.Boolean(), nullable=False),
    sa.Column('locale_uk', sa.Boolean(), nullable=False),
    sa.Column('start_picture', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('custom_username', sa.String(), nullable=True),
    sa.Column('premium', sa.Boolean(), nullable=False),
    sa.Column('rank', sa.Enum('ADMIN', 'MEMBER', name='roles'), nullable=False),
    sa.Column('show_in_tops', sa.Boolean(), nullable=False),
    sa.Column('locale', sa.Enum('RU', 'EN', 'DE', 'UK', name='locale'), nullable=False),
    sa.Column('super_premium', sa.Boolean(), nullable=False),
    sa.Column('archive', sa.Boolean(), nullable=False),
    sa.Column('hello_message', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('from_user_id', sa.Integer(), nullable=False),
    sa.Column('to_user_id', sa.Integer(), nullable=False),
    sa.Column('media_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['media_id'], ['media.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blocked',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('blocked_user_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['blocked_user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_id', 'blocked_user_id', 'message_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blocked')
    op.drop_table('payments')
    op.drop_table('messages')
    op.drop_table('users')
    op.drop_table('settings')
    op.drop_table('media')
    # ### end Alembic commands ###
