"""empty message

Revision ID: 09e03feae8be
Revises: 
Create Date: 2021-04-20 06:04:44.582641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09e03feae8be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'wallet',
        sa.Column('idx', sa.Integer, unique=True, primary_key=True, nullable=False),
        sa.Column('owner', sa.Integer, nullable=False),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('count', sa.Integer, nullable=False, default=0),
    )
    op.create_table(
        'coin',
        sa.Column('name', sa.String(30), unique=True, primary_key=True, nullable=False),
        sa.Column('price', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('wallet')
    op.drop_table('coin')
