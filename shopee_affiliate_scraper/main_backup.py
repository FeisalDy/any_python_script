import requests
import json
import time

# API URL and Headers
base_url = "https://affiliate.shopee.co.id/api/v3/offer/product/list"
headers = {
    "Cookie": "SPC_F=AGe7GC2q4G0yekZSvFCS0hrb9P7lMROU; REC_T_ID=8a26a099-f5ca-11ee-9ddf-96f7a566bb20; SPC_CLIENTID=QUdlN0dDMnE0RzB5lmussirqymdrvtdi; SPC_U=-; SPC_R_T_ID=U3lswZUPM5YPGt63Lh46P9ZiAR2ZMv2xly2a7hCQScwtStLwzOnhtZpAMYmy4E+/YxG29F1kzWm2CntNzerKFk6QMwg2etB2GEeZSyt5uuYy6wPN87NRoJ4h5I+1UDbwQ9o14hOXrh0wmosilei53aHbKMIqmbznOBnPlvT6l2U=; SPC_R_T_IV=RmRzdTZjTFVITHdLaUl0WA==; SPC_T_ID=U3lswZUPM5YPGt63Lh46P9ZiAR2ZMv2xly2a7hCQScwtStLwzOnhtZpAMYmy4E+/YxG29F1kzWm2CntNzerKFk6QMwg2etB2GEeZSyt5uuYy6wPN87NRoJ4h5I+1UDbwQ9o14hOXrh0wmosilei53aHbKMIqmbznOBnPlvT6l2U=; SPC_T_IV=RmRzdTZjTFVITHdLaUl0WA==; language=id; _sapid=d4eddad04126d7b7fc7153c0c9de46132d5798b44b55a9835b8abd40; _QPWSDCXHZQA=eb3731ee-a1d1-49e1-d9fb-2b017d51ec28; REC7iLP4Q=56487ba6-8c1c-4547-a54f-bd8860ec608f; SPC_SI=Y37yZgAAAAA2NzJqdngycfWvfgMAAAAAb096Ymx5cVM=; SPC_EC=.ZnEyYzhQZzg3Q0lqUUkzb+sFH7RYNWHnpXsBK58j78F7Ueg2cvnNWGbo/HldvQB6Yh2j444bn/cInDHGsCLdOsS+7f1f0HDfbQ7iRmlkiZko6ytdA92TTWsBkNLC9D31qITVdQkjMP3iwh2SZObQDsbj7CfpiYMnQn9l6eloBkkTkfxYp2e5ILvUIMrogHDdYKwwGzIReV2QxiNJm/SReULAPANF4Gsv8ALGof5ir4c=; SPC_ST=.ZnEyYzhQZzg3Q0lqUUkzb+sFH7RYNWHnpXsBK58j78F7Ueg2cvnNWGbo/HldvQB6Yh2j444bn/cInDHGsCLdOsS+7f1f0HDfbQ7iRmlkiZko6ytdA92TTWsBkNLC9D31qITVdQkjMP3iwh2SZObQDsbj7CfpiYMnQn9l6eloBkkTkfxYp2e5ILvUIMrogHDdYKwwGzIReV2QxiNJm/SReULAPANF4Gsv8ALGof5ir4c=; shopee_webUnique_ccd=uvFlKcG1z4xU7kv%2FDWOFJQ%3D%3D%7ClCsBW4Jvy7koyk9p44ii56%2BXYZUb1HuEMpXCjNdP5ZbuWHKseNIXUwLomgSk9N64W%2BWMUGOt6%2FigI4E%3D%7CkbRDUWX7ZoFpA5%2Fm%7C08%7C3; ds=5b2bce29d68778a3f7f581166f6292a6"
}

params = {
    "list_type": 0,
    "keyword": "tas",
    "sort_type": 2,
    "page_offset": 0,
    "page_limit": 20,  # Adjust as needed
    "client_type": 1,
    "filter_types": 2
}

# Function to filter and save items


def save_filtered_results(items, file_count, data_accumulator):
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

    # Save to JSON when the list reaches 100 items
    if len(data_accumulator["list"]) >= 100:
        with open(f"filtered_results_{file_count}.json", "w") as json_file:
            json.dump(data_accumulator, json_file, indent=4)
        file_count += 1
        data_accumulator["list"] = []  # Reset list

    return file_count

# Main loop to fetch and process pages


def fetch_and_process():
    page_offset = 0
    file_count = 1
    total_count = 0
    data_accumulator = {
        "affiliate_short_link": True,
        "list": [],
        "sub_ids": ["", "", "", "", ""]
    }

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
                    items, file_count, data_accumulator)

            # Check if we reached the total count or if list is empty
            if len(items) < params["page_limit"] or page_offset >= total_count:
                break  # End the loop if there are no more pages
        else:
            print(f"Error fetching data: {response.status_code}")
            break

        page_offset += params["page_limit"]
        print(f"Processed {page_offset} pages")
        time.sleep(3)  # Wait 3 seconds before fetching the next page

    # Save any remaining items in the accumulator
    if data_accumulator["list"]:
        with open(f"filtered_results_{file_count}.json", "w") as json_file:
            json.dump(data_accumulator, json_file, indent=4)


if __name__ == "__main__":
    fetch_and_process()
