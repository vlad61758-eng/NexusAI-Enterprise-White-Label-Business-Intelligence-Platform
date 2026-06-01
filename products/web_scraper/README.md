# Universal Web Scraper Pro 🕷️📊

A powerful, easy-to-use Python script that extracts text data from almost any website and neatly organizes it into a CSV/Excel file.

## Perfect for:
- **Competitor Analysis:** Scrape product prices and titles from e-commerce stores.
- **Lead Generation:** Extract names or job titles from directories.
- **Data Science:** Gather large datasets for machine learning or analysis.

## Setup Instructions

### 1. Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
*Important for Windows users: When installing, make sure to check the box that says "Add Python to PATH".*

### 2. Install Dependencies
Open your terminal (or Command Prompt) inside this folder and run:
```bash
pip install -r requirements.txt
```

## How to Run 🚀

Open your terminal in this folder and run:
```bash
python scraper.py
```

The script will ask you three questions:
1. **URL:** The website you want to scrape (e.g., `https://example-store.com/products`).
2. **HTML Tag:** The type of element holding the data (e.g., `h2` for titles, `span` for prices, `p` for descriptions).
3. **CSS Class (Optional):** If the data is inside a specific class (e.g., `product-price`), type it here. If you don't know, just press Enter to skip.

*Pro tip: To find the HTML tag and Class, go to the website in Google Chrome, right-click the text you want to extract, and select "Inspect".*

The script will instantly download the data and save it as `scraped_data.csv` in the same folder!