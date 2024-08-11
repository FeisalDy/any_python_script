# Pixiv Novel Scraper

This is a Flask application that uses the `pixivpy3` library to interact with the Pixiv API and fetch information about novels. The application provides endpoints to search for novels, filter novels by word count, and view specific novels.

## Setup

1. **Install Dependencies**:

   Make sure you have `Flask` and `pixivpy3` installed. You can install them using pip:

   ```bash
   pip install Flask pixivpy3
   ```
2. **Configuration**:

   Update the \_REFRESH_TOKEN variable with your Pixiv API refresh token.
3. **Run the Application:**

   Run the Flask application:

   ```bash
   python pixiv_novel_api.py
   ```

   The application will be available at `http://localhost:5000`.
