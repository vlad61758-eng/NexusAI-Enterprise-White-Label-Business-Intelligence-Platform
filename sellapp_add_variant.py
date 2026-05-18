import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SELLAPP_API_KEY")
PRODUCT_ID = 361982
API_URL = f"https://sell.app/api/v2/products/{PRODUCT_ID}/variants"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

data = {
    "title": "Standard License",
    "description": "Download the toolkit containing all 3 scripts.",
    "deliverable": {
      "types": [
        "MANUAL"
      ],
      "data": {
          "comment": "Thank you! Here is the ZIP toolkit. Since API uploads for files are restricted, please download your files via the link provided or contact support if you have issues."
      }
    },
    "pricing": {
      "humble": False,
      "price": {
        "price": 2499,
        "currency": "USD"
      }
    },
    "minimum_purchase_quantity": 1,
    "payment_methods": [
      "BALANCE"
    ]
}

print(f"Adding variant (price & delivery) to Product ID {PRODUCT_ID}...")
try:
    response = requests.post(API_URL, headers=HEADERS, json=data)

    if response.status_code == 200 or response.status_code == 201:
        print("✅ Variant added successfully!")
    else:
        print(f"❌ Failed to add variant. Status Code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
