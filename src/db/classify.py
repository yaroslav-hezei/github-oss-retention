import sqlite3

DB_PATH = 'data/github_oss.db'
SQL_PATH = 'sql/retention.sql'

conn = sqlite3.connect(DB_PATH)

with open(SQL_PATH, 'r', encoding='utf-8') as f:
    sql = f.read()

cur = conn.execute(sql)
print(f"rows updated: {cur.rowcount}")

conn.commit()
conn.close()