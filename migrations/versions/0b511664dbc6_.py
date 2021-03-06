"""empty message

Revision ID: 0b511664dbc6
Revises: 8c0cd65f5dd7
Create Date: 2020-09-21 12:40:09.138114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b511664dbc6'
down_revision = '8c0cd65f5dd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('utc_offset', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('history', 'utc_offset')
    # ### end Alembic commands ###
