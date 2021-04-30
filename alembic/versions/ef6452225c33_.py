"""empty message

Revision ID: ef6452225c33
Revises: 09e03feae8be
Create Date: 2021-04-24 01:49:03.370793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef6452225c33'
down_revision = '09e03feae8be'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'point',
        sa.Column('owner', sa.Integer, unique=True, primary_key=True, nullable=False),
        sa.Column('point', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('point')
