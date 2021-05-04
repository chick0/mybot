"""empty message

Revision ID: 94c27530b043
Revises: ef6452225c33
Create Date: 2021-05-04 01:42:48.905685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c27530b043'
down_revision = 'ef6452225c33'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gift',
        sa.Column('idx', sa.Integer, unique=True, primary_key=True, nullable=False),
        sa.Column('owner', sa.String(50), nullable=False),
        sa.Column('type', sa.String(30), nullable=False),
        sa.Column('date', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('gift')
