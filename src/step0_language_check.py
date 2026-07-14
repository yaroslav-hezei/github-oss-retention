import requests
import os
from dotenv import load_dotenv
import time
import csv


load_dotenv()
secret = os.getenv("GITHUB_TOKEN")

url = "https://api.github.com/search/repositories"
headers = {"Authorization": f"Bearer {secret}"}

years = range(2016,2021)
languages = ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C++", "C#", "Ruby", "PHP"]
# thresholds_by_year is loaded from star_threshold.csv rather than hardcoded
# because the thresholds are the empirical output of step0_star_threshold.py —
# they vary year by year and would silently drift out of sync with the CSV if
# duplicated as constants here.
thresholds_by_year = {}

with open('data/step0/star_threshold.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        thresholds_by_year[int(row['year'])] = int(row['threshold_found'])

with open('data/step0/final_check.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(['language','year','threshold_used','total_count'])

    for year in years:
        # Using the per-year empirical threshold rather than a fixed 500 avoids
        # overcounting: in competitive years the real bar is several thousand stars,
        # so a fixed 500 would include repos that never make the shared top-750.
        threshold = thresholds_by_year[year]

        for language in languages:

            query = f'language:{language} created:{year}-01-01..{year}-12-31 stars:>{threshold}'
            params = {'q': query, 'per_page': 1}
            
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                writer.writerow([language, year, threshold, data['total_count']])
            else:
                print(f"Error {response.status_code} for {language} {year}")
                
            time.sleep(2)
