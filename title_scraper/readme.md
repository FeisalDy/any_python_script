# Webpage Title Scraper

## Overview

The **Title Scraper** script extracts titles from a specified webpage and saves them to a JSON file. The filename for the JSON file is determined based on the webpage's meta description, or a random filename is generated if the meta description is not present.

## Features

- **Title Extraction**: Extracts titles from `span` tags with a `title` attribute.
- **Filename Generation**: Uses meta description content or generates a random filename.
- **Termination Condition**: Stops extraction when a specific `<dt>` tag is encountered.

## Requirements

Ensure you have the required libraries installed. You can install them using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

1. **Run the Script** : Execute the script with Python 3.7+.
2. **Enter the URL** : When prompted, input the URL of the webpage from which you want to scrape titles.
