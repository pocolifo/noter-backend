"""stripe plan id

Revision ID: b3ddb5277c30
Revises: 0e07d718fffb
Create Date: 2023-07-15 19:14:04.642856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3ddb5277c30'
down_revision = '0e07d718fffb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('plan_id', sa.String))


def downgrade() -> None:
    op.drop_column('users', 'plan_id')
