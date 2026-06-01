# The Ultimate Business Automation Toolkit 🚀

Welcome to **The Ultimate Business Automation Toolkit**! This premium bundle contains three powerful Python scripts designed to save you time, generate leads, and keep your digital workspace organized.

## What's Included?

1. **B2B Lead Scraper (`b2b_scraper.py`)**: Automatically extract business emails from websites and directories.
2. **Telegram Mini-CRM Bot (`crm_bot.py`)**: A lightweight customer support bot to receive inquiries and reply directly from Telegram.
3. **Smart Data Organizer (`organizer.py`)**: Instantly clean up messy folders (like Downloads) by sorting files into categorized folders based on their type.

---

## Prerequisites

Before running the scripts, you need to have Python installed on your computer.

### Step 1: Install Python
If you don't have Python installed, download it from the official website:
👉 [Download Python](https://www.python.org/downloads/)

*Note for Windows users:* During installation, **make sure to check the box** that says `Add Python to PATH`.

### Step 2: Open a Terminal or Command Prompt
- **Windows:** Press `Win + R`, type `cmd`, and press Enter.
- **Mac:** Press `Cmd + Space`, type `Terminal`, and press Enter.

### Step 3: Navigate to the Toolkit Folder
Use the `cd` command to navigate to the folder where you extracted this toolkit.
```bash
cd path/to/business_automation_toolkit
```

### Step 4: Install Dependencies
Run the following command to install the required Python libraries for the scripts to work:
```bash
pip install -r requirements.txt
```

---

## How to Use the Scripts

### 1. B2B Lead Scraper (`b2b_scraper.py`)
This script scans a website and collects email addresses into a neat CSV file.

**Usage:**
```bash
python b2b_scraper.py <URL> --keyword <optional_keyword> --pages <number_of_pages>
```

**Example:**
To scrape emails from an agency directory up to 2 pages deep:
```bash
python b2b_scraper.py https://example-agency-directory.com --pages 2
```
*Results will be saved in a file called `leads.csv` in the same folder.*

---

### 2. Telegram Mini-CRM Bot (`crm_bot.py`)
This script runs a Telegram bot that forwards customer messages to you and allows you to reply directly.

**Setup:**
1. Open Telegram and search for `@BotFather`.
2. Send `/newbot` and follow the instructions to create a bot.
3. Copy the **HTTP API Token** provided by BotFather.
4. Create a file named `.env` in this folder (or rename an existing `.env.example`).
5. Open the `.env` file in a text editor and add your token and your Telegram User ID (you can get your ID from `@userinfobot`):
   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_IDS=your_telegram_id_here
   ```

**Running the Bot:**
```bash
python crm_bot.py
```
*Keep this terminal window open. While it's running, your bot is active!*

**Replying to Customers:**
When a customer messages the bot, you will receive a notification. To reply, send this command to the bot:
`/reply <user_id> <your message>`

---

### 3. Smart Data Organizer (`organizer.py`)
Instantly declutter any folder by categorizing files into folders like "Images", "Documents", "Videos", etc.

**Usage:**
```bash
python organizer.py <path_to_directory>
```

**Example:**
To organize your Downloads folder (replace with your actual username):
- **Windows:** `python organizer.py "C:\Users\YourName\Downloads"`
- **Mac:** `python organizer.py "/Users/YourName/Downloads"`

---

## Support & Troubleshooting

- **"pip is not recognized"**: Ensure you checked "Add Python to PATH" during installation. You may need to reinstall Python and check that box.
- **Bot isn't responding**: Make sure the script is running in your terminal and your `.env` file contains the correct `BOT_TOKEN`.
- **Scraper found 0 emails**: Some modern websites hide emails using JavaScript to prevent scraping. Try targeting simpler HTML directories or contact pages directly.

Enjoy your new automated workflow! 🎉
