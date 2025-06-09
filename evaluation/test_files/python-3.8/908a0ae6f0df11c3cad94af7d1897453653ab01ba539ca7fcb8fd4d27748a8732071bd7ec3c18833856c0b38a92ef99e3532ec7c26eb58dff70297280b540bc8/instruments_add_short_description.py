"""
Add short_description and short_description_is_markdown columns to instruments table.
"""
import os
import flask_sqlalchemy
MIGRATION_INDEX = 40
(MIGRATION_NAME, _) = os.path.splitext(os.path.basename(__file__))

def run(db: flask_sqlalchemy.SQLAlchemy) -> bool:
    column_names = db.session.execute(db.text("\n        SELECT column_name\n        FROM information_schema.columns\n        WHERE table_name = 'instruments'\n    ")).fetchall()
    if ('short_description',) in column_names:
        return False
    if ('name',) not in column_names:
        return False
    db.session.execute(db.text("\n        ALTER TABLE instruments\n        ADD short_description TEXT NOT NULL DEFAULT ''\n    "))
    db.session.execute(db.text('\n        ALTER TABLE instruments\n        ADD short_description_is_markdown BOOLEAN NOT NULL DEFAULT FALSE\n    '))
    db.session.execute(db.text('\n        UPDATE instruments\n        SET short_description = description, short_description_is_markdown=description_is_markdown\n    '))
    return True