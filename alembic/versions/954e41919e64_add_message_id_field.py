"""add message_id field

Revision ID: 954e41919e64
Revises: 9f4a3b722af7
Create Date: 2025-05-26 16:52:52.559484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954e41919e64'
down_revision = '9f4a3b722af7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('message_id', sa.BigInteger(), default=None, nullable=True))
    op.create_index('message_id_index', 'messages', ['message_id'])


def downgrade() -> None:
    op.drop_index('message_id_index')
    op.drop_column('messages', 'message_id')
