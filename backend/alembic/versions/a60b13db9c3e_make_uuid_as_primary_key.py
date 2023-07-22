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
    for table in ['notes', 'folders']:
        op.drop_constraint(f'{table}_owner_id_fkey', table, type_='foreignkey')
        op.execute(
            sa.text(f'ALTER TABLE {table} ALTER COLUMN owner_id TYPE UUID USING id::uuid;')
        )

    # For all tables, drop primary_id and convert id to primary key & UUID
    for table in ['users', 'notes', 'folders']:
        op.drop_column(table, 'primary_id')

        # change from string to UUID
        # USING {} is SAFE HERE because table can only be one of ['users', 'notes', 'folders']

        op.execute(
            sa.text(f'ALTER TABLE {table} ALTER COLUMN id TYPE UUID USING id::uuid;')
        )

        # set the server default to generate a uuid4 automatically
        op.execute(
            sa.text(f'ALTER TABLE {table} ALTER COLUMN id SET DEFAULT gen_random_uuid();')
        )

        op.create_primary_key(
            f'pk_{table}',
            table,
            ['id']
        )

    # re-add foreign key
    for table in ['notes', 'folders']:
        op.create_foreign_key(op.f(f'{table}_owner_id_fkey'), table, 'users', ['owner_id'], ['id'])

def downgrade() -> None:
    # update foreign key types
    for table in ['notes', 'folders']:
        op.drop_constraint(f'{table}_owner_id_fkey', table, type_='foreignkey')
        op.alter_column(
            table,
            'owner_id',
            existing_type=sa.UUID(as_uuid=False),
            type_=sa.String,
            server_default=None
        )
    
    # For all tables, drop primary_id and convert id to primary key & UUID
    for table in ['users', 'notes', 'folders']:
        op.drop_constraint(
            f'pk_{table}',
            table,
            type_='primary'
        )
        op.add_column(table, sa.Column('primary_id', sa.Integer, primary_key=True))
        op.alter_column(
            table,
            'id',
            existing_type=sa.UUID(as_uuid=False),
            type_=sa.String,
            server_default=None
        )
    
    # re-add foreign key
    for table in ['notes', 'folders']:
        op.create_foreign_key(op.f(f'{table}_owner_id_fkey'), table, 'users', ['owner_id'], ['id'])
