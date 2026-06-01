import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

def scrape_data(url, element_tag, class_name=None):
    """Scrapes specific elements from a webpage and saves them to a CSV."""

    # Headers to mimic a real browser to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"🔄 Connecting to {url}...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for HTTP errors
    except Exception as e:
        print(f"❌ Error connecting to website: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"🔍 Searching for <{element_tag}> with class: '{class_name}'...")

    if class_name:
        elements = soup.find_all(element_tag, class_=class_name)
    else:
        elements = soup.find_all(element_tag)

    if not elements:
        print("⚠️ No matching elements found on the page. Try inspecting the page and using different tags/classes.")
        return

    extracted_data = []
    for el in elements:
        text = el.get_text(strip=True)
        if text:
            extracted_data.append(text)

    print(f"✅ Found {len(extracted_data)} items!")

    # Save to CSV using pandas
    df = pd.DataFrame(extracted_data, columns=['Extracted_Text'])
    filename = "scraped_data.csv"
    df.to_csv(filename, index=False, encoding='utf-8')

    print(f"💾 Data successfully saved to {filename}")

if __name__ == "__main__":
    print("="*50)
    print("🕷️ Universal Web Scraper Pro 🕷️")
    print("="*50)

    url = input("Enter the target URL (e.g., https://example.com): ")
    tag = input("Enter the HTML tag to extract (e.g., h1, p, div, span): ")
    css_class = input("Enter the CSS class (optional, press Enter to skip): ")

    if not css_class.strip():
        css_class = None

    if url and tag:
        scrape_data(url, tag, css_class)
    else:
        print("Error: URL and HTML tag are required!")