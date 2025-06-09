"""Add ``dag_id``/``state`` index on ``dag_run`` table

Revision ID: 127d2bf2dfa7
Revises: 5e7d17757c7a
Create Date: 2017-01-25 11:43:51.635667

"""
from alembic import op
revision = '127d2bf2dfa7'
down_revision = '5e7d17757c7a'
branch_labels = None
depends_on = None
airflow_version = '1.7.1.3'

def upgrade():
    op.create_index('dag_id_state', 'dag_run', ['dag_id', 'state'], unique=False)

def downgrade():
    op.drop_index('dag_id_state', table_name='dag_run')