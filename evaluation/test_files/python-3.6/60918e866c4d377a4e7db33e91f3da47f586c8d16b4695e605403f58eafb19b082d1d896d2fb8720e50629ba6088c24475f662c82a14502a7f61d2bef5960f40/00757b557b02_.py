"""
Add checks column to instance, execution and case tables. Add solution_checks to case table

Revision ID: 00757b557b02
Revises: f3bee20314a2
Create Date: 2022-02-08 18:38:15.959348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '00757b557b02'
down_revision = 'f3bee20314a2'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('cases', sa.Column('checks', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('cases', sa.Column('solution_checks', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('executions', sa.Column('checks', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('instances', sa.Column('checks', postgresql.JSON(astext_type=sa.Text()), nullable=True))

def downgrade():
    op.drop_column('instances', 'checks')
    op.drop_column('executions', 'checks')
    op.drop_column('cases', 'solution_checks')
    op.drop_column('cases', 'checks')