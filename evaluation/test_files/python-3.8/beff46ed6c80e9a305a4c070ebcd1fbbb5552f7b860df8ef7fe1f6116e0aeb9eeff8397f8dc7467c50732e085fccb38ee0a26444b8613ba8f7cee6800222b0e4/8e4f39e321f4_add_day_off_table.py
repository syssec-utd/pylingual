"""add day off table

Revision ID: 8e4f39e321f4
Revises: fb87feaaa094
Create Date: 2021-02-13 01:03:30.408954

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid
revision = '8e4f39e321f4'
down_revision = 'fb87feaaa094'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('day_off', sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False), sa.Column('created_at', sa.DateTime(), nullable=True), sa.Column('updated_at', sa.DateTime(), nullable=True), sa.Column('date', sa.Date(), nullable=False), sa.Column('person_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=True), sa.ForeignKeyConstraint(['person_id'], ['person.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('person_id', 'date', name='day_off_uc'))
    op.create_index(op.f('ix_day_off_person_id'), 'day_off', ['person_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_day_off_person_id'), table_name='day_off')
    op.drop_table('day_off')