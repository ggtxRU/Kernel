"""Added calculation's tables

Revision ID: 5cc1b2f4034e
Revises: 
Create Date: 2022-11-29 19:36:20.011925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cc1b2f4034e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('calculation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('input_data', sa.JSON(), nullable=False),
    sa.Column('status', sa.Enum('complete', 'in_progress', 'in_the_queue', name='calculationstatusenum'), server_default='in_the_queue', nullable=False),
    sa.Column('calculation_start_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_calculation')),
    sa.UniqueConstraint('id', name=op.f('uq_calculation_id'))
    )
    op.create_table('calculation_result',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('calculation_result_date', sa.DateTime(), nullable=False),
    sa.Column('liquid', sa.Integer(), nullable=False),
    sa.Column('oil', sa.Integer(), nullable=False),
    sa.Column('water', sa.Integer(), nullable=False),
    sa.Column('wct', sa.Integer(), nullable=False),
    sa.Column('time_spent', sa.Float(), nullable=False),
    sa.Column('calculation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['calculation_id'], ['calculation.id'], name=op.f('fk_calculation_result_calculation_id_calculation'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_calculation_result')),
    sa.UniqueConstraint('id', name=op.f('uq_calculation_result_id'))
    )


def downgrade():
    op.drop_table('calculation_result')
    op.drop_table('calculation')
