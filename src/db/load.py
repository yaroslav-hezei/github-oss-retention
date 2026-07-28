import json
import sqlite3
from collections import Counter

YEARS = range(2016, 2026)

RAW = 'data/raw/'
CONTRIBUTORS = 'data/processed/contributors.csv'
DB_PATH = 'data/github_oss.db'
TOP_N = 750

repos = []
for year in YEARS:
    with open(f'{RAW}{year}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Pages were fetched sequentially, so seams between them may not be monotonic.
        data.sort(key=lambda r: r['stargazers_count'], reverse=True)

        # Analytical trim, unlike prepare_repos.py's — that one only saved API calls.
        top = data[:TOP_N]

    repos.extend(top)

unique_ids = {repo['id'] for repo in repos}
if len(unique_ids) != len(repos):
    raise ValueError(f"Duplicate repo ids: {len(repos)} rows, {len(unique_ids)} unique")

contributors = {}
with open(CONTRIBUTORS, 'r', encoding='utf-8') as f:
    for line in f:
        name, value = line.strip().split(',')
        # SQLite accepts text in an INTEGER column silently, so 'NULL' must become
        # None here or "could not be counted" becomes indistinguishable from a real 0.
        if value.isdigit():
            value = int(value)
        elif value == 'NULL':
            value = None
        else:
            raise ValueError(f"Malformed line in {CONTRIBUTORS}: {line!r}")
        contributors[name] = value

# GitHub renamed several languages in linguist ('Matlab' -> 'MATLAB'); a repo keeps
# the spelling from when it was last analysed, so both live in the data. SQLite
# compares text case-sensitively and accepted them as distinct keys — the engine
# reading this database does not, and the duplicate blocks the language dimension
# entirely. Nine repos out of 7500 are affected.
spelling_counts = Counter(
    repo['language'] for repo in repos if repo['language'] is not None
)

# Sorted by count desc, then name asc: frequency picks the winner, the name is a
# tie-break so a rebuild cannot produce a different legend label from the same input.
canonical = {}
for spelling, _ in sorted(spelling_counts.items(), key=lambda kv: (-kv[1], kv[0])):
    canonical.setdefault(spelling.lower(), spelling)

languages = set()
owners = {}

for repo in repos:
    # A NULL FK is what excludes documentation repos from language cuts.
    if repo['language'] is not None:
        # Rewritten on the fact, not only in the dimension: normalising the dimension
        # alone would leave those repos pointing at a key that no longer exists,
        # trading a loud failure for a silent (Blank) bucket.
        repo['language'] = canonical[repo['language'].lower()]
        languages.add(repo['language'])
    owners[repo['owner']['login']] = repo['owner']['type']

null_contributors = sum(1 for repo in repos if contributors[repo['full_name']] is None)
print(f"repos: {len(repos)}, languages: {len(languages)}, "
      f"owners: {len(owners)}, contributors NULL: {null_contributors}")

conn = sqlite3.connect(DB_PATH)

# The DB mirrors the current raw files, not an accumulation of runs. INSERT OR
# IGNORE/REPLACE would keep rows that have since vanished from the source.
conn.execute('DELETE FROM repositories')
conn.execute('DELETE FROM owners')
conn.execute('DELETE FROM languages')

conn.executemany('INSERT INTO languages (language) VALUES (?)',
                 [(language,) for language in languages])


conn.executemany('INSERT INTO owners (owner_login, owner_type) VALUES (?, ?)',
                 owners.items())

rows = []
for repo in repos:
    rows.append((
        repo['id'],
        repo['full_name'],
        repo['owner']['login'],
        repo['language'],
        repo['stargazers_count'],
        repo['forks_count'],
        repo['open_issues_count'],
        contributors[repo['full_name']],
        repo['created_at'],
        repo['pushed_at'],
    ))

# Derived columns depend on SNAPSHOT_DATE and on thresholds not yet drawn from the
# distributions — filled by a separate script.
conn.executemany(
    'INSERT INTO repositories (repo_id, full_name, owner_login, language, stars, '
    'forks, open_issues, contributors, created_at, pushed_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
    rows
)

conn.commit()
conn.close()