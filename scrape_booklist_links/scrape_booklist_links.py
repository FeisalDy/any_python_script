import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import os
import time


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_page(session, page_num):
    url = f'https://www.bqxs520.com/booklist_{page_num}.shtml'
    print(f'Scraping {url}...')

    try:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')

        links = []
        items = soup.find_all('div', class_='imgmain')
        for item in items:
            link_tag = item.find('a')
            if link_tag:
                link = 'https://www.bqxs520.com' + link_tag['href']
                links.append(link)

        print(f'Page {page_num} found {len(links)} links.')
        return links, None  # No error occurred

    except Exception as e:
        print(f'Error occurred while scraping {url}: {e}')
        return [], page_num  # Return the page number that caused the error


async def scrape_bqxs520_links(start_page=1, end_page=2443, output_file='booklist_links.json', error_file='error_pages.json', delay=20, batch_size=50):
    # Load existing data if the file exists
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            all_links = json.load(f)
    else:
        all_links = []

    # Load existing error pages if the file exists
    if os.path.exists(error_file):
        with open(error_file, 'r', encoding='utf-8') as f:
            error_pages = json.load(f)
    else:
        error_pages = []

    # Process pages in batches
    for start in range(start_page, end_page + 1, batch_size):
        end = min(start + batch_size - 1, end_page)
        async with aiohttp.ClientSession() as session:
            tasks = [scrape_page(session, page_num)
                     for page_num in range(start, end + 1)]
            results = await asyncio.gather(*tasks)

            # Process results and update files
            batch_links = []
            batch_errors = []

            for links, error_page in results:
                if links:
                    batch_links.extend(links)
                if error_page is not None:
                    batch_errors.append(error_page)

            # Update all_links and error_pages
            all_links.extend(batch_links)
            error_pages.extend(batch_errors)

            # Remove duplicates from all_links
            all_links = list(set(all_links))

            # Save the updated data to the JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_links, f, ensure_ascii=False, indent=4)

            # Save the error pages to a separate JSON file
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_pages, f, ensure_ascii=False, indent=4)

        # Delay to avoid overwhelming the server
        time.sleep(delay)

    print(f'Scraping completed. Total links found: {len(all_links)}')

# Example usage
asyncio.run(scrape_bqxs520_links(start_page=400, end_page=2443,
            output_file='booklist_links.json', error_file='error_pages.json'))
