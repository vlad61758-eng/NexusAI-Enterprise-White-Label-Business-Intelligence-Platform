# Cold Email Outreach Automator 📧🤝

A professional Python script for B2B salespeople, freelancers, and agency owners to automate personalized cold email outreach. This script reads leads from a CSV file, customizes the email template for each person, and sends them out with random human-like delays to ensure high deliverability and avoid spam filters.

## Features
- Dynamic variables: Automatically inserts the lead's First Name and Company Name into the email.
- Anti-Spam Delays: Waits a random amount of time (e.g., 1-3 minutes) between each email so Gmail doesn't flag your account as a bot.
- Easy to use: No complex database setup, just a simple CSV file.

## Setup Instructions 🛠️

### 1. Install Python
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
*Important for Windows users: When installing, make sure to check the box that says "Add Python to PATH".*

### 2. Get an App Password (For Gmail users)
For security, Gmail does not let scripts log in with your normal password. You need an "App Password".
1. Go to your Google Account Management -> Security.
2. Turn on 2-Step Verification (if it isn't already).
3. Search for "App Passwords" in the Google Account search bar.
4. Create a new App Password (name it "Email Script" or similar).
5. Google will give you a 16-letter code. Copy this code.

### 3. Install Dependencies
Open your terminal (or Command Prompt) inside this folder and run:
```bash
pip install -r requirements.txt
```

### 4. Configure Credentials
1. In this folder, create a new file named exactly `.env`.
2. Open it in a text editor and add these lines:
```text
SENDER_EMAIL=your_actual_email@gmail.com
SENDER_APP_PASSWORD=the_16_letter_code_from_google
```

## How to Run 🚀

### 1. Prepare your Leads
Run the script once to generate a sample `leads.csv` file:
```bash
python automator.py
```
Open `leads.csv` in Excel or Google Sheets and replace the sample data with your real leads. Keep the column headers exactly as they are (`Email`, `FirstName`, `CompanyName`).

### 2. Edit the Email Template
Open `automator.py` in a text editor. Look for the section labeled `--- EDIT YOUR EMAIL TEMPLATE HERE ---` and customize the subject line and body text to pitch your own product/service.

### 3. Launch the Campaign
When your CSV is ready and your template is written, run the script again:
```bash
python automator.py
```
The script will log into your email and start sending messages one by one, waiting a random amount of time between each to keep your account safe.