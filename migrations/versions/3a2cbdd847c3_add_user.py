"""add user

Revision ID: 3a2cbdd847c3
Revises: 
Create Date: 2024-02-26 22:33:19.898822

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3a2cbdd847c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the User table
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=50), nullable=False),
                    sa.Column('email', sa.String(length=120), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    # Drop the User table
    op.drop_table('user')
