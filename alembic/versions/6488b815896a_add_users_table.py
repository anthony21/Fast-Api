"""add users table

Revision ID: 6488b815896a
Revises: 6984834d9c10
Create Date: 2022-10-27 11:30:16.237416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6488b815896a'
down_revision = '6984834d9c10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                     sa.Column('id', sa.Integer(), nullable=False),
                     sa.Column('email', sa.String(), nullable=False),
                     sa.Column('password', sa.String(), nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    pass
