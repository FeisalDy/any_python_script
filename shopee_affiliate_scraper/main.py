import requests
import json
import time
import os

# API URL and Headers
base_url = "https://affiliate.shopee.co.id/api/v3/offer/product/list"
headers = {
    "Cookie": "xxxxx"
}

params = {
    "list_type": 0,
    "sort_type": 2,
    "page_offset": 0,
    "page_limit": 20,
    "client_type": 1,
    "filter_types": 2
}

# List of keywords to automate
keywords = ["botol", "garpu"]

# Function to get the latest file and check if it's below 100 items


def get_latest_file_data():
    json_files = [f for f in os.listdir() if f.startswith(
        "filtered_results_") and f.endswith(".json")]
    if not json_files:
        return None, 1  # Start with file count 1 if no files exist
    latest_file = sorted(json_files, key=lambda x: int(
        x.split('_')[-1].split('.')[0]))[-1]
    with open(latest_file, "r") as json_file:
        data = json.load(json_file)
    return data, int(latest_file.split('_')[-1].split('.')[0])

# Function to filter and save items


def save_filtered_results(items, data_accumulator, file_count):
    for item in items:
        commission_rate = float(item["default_commission_rate"].strip('%'))
        historical_sold = item["batch_item_for_item_card_full"]["historical_sold"]

        if commission_rate >= 10 and historical_sold > 300:
            filtered_item = {
                "item_id": item["batch_item_for_item_card_full"]["itemid"],
                "item_name": item["batch_item_for_item_card_full"]["name"],
                "shop_name": item["batch_item_for_item_card_full"]["shop_name"],
                "long_link": item["long_link"],
                "commission_rate": item["default_commission_rate"],
                "price": int(item["batch_item_for_item_card_full"]["price"]),
                "sales": historical_sold,
                "product_link": item["product_link"],
                "from_shop_id": item["batch_item_for_item_card_full"]["shopid"],
                "trace": item["trace"]
            }
            data_accumulator["list"].append(filtered_item)

        # Save when the list reaches 100 items
        if len(data_accumulator["list"]) >= 100:
            with open(f"filtered_results_{file_count}.json", "w") as json_file:
                json.dump(data_accumulator, json_file, indent=4)
            file_count += 1
            data_accumulator["list"] = []  # Reset list

    return file_count

# Main loop to fetch and process pages for multiple keywords


def fetch_and_process():
    for keyword in keywords:
        # Get the latest file data for each keyword
        data_accumulator, file_count = get_latest_file_data()
        if data_accumulator is None:
            data_accumulator = {
                "affiliate_short_link": True,
                "list": [],
                "sub_ids": ["", "", "", "", ""]
            }

        page_offset = 0
        total_count = 0
        params["keyword"] = keyword  # Set the keyword in the params

        while True:
            params["page_offset"] = page_offset
            response = requests.get(base_url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                items = data.get("data", {}).get("list", [])
                total_count = data.get("data", {}).get("total_count", 0)

                # Filter and save items, appending new items to the accumulator
                if items:
                    file_count = save_filtered_results(
                        items, data_accumulator, file_count)

                # Check if we reached the total count or if list is empty
                if len(items) < params["page_limit"] or page_offset >= total_count:
                    break  # End the loop if there are no more pages
            else:
                print(
                    f"Error fetching data for {keyword}: {response.status_code}")
                break

            page_offset += params["page_limit"]
            print(f"Fetching {page_offset} for {keyword}...")
            time.sleep(5)  # Wait 5 seconds before fetching the next page

        # Save any remaining items in the accumulator if it's less than 100
        if data_accumulator["list"]:
            with open(f"filtered_results_{file_count}.json", "w") as json_file:
                json.dump(data_accumulator, json_file, indent=4)
            file_count += 1


if __name__ == "__main__":
    fetch_and_process()
