"""create JSON tables

Revision ID: 261a72acbe75
Revises: 
Create Date: 2023-06-29 20:48:34.286117

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = '261a72acbe75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('info', JSON)
    )

    op.create_table(
        'notes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('info', JSON)
    )

    op.create_table(
        'folders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('info', JSON)
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('notes')
    op.drop_table('folders')
