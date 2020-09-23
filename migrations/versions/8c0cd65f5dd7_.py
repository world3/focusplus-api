"""empty message

Revision ID: 8c0cd65f5dd7
Revises: 26fe28cf81ad
Create Date: 2020-09-18 15:35:52.209840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c0cd65f5dd7'
down_revision = '26fe28cf81ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stat_key', sa.String(length=8), nullable=False),
    sa.Column('pomos', sa.String(length=256), nullable=False),
    sa.Column('breaks', sa.String(length=256), nullable=False),
    sa.Column('totalPomos', sa.Integer(), nullable=False),
    sa.Column('totalBreaks', sa.Integer(), nullable=False),
    sa.Column('interruptions', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stat_stat_key'), 'stat', ['stat_key'], unique=False)
    op.drop_index('title', table_name='task')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('title', 'task', ['title'], unique=True)
    op.drop_index(op.f('ix_stat_stat_key'), table_name='stat')
    op.drop_table('stat')
    # ### end Alembic commands ###
