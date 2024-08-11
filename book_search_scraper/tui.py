import requests
import time
import json

url = "https://pre-api.tuishujun.com/api/searchBookByTag"
params = {
    "search_value": "",
    "sort_field": "score",
    "pageSize": 5000
}

max_retries = 3 
retry_delay = 120  

for page in range(1, 84):
    params["page"] = page
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  
            data = response.json()
            with open(f"{page}.json", "w") as f:
                json.dump(data, f)
            print(f"Page {page} saved to {page}.json")
            retry_count = 0  # reset retry count
            break  # exit the retry loop
        except requests.exceptions.RequestException as e:
            print(f"Error on page {page}: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Maximum retries reached. Skipping page {page}.")
                break
    time.sleep(120)  # wait for 2 minute before sending the next request
