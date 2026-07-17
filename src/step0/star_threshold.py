import requests
import os
from dotenv import load_dotenv
import time
import csv


load_dotenv()
secret = os.getenv("GITHUB_TOKEN")

url = "https://api.github.com/search/repositories"
headers = {"Authorization": f"Bearer {secret}"}

api_calls = 0

N_low = 500
N_high = 1000
years = list(range(2016,2026))


with open("data/step0/star_threshold.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['year', 'threshold_found', 'total_count_at_threshold', 'api_calls'])

    for year in years:

        api_calls = 0
        # N_low starts at 500 without an API call because step0_grid.py already confirmed
        # that every year has well over 750 repos above 500 stars — it is a known lower bound.
        # N_high = 1000 is a cheap first guess; the exponential phase doubles it immediately
        # if 750+ repos still exist above that level.
        N_low = 500
        N_high = 1000

        query = f'created:{year}-01-01..{year}-12-31 stars:>{N_high}'
        params = {'q': query, 'per_page': 1}
        
        response = requests.get(url, params=params, headers=headers)
        api_calls += 1
        data = response.json()

        # Exponential search doubles N_high until the repo count drops below 750,
        # quickly bracketing the true threshold even when it is in the thousands.
        # Pure binary search from 500 upward would need many more API calls for
        # years where the real threshold is far above the starting point.
        while data['total_count'] >= 750:

            N_low = N_high
            N_high = N_high * 2

            query = f'created:{year}-01-01..{year}-12-31 stars:>{N_high}'
            params = {'q' : query, 'per_page' : 1}
            response = requests.get(url, params=params, headers=headers)
            api_calls += 1
            if response.status_code == 200:
                data = response.json()
            else:
                print(f"Error {response.status_code} for {year} N_high={N_high}")

            time.sleep(2)

        # Stored here rather than only inside the binary loop: if the exponential phase
        # already produced a 1-star gap, the binary loop never runs, so this is the only
        # place where total_count_at_high gets set before the CSV write.
        total_count_at_high = data['total_count']

        # The stop condition is a 1-star gap rather than a tolerance on total_count.
        # Because GitHub returns integer counts, a gap of 1 means no integer can exist
        # between N_low and N_high — N_high is provably the smallest star count that
        # yields fewer than 750 repos for this year.
        while N_high - N_low > 1:

            N_mid = (N_high + N_low) // 2 

            query = f'created:{year}-01-01..{year}-12-31 stars:>{N_mid}'
            params = {'q' : query, 'per_page' : 1}
            response = requests.get(url, params=params, headers=headers)
            api_calls += 1
            if response.status_code == 200:
                data = response.json()
            else:
                print(f"Error {response.status_code} for {year} N_mid={N_mid}")

            if data['total_count'] >= 750:
                N_low = N_mid
            else:
                N_high = N_mid
                # Updated whenever N_high narrows so the final CSV row reflects the
                # count at the actual threshold, not the coarser exponential-phase value.
                total_count_at_high = data['total_count']
            time.sleep(2)

        writer.writerow([year, N_high, total_count_at_high, api_calls])
        print(f"{year}: threshold={N_high}, total_count={total_count_at_high}, api_calls={api_calls}")

    

