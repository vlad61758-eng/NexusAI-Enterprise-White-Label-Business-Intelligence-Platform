import time
import random
import json
import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

# Common User-Agents to prevent blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
]

EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

def is_valid_email(email):
    email = email.lower()
    invalid_domains = ['example.com', 'yourdomain.com', 'domain.com', 'email.com', 'sentry.io']
    invalid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']

    # Check for image/file extensions
    if any(email.endswith(ext) for ext in invalid_extensions):
        return False

    # Check for dummy domains
    domain = email.split('@')[1] if '@' in email else ""
    if domain in invalid_domains or "example" in domain:
        return False

    return True

def extract_emails_from_text(text):
    emails = re.findall(EMAIL_REGEX, text)
    valid_emails = list(set([e for e in emails if is_valid_email(e)]))
    return valid_emails

def fetch_page(url, timeout=10):
    try:
        response = requests.get(url, headers=get_random_headers(), timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        pass
    return None

def extract_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        # Clean up common title suffixes
        title = re.sub(r'\|.*$', '', title).strip()
        title = re.sub(r'-.*$', '', title).strip()
        return title
    return "Unknown Agency"

def scrape_emails_from_website(base_url):
    extracted_emails = set()
    business_name = "Unknown Agency"

    # Check homepage
    html = fetch_page(base_url)
    if html:
        business_name = extract_title(html)
        emails = extract_emails_from_text(html)
        extracted_emails.update(emails)

        # If no emails found on homepage, try /contact
        if not extracted_emails:
            time.sleep(random.uniform(1, 3))
            contact_url = urljoin(base_url, '/contact')
            contact_html = fetch_page(contact_url)
            if contact_html:
                contact_emails = extract_emails_from_text(contact_html)
                extracted_emails.update(contact_emails)

        # Optional: Try /about if still no emails
        if not extracted_emails:
            time.sleep(random.uniform(1, 3))
            about_url = urljoin(base_url, '/about')
            about_html = fetch_page(about_url)
            if about_html:
                about_emails = extract_emails_from_text(about_html)
                extracted_emails.update(about_emails)

    return list(extracted_emails), business_name

def main():
    queries = [
        "top digital marketing agency Texas",
        "SEO agency London"
    ]

    num_results_per_query = 5
    results = []
    seen_domains = set()

    with DDGS() as ddgs:
        for query in queries:
            try:
                # Use duckduckgo-search to get search results
                search_results = [r for r in ddgs.text(query, max_results=num_results_per_query)]

                for r in search_results:
                    url = r['href']
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc.replace('www.', '')

                    # Skip social media, directories, and already seen domains
                    skip_domains = ['facebook.com', 'linkedin.com', 'clutch.co', 'yelp.com', 'upcity.com', 'instagram.com', 'twitter.com', 'google.com', 'designrush.com', 'semrush.com', 'topdevelopers.co', 'sortlist.com', 'themanifest.com']
                    if domain in seen_domains or any(skip in domain for skip in skip_domains):
                        continue

                    seen_domains.add(domain)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

                    time.sleep(random.uniform(2, 5))  # Delay before scraping site

                    emails, business_name = scrape_emails_from_website(base_url)

                    if emails:
                        results.append({
                            "business_name": business_name,
                            "email": emails[0],  # Take the first valid email found
                            "website": domain
                        })

            except Exception as e:
                # Silently pass errors from search engine
                pass

            time.sleep(random.uniform(5, 10))  # Delay between queries

    # Output exact JSON format as required
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
