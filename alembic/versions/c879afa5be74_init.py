"""init

Revision ID: c879afa5be74
Revises: 
Create Date: 2023-05-04 22:39:26.736408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = 'c879afa5be74'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.create_table(
        'chats',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('prompt', sa.Text, default=None, nullable=True),
        sa.Column('scope', sa.Text, default='default', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('chat_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('text', sa.Text),
        sa.Column('scope', sa.String(200)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
        sa.ForeignKeyConstraint(('chat_id',), ['chats.id'], ),
        sa.ForeignKeyConstraint(('user_id',), ['users.id'], ),
    )


def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('chats')
    op.drop_table('users')
