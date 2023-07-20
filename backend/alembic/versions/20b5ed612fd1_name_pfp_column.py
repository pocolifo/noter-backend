"""name column

Revision ID: 20b5ed612fd1
Revises: 133e06e0deec
Create Date: 2023-07-20 14:34:50.920382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20b5ed612fd1'
down_revision = '133e06e0deec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String))
    op.add_column('users', sa.Column('pfp', sa.String))

def downgrade() -> None:
    op.drop_column('users', 'name')
    op.drop_column('users', 'pfp')
