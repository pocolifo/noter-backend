"""note data

Revision ID: e612ff015a41
Revises: 472fbd54de0c
Create Date: 2023-07-08 12:47:46.948830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e612ff015a41'
down_revision = '472fbd54de0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.create_table(
        'notedata',
        sa.Column('primary_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.String, unique=True),
        sa.Column('data', sa.String)
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('notes')
    op.drop_table('folders')
