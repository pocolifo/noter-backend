"""appropriate datetime type

Revision ID: 78bccc60f21d
Revises: a60b13db9c3e
Create Date: 2023-08-12 13:39:13.464986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78bccc60f21d'
down_revision = 'a60b13db9c3e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Folders
    op.alter_column('folders', 'last_edited', existing_type=sa.String(), type_=sa.DateTime(),
                    postgresql_using="to_timestamp(last_edited, 'YYYY-MM-DDTHH24:MI:SS')")
    op.alter_column('folders', 'created_on', existing_type=sa.String(), type_=sa.DateTime(),
                    postgresql_using="to_timestamp(created_on, 'YYYY-MM-DDTHH24:MI:SS')")

    # Notes
    op.alter_column('notes', 'last_edited', existing_type=sa.String(), type_=sa.DateTime(),
                    postgresql_using="to_timestamp(last_edited, 'YYYY-MM-DDTHH24:MI:SS')")
    op.alter_column('notes', 'created_on', existing_type=sa.String(), type_=sa.DateTime(),
                    postgresql_using="to_timestamp(created_on, 'YYYY-MM-DDTHH24:MI:SS')")

    # Users
    op.alter_column('users', 'last_signed_in', existing_type=sa.String(), type_=sa.DateTime(),
                    postgresql_using="to_timestamp(last_signed_in, 'YYYY-MM-DDTHH24:MI:SS')")
    op.alter_column('users', 'joined_on', existing_type=sa.String(), type_=sa.DateTime(),
                    postgresql_using="to_timestamp(joined_on, 'YYYY-MM-DDTHH24:MI:SS')")
    
    
def downgrade() -> None:
    # Folders
    op.alter_column('folders', 'last_edited', existing_type=sa.DateTime(), type_=sa.String())
    op.alter_column('folders', 'created_on', existing_type=sa.DateTime(), type_=sa.String())

    # Notes
    op.alter_column('notes', 'last_edited', existing_type=sa.DateTime(), type_=sa.String())
    op.alter_column('notes', 'created_on', existing_type=sa.DateTime(), type_=sa.String())

    # Users
    op.alter_column('users', 'last_signed_in', existing_type=sa.DateTime(), type_=sa.String())
    op.alter_column('folders', 'joined_on', existing_type=sa.DateTime(), type_=sa.String())
