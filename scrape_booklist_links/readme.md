# Booklist Scraper

## Overview

The **Booklist Scraper** script extracts links from a series of web pages on the [bqxs520.com](https://www.bqxs520.com) website. It collects URLs of book lists, saves them to a JSON file, and handles errors by recording pages that encounter issues. The script processes pages in batches to avoid overwhelming the server and includes a delay between requests to ensure respectful scraping.

## Features

- **Asynchronous Scraping**: Utilizes `aiohttp` and `asyncio` for efficient, non-blocking network requests.
- **Incremental Saving**: Updates results and error logs for each batch of pages processed.
- **Error Handling**: Records pages that cause errors, allowing for retrying later without restarting from scratch.
- **Rate Limiting**: Includes a delay between requests to prevent server overload.

## Requirements

Ensure you have the required libraries installed. You can install them using pip:

```bash

pip install aiohttp beautifulsoup4

```

## Usage

1. Update the start_page and end_page: Modify these parameters in the asyncio.run call to specify the range of pages you want to scrape.
2. Run the script: Execute the script with Python 3.7+.

```bash

python scrape_booklist_links.py

```
