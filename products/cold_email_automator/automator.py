import smtplib
import csv
import time
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load credentials
load_dotenv()
EMAIL_ADDRESS = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_APP_PASSWORD")

# Configuration
SMTP_SERVER = "smtp.gmail.com"  # Change if not using Gmail
SMTP_PORT = 587
CSV_FILE = "leads.csv"

# Time to wait between emails to avoid spam filters (in seconds)
MIN_DELAY = 60
MAX_DELAY = 180

def create_email_message(to_email, first_name, company_name):
    """Creates a personalized email message."""

    # --- EDIT YOUR EMAIL TEMPLATE HERE ---
    subject = f"Quick question regarding {company_name}"

    body = f"""Hi {first_name},

I noticed the great work {company_name} is doing and wanted to reach out.

I help businesses like yours automate their daily workflows to save 10+ hours a week. We recently helped a similar company in your industry increase their efficiency by 30%.

Would you be open to a quick 5-minute chat next week to see if this makes sense for {company_name}?

Best regards,
Your Name
Your Title
"""
    # -------------------------------------

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    return msg

def main():
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Error: Missing email credentials in .env file.")
        print("You need SENDER_EMAIL and SENDER_APP_PASSWORD.")
        return

    if not os.path.exists(CSV_FILE):
        print(f"Creating sample {CSV_FILE}...")
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'FirstName', 'CompanyName'])
            writer.writerow(['test1@example.com', 'John', 'TechCorp'])
            writer.writerow(['test2@example.com', 'Sarah', 'DesignStudio'])
        print(f"Please edit {CSV_FILE} with your real leads and run the script again.")
        return

    print("🚀 Starting Cold Email Outreach Automator...")

    leads = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            leads.append(row)

    print(f"Found {len(leads)} leads to email.\n")

    try:
        # Connect to server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ Login successful!\n")

        for index, lead in enumerate(leads):
            to_email = lead['Email']
            first_name = lead['FirstName']
            company_name = lead['CompanyName']

            print(f"[{index + 1}/{len(leads)}] Sending email to {to_email} ({company_name})...")

            msg = create_email_message(to_email, first_name, company_name)
            server.send_message(msg)

            print("✅ Sent successfully.")

            # Don't delay after the very last email
            if index < len(leads) - 1:
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"⏳ Waiting {delay} seconds to mimic human behavior and avoid spam filters...\n")
                time.sleep(delay)

        server.quit()
        print("\n🎉 All emails sent successfully!")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Note: If using Gmail, make sure you generated an 'App Password', not your regular login password.")

if __name__ == "__main__":
    main()