"""Add unmanaged_path column to vfolders

Revision ID: 5e88398bc340
Revises: d452bacd085c
Create Date: 2019-11-28 13:41:03.545551

"""
import sqlalchemy as sa
from alembic import op
revision = '5e88398bc340'
down_revision = 'd452bacd085c'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('vfolders', sa.Column('unmanaged_path', sa.String(length=512), nullable=True))

def downgrade():
    op.drop_column('vfolders', 'unmanaged_path')