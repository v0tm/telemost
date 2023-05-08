"""Add Chat title, index on scope for messages

Revision ID: f0ff8c13c008
Revises: c879afa5be74
Create Date: 2023-05-05 16:47:16.974517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0ff8c13c008'
down_revision = 'c879afa5be74'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('chats', sa.Column('name', sa.String(150), default=None, nullable=True))
    op.create_index('scope_index', 'chats', ['scope'])


def downgrade() -> None:
    op.drop_index('scope_index')
    op.drop_column('chats', 'name')
