"""content

Revision ID: d0118d8ec0b4
Revises: 2c36fcc0b921
Create Date: 2021-02-04 02:59:06.516503

"""
from alembic import op
import sqlalchemy as sa
revision = 'd0118d8ec0b4'
down_revision = '2c36fcc0b921'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('medias', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preview', sa.Integer(), nullable=True))

def downgrade():
    with op.batch_alter_table('medias', schema=None) as batch_op:
        batch_op.drop_column('preview')