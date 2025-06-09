from typing import Dict
from typing import List
import sqlite3

async def create_aliases_table(db_file_name: str) -> Dict[str, str]:
    """Creates a sqlite table with default aliases and returns all aliases.

    Assumes the table does not exist.
    """
    default_aliases = {'c': 'c-clang', 'c#': 'cs-csc', 'c++': 'cpp-clang', 'cpp': 'cpp-clang', 'cs': 'cs-csc', 'f#': 'fs-core', 'fs': 'fs-core', 'java': 'java-openjdk', 'javascript': 'javascript-node', 'js': 'javascript-node', 'objective-c': 'objective-c-clang', 'py': 'python3', 'python': 'python3', 'swift': 'swift4'}
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        cursor.execute('\n            CREATE TABLE aliases (\n                id INTEGER PRIMARY KEY,\n                alias TEXT NOT NULL,\n                language TEXT NOT NULL,\n                UNIQUE (alias)\n            );\n            ')
        cursor.executemany('\n            INSERT OR IGNORE INTO aliases\n            (alias, language)\n            VALUES (?, ?);\n            ', default_aliases.items())
        conn.commit()
    return default_aliases

async def load_aliases(db_file_name: str) -> Dict[str, str]:
    """Loads aliases from the database.

    Returns an empty dictionary if there are no aliases.
    """
    try:
        with sqlite3.connect(db_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT alias, language FROM aliases')
            records = cursor.fetchall()
            if not records:
                return dict()
            all_aliases = dict()
            for (alias, language) in records:
                all_aliases[alias] = language
            return all_aliases
    except sqlite3.OperationalError:
        return await create_aliases_table(db_file_name)

async def create_alias(db_file_name: str, new_alias: str, language: str, aliases: Dict[str, str], languages: List[str]) -> None:
    aliases[new_alias] = language
    languages.append(new_alias)
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        cursor.execute('\n            INSERT INTO languages\n            (language)\n            VALUES (?);\n            ', [new_alias])
        cursor.execute('\n            INSERT INTO aliases\n            (alias, language)\n            VALUES (?, ?);\n            ', (new_alias, language))

async def delete_alias(alias: str, aliases: Dict[str, str], languages: List[str], db_file_name: str):
    del aliases[alias]
    languages.remove(alias)
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        cursor.execute('\n            DELETE FROM aliases\n            WHERE alias = ?;\n            ', [alias])
        cursor.execute('\n            DELETE FROM languages\n            WHERE language = ?;\n            ', [alias])
        cursor.execute('\n            DELETE FROM jargon\n            WHERE language = ?;\n            ', [alias])