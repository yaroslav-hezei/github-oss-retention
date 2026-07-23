import json
import os

os.makedirs('data/processed', exist_ok=True)

years = range(2016,2026)
# outside the loop: all years go into one file
all_names = []

for year in years:

    with open(f'data/raw/{year}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # raw is sorted by stars desc, so first 750 = top-750, dropping the padding to page 8
    top_750 = data[:750]

    # C only needs owner/repo; other fields stay in raw for the SQLite stage
    names = [repo['full_name'] for repo in top_750]
    all_names.extend(names)


with open('data/processed/repos_to_process.txt', 'w', encoding ='utf-8') as f:
    for name in all_names:
        f.write(name + '\n')