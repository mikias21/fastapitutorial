"""add the last few columns for the posts table

Revision ID: efaf95303dea
Revises: 8f95231e3b33
Create Date: 2022-08-18 00:39:54.818921

"""
from cgitb import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efaf95303dea'
down_revision = '8f95231e3b33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, sever_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
