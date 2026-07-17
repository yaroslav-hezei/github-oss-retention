import requests
import os
import json
from dotenv import load_dotenv
import time 

load_dotenv() 
secret = os.getenv('GITHUB_TOKEN')

url = "https://api.github.com/search/repositories"
headers = {"Authorization": f"Bearer {secret}"}

years = range(2016,2026)
per_page = 100


for year in years:
    # Reset per year: each year is accumulated fully, then written as one file.
    # Declared here (not above the year loop) so it starts empty for every year —
    # otherwise years would bleed into each other in a single growing list.
    bucket = []

    # Pages 1..8 = 800 repos. The sample target is top-750, but trimming is
    # deferred to the parsing step: raw stays as-is. Cannot exceed 10 pages —
    # GitHub search returns at most 1000 results per query.
    for page in range(1,9):

        # q holds only the year — no language/stars qualifiers. The shared
        # top-N is taken by sort alone; language is derived later from the raw.
        query = f'created:{year}-01-01..{year}-12-31'
        params = {'q': query,
                  'sort': 'stars',
                  'order': 'desc', 
                  'per_page': per_page,
                  'page' : page}
        

        # Retry with exponential backoff: a failed page would leave a hole in
        # the middle of the star-sorted sample, so pages are retried, not skipped.
        for attempt in range(1,6):
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                break
            else:
                time.sleep(2**attempt)
        else: 
            # for-else fires only if no break happened, i.e. all 5 attempts failed.
            # Fail loud rather than write a year with a gap.
            raise Exception(f"Failed to fetch year {year} page {page} after 5 attempts")
        
        # extend (not append) with data['items'] to keep the year a flat list
        # of repos, not a nested list of pages.
        bucket.extend(data['items'])

        time.sleep(2)

    with open(f'data/raw/{year}.json', 'w', encoding='utf-8') as f:
        json.dump(bucket,f,indent=4,ensure_ascii=False)