"""v0.1.4a.

This introduces an auxiliary user table needed to query the auth schema user table.

Revision ID: c13c9dd0f3ae
Revises: f7ba9352c706
Create Date: 2023-01-23 16:27:41.130937

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
revision = 'c13c9dd0f3ae'
down_revision = 'f7ba9352c706'
branch_labels = None
depends_on = None
sql = '\n\ncreate table public.auxuser (\n  id uuid not null references auth.users on delete cascade,\n  email text,\n  created_at timestamp,\n  primary key (id)\n);\n\nalter table public.auxuser enable row level security;\n\ncreate function public.handle_new_user()\nreturns trigger\nlanguage plpgsql\nsecurity definer set search_path = public\nas $$\nbegin\n  insert into public.auxuser (id)\n  values (new.id, new.email, new.created_at);\n  return new;\nend;\n$$;\n\ncreate trigger on_auth_user_created\n  after insert on auth.users\n  for each row execute procedure public.handle_new_user();\n\n'

def upgrade() -> None:
    op.execute(sql)
    op.drop_constraint('auxuser_id_fkey', 'auxuser', type_='foreignkey')
    op.create_foreign_key('auxuser_id_fkey', 'auxuser', 'users', ['id'], ['id'], referent_schema='auth')

def downgrade() -> None:
    pass