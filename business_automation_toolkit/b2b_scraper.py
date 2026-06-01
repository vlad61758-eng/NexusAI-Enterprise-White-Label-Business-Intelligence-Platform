import requests
from bs4 import BeautifulSoup
import re
import csv
import argparse
import logging
from urllib.parse import urljoin, urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_emails_from_url(url, keyword=None):
    """Scrapes a URL, looking for emails and optional keyword match."""
    emails = set()
    try:
        logging.info(f"Scraping: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        if keyword and keyword.lower() not in text.lower():
            logging.info(f"Keyword '{keyword}' not found on {url}. Skipping.")
            return []

        # Basic email regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        found_emails = re.findall(email_pattern, text)

        # Also check mailto links
        for a_tag in soup.find_all('a', href=True):
            if a_tag['href'].startswith('mailto:'):
                email = a_tag['href'].replace('mailto:', '').split('?')[0] # remove subject/body params
                if re.match(email_pattern, email):
                    found_emails.append(email)

        for email in found_emails:
            # Filter out some common false positives like image extensions
            if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.webp')):
                 emails.add(email.lower())

        return list(emails)

    except requests.RequestException as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return []
    except Exception as e:
        logging.error(f"An error occurred while processing {url}: {e}")
        return []


def scrape_directory(base_url, keyword=None, max_pages=1):
    """Scrapes multiple pages starting from a base URL."""
    all_emails = set()
    urls_to_visit = [base_url]
    visited_urls = set()

    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc

    pages_scraped = 0

    while urls_to_visit and pages_scraped < max_pages:
        current_url = urls_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)

        emails_found = extract_emails_from_url(current_url, keyword)
        all_emails.update(emails_found)
        pages_scraped += 1

        # Very basic crawling: find links on the page that belong to the same domain
        try:
             response = requests.get(current_url, timeout=5)
             if response.status_code == 200:
                 soup = BeautifulSoup(response.text, 'html.parser')
                 for link in soup.find_all('a', href=True):
                     href = link['href']
                     full_url = urljoin(current_url, href)
                     parsed_url = urlparse(full_url)

                     if parsed_url.netloc == base_domain and full_url not in visited_urls:
                         urls_to_visit.append(full_url)
        except Exception:
             pass

    return list(all_emails)


def save_to_csv(emails, filename="leads.csv"):
    """Saves the extracted emails to a CSV file."""
    if not emails:
        logging.info("No emails found to save.")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Email"])
            for email in emails:
                writer.writerow([email])
        logging.info(f"Successfully saved {len(emails)} emails to {filename}")
    except IOError as e:
        logging.error(f"Error saving to {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="B2B Lead Scraper: Extract emails from web directories.")
    parser.add_argument("url", help="The base URL of the directory to scrape.")
    parser.add_argument("--keyword", help="Optional keyword to filter pages.", default=None)
    parser.add_argument("--pages", type=int, help="Maximum number of pages to scrape.", default=1)
    parser.add_argument("--output", help="Output CSV filename.", default="leads.csv")

    args = parser.parse_args()

    logging.info(f"Starting scraper for URL: {args.url}")
    emails = scrape_directory(args.url, keyword=args.keyword, max_pages=args.pages)

    if emails:
         logging.info(f"Found {len(emails)} unique emails.")
         save_to_csv(emails, args.output)
    else:
         logging.warning("No emails were found during scraping.")
