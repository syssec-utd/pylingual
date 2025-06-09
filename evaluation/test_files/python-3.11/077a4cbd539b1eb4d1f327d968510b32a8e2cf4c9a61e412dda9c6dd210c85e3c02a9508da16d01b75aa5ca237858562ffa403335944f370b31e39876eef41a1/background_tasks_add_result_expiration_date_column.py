"""
Add the result and expiration date column to the background_tasks table.
"""
import os
import flask_sqlalchemy
MIGRATION_INDEX = 124
MIGRATION_NAME, _ = os.path.split(os.path.basename(__file__))

def run(db: flask_sqlalchemy.SQLAlchemy) -> bool:
    column_names = db.session.execute(db.text("\n        SELECT column_name\n        FROM information_schema.columns\n        WHERE table_name = 'background_tasks'\n        ")).fetchall()
    if ('result',) in column_names:
        return False
    db.session.execute(db.text('\n        ALTER TABLE background_tasks\n        ADD expiration_date TIMESTAMP NULL,\n        ADD result JSON NULL\n        '))
    return True