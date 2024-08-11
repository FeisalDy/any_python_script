# Book Search Scraper

This script is designed to scrape book data from an API by sending requests for multiple pages. It handles retries on request failures and saves the data to JSON files.

## Features

- Requests data from the `https://pre-api.tuishujun.com/api/searchBookByTag` endpoint.
- Handles retries with a configurable delay for request failures.
- Saves each page's data to a separate JSON file.
- Includes a delay between requests to avoid overwhelming the server.

## Setup

1. **Install Dependencies**:

   Ensure you have `requests` installed. You can install it using pip:

   ```bash
   pip install requests
   ```

2. **Configure Parameters:**

   - `max_retries`: Maximum number of retries for failed requests (default is 3).
   - `retry_delay`: Delay between retries in seconds (default is 120 seconds).
   - `pageSize`: Number of items per page (default is 5000).
   - `url`: The API endpoint to fetch the data from.

3. **Run the Script**
