import requests
from bs4 import BeautifulSoup
import json
import string
import random


def scrape_titles(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Failed to retrieve the web page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    N = 7

    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        filename = meta_description.get('content').split()[0] + ".json"
    else:
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N))
        filename = res + '.json'

    titles = []

    for element in soup.find_all():
        if element.name == 'dt' and element.get_text() == "随机推荐":
            print("Reached <dt> tag with text '随机推荐'. Stopping the script.")
            break

        if element.name == 'span' and element.has_attr('title'):
            title = element['title']
            titles.append(title)

    return titles, filename


def save_titles_to_json(titles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    url = input("Enter the URL of the webpage to scrape titles from: ")
    # filename = input("Enter the name of the output JSON file: ") + '.json'

    # titles = scrape_titles(url)
    titles, filename = scrape_titles(url)

    if titles:
        save_titles_to_json(titles, filename)
        print(f"Titles saved to {filename}")
    else:
        print("No titles found.")

# python script_name.py https://www.example.com output_file.json
