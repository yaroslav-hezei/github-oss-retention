import requests
import os
from dotenv import load_dotenv
import time
import csv


load_dotenv()
secret = os.getenv("GITHUB_TOKEN")

url = "https://api.github.com/search/repositories"
headers = {"Authorization": f"Bearer {secret}"}

languages = ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C++", "C#", "Ruby", "PHP"]
# These values are a rough order-of-magnitude ladder, not analytical cutoffs.
# The purpose is to check whether each language/year cell has a non-trivial
# number of repos at each level, so 50/100/500 are spaced on a log scale.
# The exact values do not matter — only the shape of the drop-off does.
thresholds = [50, 100, 500]
years = list(range(2016, 2026))

success = 0
errors = 0

with open("data/step0/result.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['language','year','threshold','total_count'])

    for language in languages:
        for threshold in thresholds:
            for year in years:

                query = f'language:{language} created:{year}-01-01..{year}-12-31 stars:>{threshold}'
                # per_page=1 keeps the response payload minimal — total_count is part of
                # the search metadata and is returned regardless of per_page, so there is
                # no reason to download the full repo list just to read that one number.
                params = {"q": query, "per_page": 1}
                response = requests.get(url, params=params, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    writer.writerow([language, year, threshold, data['total_count']])
                    print(language, year, threshold, data['total_count'])
                    success += 1
                else: 
                    print('ERROR', response.status_code, response.text)
                    errors += 1

                time.sleep(2)

print('Complete!', 'success:', success, 'errors:', errors)
