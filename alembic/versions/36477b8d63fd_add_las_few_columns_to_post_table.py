"""add las few columns to post table

Revision ID: 36477b8d63fd
Revises: ddbbe14f5dfb
Create Date: 2022-10-29 13:08:24.197249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36477b8d63fd'
down_revision = 'ddbbe14f5dfb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
