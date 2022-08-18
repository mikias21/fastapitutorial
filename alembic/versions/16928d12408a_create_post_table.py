"""Create post table

Revision ID: 16928d12408a
Revises: 
Create Date: 2022-08-18 00:09:36.093967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16928d12408a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass 

def downgrade() -> None:
    op.drop_table('posts')
    pass 