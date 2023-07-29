"""Make UUID as primary key

Revision ID: a60b13db9c3e
Revises: 20b5ed612fd1
Create Date: 2023-07-21 21:33:54.971329

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a60b13db9c3e'
down_revision = '20b5ed612fd1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # update foreign key types
    # in notes table
    op.drop_constraint(f'notes_owner_id_fkey', 'notes', type_='foreignkey')
    op.execute(
        sa.text('ALTER TABLE notes ALTER COLUMN owner_id TYPE UUID USING id::uuid;')
    )

    # then folders
    op.drop_constraint(f'folders_owner_id_fkey', 'folders', type_='foreignkey')
    op.execute(
        sa.text('ALTER TABLE folders ALTER COLUMN owner_id TYPE UUID USING id::uuid;')
    )

    # For all tables, drop primary_id and convert id to primary key & UUID
    # users TABLE
    op.drop_column('users', 'primary_id')

    # change from string to UUID
    op.execute(
        sa.text('ALTER TABLE users ALTER COLUMN id TYPE UUID USING id::uuid;')
    )

    # set the server default to generate a uuid4 automatically
    op.execute(
        sa.text('ALTER TABLE users ALTER COLUMN id SET DEFAULT gen_random_uuid();')
    )

    # recreate primary key
    op.create_primary_key(
        'pk_users',
        'users',
        ['id']
    )

    # notes TABLE
    op.drop_column('notes', 'primary_id')

    op.execute(
        sa.text('ALTER TABLE notes ALTER COLUMN id TYPE UUID USING id::uuid;')
    )

    op.execute(
        sa.text('ALTER TABLE notes ALTER COLUMN id SET DEFAULT gen_random_uuid();')
    )

    op.create_primary_key(
        'pk_notes',
        'notes',
        ['id']
    )

    # folders TABLE
    op.drop_column('folders', 'primary_id')

    op.execute(
        sa.text('ALTER TABLE folders ALTER COLUMN id TYPE UUID USING id::uuid;')
    )

    op.execute(
        sa.text('ALTER TABLE folders ALTER COLUMN id SET DEFAULT gen_random_uuid();')
    )

    op.create_primary_key(
        'pk_folders',
        'folders',
        ['id']
    )

    # re-add foreign key
    op.create_foreign_key('folders_owner_id_fkey', 'folders', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('notes_owner_id_fkey', 'notes', 'users', ['owner_id'], ['id'])

def downgrade() -> None:
    # update foreign key types
    # notes TABLE
    op.drop_constraint('notes_owner_id_fkey', 'notes', type_='foreignkey')
    op.alter_column(
        'notes',
        'owner_id',
        existing_type=sa.UUID(as_uuid=False),
        type_=sa.String,
        server_default=None
    )

    op.drop_constraint('folders_owner_id_fkey', 'folders', type_='foreignkey')
    op.alter_column(
        'folders',
        'owner_id',
        existing_type=sa.UUID(as_uuid=False),
        type_=sa.String,
        server_default=None
    )
    
    # For all tables, drop primary_id and convert id to primary key & UUID
    # users TABLE
    op.drop_constraint(
        'pk_users',
        'users',
        type_='primary'
    )
    op.add_column('users', sa.Column('primary_id', sa.Integer, primary_key=True))
    op.alter_column(
        'users',
        'id',
        existing_type=sa.UUID(as_uuid=False),
        type_=sa.String,
        server_default=None
    )

    # notes TABLE
    op.drop_constraint(
        'pk_notes',
        'notes',
        type_='primary'
    )
    op.add_column('notes', sa.Column('primary_id', sa.Integer, primary_key=True))
    op.alter_column(
        'notes',
        'id',
        existing_type=sa.UUID(as_uuid=False),
        type_=sa.String,
        server_default=None
    )
    
    # folders TABLE
    op.drop_constraint(
        'pk_folders',
        'folders',
        type_='primary'
    )
    op.add_column('folders', sa.Column('primary_id', sa.Integer, primary_key=True))
    op.alter_column(
        'folders',
        'id',
        existing_type=sa.UUID(as_uuid=False),
        type_=sa.String,
        server_default=None
    )

    # re-add foreign key
    op.create_foreign_key('notes_owner_id_fkey', 'notes', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('folders_owner_id_fkey', 'folders', 'users', ['owner_id'], ['id'])
