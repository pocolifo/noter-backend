"""Is email verified (users)

Revision ID: 0e07d718fffb
Revises: 472fbd54de0c
Create Date: 2023-07-11 10:29:57.266920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e07d718fffb'
down_revision = '472fbd54de0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('email_verified', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column('users', 'email_verified')
