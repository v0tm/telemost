"""add topic field

Revision ID: 9f4a3b722af7
Revises: f0ff8c13c008
Create Date: 2025-05-26 15:31:48.583109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f4a3b722af7'
down_revision = 'f0ff8c13c008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('topic', sa.Integer(), default=None, nullable=True))
    op.create_index('topic_index', 'messages', ['topic'])


def downgrade() -> None:
    op.drop_index('topic_index')
    op.drop_column('messages', 'topic')
