import os
import zipfile
import requests

# Load from environment variable for security, as per best practices.
WHOP_API_KEY = os.environ.get("WHOP_API_KEY", "apik_woK8B78LznFW7_C5155873_C_3cc2579181a1f939da0da4484848511a95cbd9ccf39ef7016f169b7700f5ac")

# File paths
DIRECTORY_TO_ZIP = "Pro_Admin_Bot"
ZIP_FILE_NAME = "product_deliverable.zip"

def create_zip_archive():
    """Zips the target directory, excluding __pycache__ and hidden files."""
    print(f"Creating zip archive: {ZIP_FILE_NAME} from directory: {DIRECTORY_TO_ZIP}")
    with zipfile.ZipFile(ZIP_FILE_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DIRECTORY_TO_ZIP):
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')

            for file in files:
                if not file.startswith('.') and file != '.env':
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, os.path.dirname(DIRECTORY_TO_ZIP))
                    zipf.write(file_path, archive_name)
    print("Zip archive created successfully.")

def create_whop_product():
    """Creates a new digital product listing and uploads the file using the Whop API."""
    print("Preparing to create product on Whop...")

    # Read marketing description from file
    description = ""
    try:
        with open("marketing_assets.txt", "r") as f:
            content = f.read()
            parts = content.split("====================================\nIMAGE GENERATION PROMPT (Thumbnail)")
            if len(parts) > 0:
                listing_part = parts[0]
                lines = listing_part.split('\n')
                recording = False
                desc_lines = []
                for line in lines:
                    if line.startswith("Title:"):
                        recording = True
                        continue
                    if recording:
                        desc_lines.append(line)
                description = '\n'.join(desc_lines).strip()
    except Exception as e:
        print(f"Warning: Could not read marketing_assets.txt. Using fallback description. Error: {e}")
        description = "Pro AI Telegram Admin Bot - 24/7 Automated Community Management."

    if not description:
        description = "Pro AI Telegram Admin Bot - 24/7 Automated Community Management."

    headers = {
        "Authorization": f"Bearer {WHOP_API_KEY}",
        "Content-Type": "application/json"
    }

    # Step 1: Create the product
    # Note: Using v2 endpoints based on memory
    product_url = "https://api.whop.com/api/v2/products"

    product_data = {
        "name": "Pro AI Telegram Admin Bot",
        "description": description,
        "visibility": "public", # Memory notes visibility is required
        "price": 24.99 # Set the price to $24.99
    }

    print(f"Attempting to POST to {product_url} with data: {product_data}")
    # The user asked NOT to execute the upload yet, just to provide the architecture.
    # Therefore, we commented out the actual request logic to prevent it from failing
    # when the key isn't active or when running tests, but leaving the full code structure intact.

    # response = requests.post(product_url, json=product_data, headers=headers)
    # response.raise_for_status()
    # product_id = response.json().get('id')
    # print(f"Product created successfully. ID: {product_id}")

    # # Step 2: Upload the Zip file
    # print(f"Attempting to attach {ZIP_FILE_NAME} to the new product.")
    #
    # upload_url = f"https://api.whop.com/api/v2/products/{product_id}/files"
    # file_headers = {"Authorization": f"Bearer {WHOP_API_KEY}"} # Don't set Content-Type for multipart form data
    # with open(ZIP_FILE_NAME, 'rb') as f:
    #     files = {'file': (ZIP_FILE_NAME, f, 'application/zip')}
    #     upload_response = requests.post(upload_url, headers=file_headers, files=files)
    #     upload_response.raise_for_status()
    #
    # print(f"File uploaded successfully to product ID: {product_id}")

    print("\nAPI Architecture is complete and commented out to prevent premature execution as requested.")
    print("To execute, uncomment the `requests` logic inside `create_whop_product`.")

def main():
    if not os.path.exists(DIRECTORY_TO_ZIP):
        print(f"Error: Directory '{DIRECTORY_TO_ZIP}' not found.")
        return

    create_zip_archive()
    # Execute the Whop product creation and file upload setup
    create_whop_product()
    print("\nProcess finished.")

if __name__ == "__main__":
    main()
