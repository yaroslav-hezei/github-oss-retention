import requests
import os
from dotenv import load_dotenv
import time


load_dotenv()
secret = os.getenv('GITHUB_TOKEN')

headers = {"Authorization": f"Bearer {secret}"}

INPUT_PATH = 'data/processed/repos_to_process.txt'
OUTPUT_PATH = 'data/processed/contributors.csv'

done = set()
todo = []

# The output file doubles as the progress journal — a 3-hour run can die anytime,
# so completed work is recovered from what actually reached disk.
if os.path.exists(OUTPUT_PATH):
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')

            # A kill mid-write leaves "owner/repo," — accepting it would mark the
            # repo done and lose its value silently.
            if len(parts) == 2 and parts[0] != '' and (parts[1].isdigit() or parts[1] == 'NULL'):
                done.add(parts[0])

with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    for name in f:
        # Names in `done` are stripped; an unstripped '\n' here would break every check.
        name = name.strip()
        if name not in done:
            todo.append(name)

print(f"todo: {len(todo)}, done: {len(done)}")

for i, full_name in enumerate(todo, start=1):
    url = f"https://api.github.com/repos/{full_name}/contributors"

    # per_page=1 makes the last page number equal the contributor count, so the
    # full list is never downloaded. anon=true counts unlinked-email commits —
    # skipping them would undercount team size on older repos.
    params = {'per_page': 1, 'anon': 'true'}

    contributors = None

    for attempt in range(1, 6):
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            link = response.headers.get('Link')
            # No Link means one page of results, i.e. one contributor — not an error.
            if link is None:
                contributors = 1
            else:
                segments = link.split(',')
                for part in segments:
                    # By rel="last", not by position: the returned link set varies.
                    if 'rel="last"' in part:
                        # [-1] because 'page=' also occurs inside 'per_page='.
                        after = part.split('page=')[-1]
                        contributors = int(after.split('>')[0])
                        break
                # Link without rel="last" would leave None, which fails the integrity
                # check on resume and makes the repo retry forever.
                if contributors is None:
                    contributors = 'NULL'
            break
        elif response.status_code == 404:
            contributors = 'NULL'
            break
        elif response.status_code == 403:
            # 403 covers both an inaccessible repo and an exhausted rate limit.
            # Writing NULL for the latter would silently corrupt the rest of the run.
            if response.headers.get('X-RateLimit-Remaining') == '0':
                raise Exception("Rate limit exhausted — rerun later, resume will continue")
            contributors = 'NULL'
            break
        else:
            time.sleep(2 ** attempt)
    else:
        # All attempts failed — record as unknown rather than dropping the repo,
        # otherwise resume cannot tell "not processed" from "processed, unavailable".
        contributors = 'NULL'

    # Opened per iteration so each line is flushed to disk on close — buffering
    # across the loop would lose the tail of the run on a crash.
    with open(OUTPUT_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{full_name},{contributors}\n")

    if i % 100 == 0:
        print(f"{i}/{len(todo)}")

    # 5000 req/hour = 1.39s minimum; 1.5 leaves headroom for retries.
    time.sleep(1.5)