# Digital Marketing Agency Lead Scraper

This script automatically searches for digital marketing agencies in specified locations, extracts their website URLs, visits their homepage and contact pages, and extracts valid public contact email addresses. The final output is printed in JSON format.

## Setup Instructions

1. Ensure you have Python 3 installed.
2. Install the required dependencies using pip:

```bash
pip install ddgs requests beautifulsoup4
```

3. Run the script:

```bash
python lead_scraper.py
```

The output will be formatted in JSON exactly as requested, ready to be copy-pasted into an n8n Code node.
