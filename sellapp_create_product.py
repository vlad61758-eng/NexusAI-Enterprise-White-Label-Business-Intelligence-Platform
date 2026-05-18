import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Required credentials
# API key must be generated from https://sell.app/dashboard/settings?settings=developers
API_KEY = os.getenv("SELLAPP_API_KEY")

if not API_KEY:
    print("Error: SELLAPP_API_KEY environment variable is not set.")
    print("Please add it to your .env file or export it in your terminal.")
    exit(1)

API_URL = "https://sell.app/api/v2/products"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# The marketing copy generated earlier
with open("business_automation_toolkit/marketing_copy.txt", "r") as f:
    description = f.read()

# Create a draft product payload
data = {
    "title": "The Ultimate Business Automation Toolkit | Save Time & Scale Faster",
    "description": description,
    "visibility": "PUBLIC",
    "slug": "ultimate-business-automation-toolkit", # Optional
    "type": "product"
}

# In a full implementation, you would use Multipart requests to upload the ZIP file
# and the product image, but SellApp's v2 API documentation for file uploads (digital items)
# is usually handled as a variant after creating the draft product.
# Here we create the base product.

print("Sending request to Sell.app API to create the product...")
try:
    response = requests.post(API_URL, headers=HEADERS, data=data)

    if response.status_code == 200 or response.status_code == 201:
        result = response.json()
        print("✅ Product created successfully!")
        print(f"Product ID: {result.get('data', {}).get('id')}")
        print(f"Product URL: {result.get('data', {}).get('url')}")
        print("\nNote: You will still need to manually attach the ZIP file as a variant in your dashboard or via the API.")
    else:
        print(f"❌ Failed to create product. Status Code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
