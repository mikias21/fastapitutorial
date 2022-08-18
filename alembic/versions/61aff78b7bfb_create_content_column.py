"""Create content column

Revision ID: 61aff78b7bfb
Revises: 16928d12408a
Create Date: 2022-08-18 00:21:52.615330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61aff78b7bfb'
down_revision = '16928d12408a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
