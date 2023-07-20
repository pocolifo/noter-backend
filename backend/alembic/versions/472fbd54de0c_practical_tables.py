"""Practical tables

Revision ID: 472fbd54de0c
Revises: 261a72acbe75
Create Date: 2023-06-30 18:05:40.653869

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = '472fbd54de0c'
down_revision = '261a72acbe75'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('users')
    op.drop_table('notes')
    op.drop_table('folders')

    op.create_table(
        'users',
        sa.Column('primary_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.String, unique=True),
        sa.Column('email', sa.String),
        sa.Column('password', sa.String),
        sa.Column('stripe_id', sa.String),
        sa.Column('last_signed_in', sa.String),
        sa.Column('joined_on', sa.String),
        sa.Column('history', JSON)
    )

    op.create_table(
        'notes',
        sa.Column('primary_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.String, unique=True),
        sa.Column('type', sa.String),
        sa.Column('name', sa.String),
        sa.Column('path', sa.ARRAY(sa.String)),
        sa.Column('last_edited', sa.String),
        sa.Column('created_on', sa.String),
        sa.Column('owner_id', sa.String, sa.ForeignKey('users.id')),
        sa.Column('blocks', JSON)
    )
    
    op.create_table(
        'folders',
        sa.Column('primary_id', sa.Integer, primary_key=True),
        sa.Column('id', sa.String, unique=True),
        sa.Column('type', sa.String),
        sa.Column('name', sa.String),
        sa.Column('path', sa.ARRAY(sa.String)),
        sa.Column('last_edited', sa.String),
        sa.Column('created_on', sa.String),
        sa.Column('owner_id', sa.String, sa.ForeignKey('users.id')),
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('notes')
    op.drop_table('folders')
