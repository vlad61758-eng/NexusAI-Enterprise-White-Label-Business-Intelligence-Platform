import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json
from urllib.parse import urljoin, urlparse

try:
    from googlesearch import search
    HAS_GOOGLESEARCH = True
except ImportError:
    HAS_GOOGLESEARCH = False

# 1. Define queries
QUERIES = [
    "top digital marketing agency Texas",
    "SEO agency London"
]

# 2. Regex and Filters
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
IGNORE_EMAILS = ["example", "sentry", "wix", "test", "domain", "email", "yourdomain", "company", "name"]
IGNORE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css')

def is_valid_email(email):
    email = email.lower()
    if any(ignore in email for ignore in IGNORE_EMAILS):
        return False
    if email.endswith(IGNORE_EXTENSIONS):
        return False
    return True

def get_urls(query, num_results=5):
    """Search Google and return URLs."""
    urls = []

    # Try googlesearch-python first
    if HAS_GOOGLESEARCH:
        try:
            # Note: in some googlesearch-python versions it's 'num', in others it's 'num_results'
            for url in search(query, num_results=num_results, lang="en"):
                urls.append(url)
            if urls:
                return urls
        except Exception:
            try:
                for url in search(query, num=num_results, lang="en"):
                    urls.append(url)
                if urls:
                    return urls
            except Exception:
                pass

    return urls

def extract_emails_and_title(url):
    """Visit URL and extract emails using Regex and BeautifulSoup."""
    emails = set()
    title = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract Title
            if soup.title and soup.title.string:
                title = soup.title.string.strip()

            # Extract via Regex from raw text
            found_emails = set(re.findall(EMAIL_REGEX, response.text))

            # Extract via mailto: links (as a fallback)
            for a in soup.find_all('a', href=True):
                if a.get('href') and a['href'].startswith('mailto:'):
                    email = a['href'].replace('mailto:', '').split('?')[0].strip()
                    if email:
                        found_emails.add(email)

            for email in found_emails:
                if is_valid_email(email):
                    emails.add(email)
    except Exception as e:
        pass

    return emails, title

def main():
    leads = []
    visited_domains = set()

    for query in QUERIES:
        urls = get_urls(query, num_results=5)
        for url in urls:
            if not url.startswith('http'):
                url = 'https://' + url

            domain = urlparse(url).netloc
            if domain in visited_domains or not domain:
                continue
            visited_domains.add(domain)

            # 1. Check Homepage
            time.sleep(random.uniform(2, 5)) # Random delay
            emails, title = extract_emails_and_title(url)

            # 2. Check /contact page if no emails found
            if not emails:
                contact_url = urljoin(url, "/contact")
                time.sleep(random.uniform(2, 5)) # Random delay
                more_emails, _ = extract_emails_and_title(contact_url)
                emails.update(more_emails)

            # 3. Check /contact-us page
            if not emails:
                contact_us_url = urljoin(url, "/contact-us")
                time.sleep(random.uniform(2, 5)) # Random delay
                more_emails, _ = extract_emails_and_title(contact_us_url)
                emails.update(more_emails)

            if emails:
                # Clean up business name
                business_name = title.split('-')[0].split('|')[0].strip() if title else domain
                if not business_name:
                    business_name = domain

                # Store only the first valid email for simplicity
                for email in emails:
                    leads.append({
                        "business_name": business_name,
                        "email": email,
                        "website": domain
                    })
                    break # Break after adding one email per agency

    # The output MUST be formatted exactly as JSON
    print(json.dumps(leads, indent=2))

if __name__ == "__main__":
    main()
