import sqlite3

# Fixed to the run date of repos.py, when pushed_at was captured. With now() the
# derived values shift on every run, and retention_class — which rests on a
# days_since_push threshold — would drift with the run date instead of the data.
SNAPSHOT_DATE = '2026-07-17'
DB_PATH = 'data/github_oss.db'
SQL_PATH = 'sql/derive.sql'

conn = sqlite3.connect(DB_PATH)

with open(SQL_PATH, 'r', encoding='utf-8') as f:
    sql = f.read()

cur = conn.execute(sql, (SNAPSHOT_DATE, SNAPSHOT_DATE))
print(f"rows updated: {cur.rowcount}")

conn.commit()
conn.close()