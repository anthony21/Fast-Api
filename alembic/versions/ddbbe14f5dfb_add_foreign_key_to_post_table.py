"""add foreign-key to post table

Revision ID: ddbbe14f5dfb
Revises: 6488b815896a
Create Date: 2022-10-29 13:04:06.491510

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddbbe14f5dfb'
down_revision = '6488b815896a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))

    op.create_foreign_key('post_users_fk',
                           source_table='posts',
                           referent_table='users',
                           local_cols=['owner_id'], 
                           remote_cols=['id'], 
                           ondelete=CASCADE)
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
