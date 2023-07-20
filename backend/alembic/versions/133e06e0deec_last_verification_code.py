"""last verification code

Revision ID: 133e06e0deec
Revises: a65140396406
Create Date: 2023-07-19 19:52:24.115329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133e06e0deec'
down_revision = 'a65140396406'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('verification_code', sa.String, default=False))


def downgrade() -> None:
    op.drop_column('users', 'verification_code')
