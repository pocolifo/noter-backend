"""Add has_noter_access which will be updated in the Stripe webhook

Revision ID: a65140396406
Revises: b3ddb5277c30
Create Date: 2023-07-16 22:29:30.246072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a65140396406'
down_revision = 'b3ddb5277c30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('has_noter_access', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column('users', 'has_noter_access')
