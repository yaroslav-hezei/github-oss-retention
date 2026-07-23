import sqlite3

DB_PATH = 'data/github_oss.db'
SCHEMA_PATH = 'sql/schema.sql'

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    schema = f.read()

# executescript, not execute: the file holds several statements and execute
# accepts only one.
conn.executescript(schema)

conn.commit()
conn.close()