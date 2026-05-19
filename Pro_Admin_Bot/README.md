# Pro AI Telegram Admin Bot 🤖

Welcome to the Pro AI Telegram Admin Bot! This is a powerful, production-ready Telegram group management assistant built with Python and `aiogram`.

## ✨ Features

- **Auto-Welcome:** Greets new users automatically when they join your group.
- **Anti-Spam Filter:** Automatically deletes messages containing prohibited words (e.g., 'spam', 'scam', 'crypto', 'link') and warns the user.
- **Mute Users:** Admins can easily mute users for a specific number of minutes.
- **Ban Users:** Admins can instantly ban disruptive users from the group.

## 🚀 Quick Start Guide

Follow these simple steps to get your bot running:

### 1. Get a Bot Token
1. Open Telegram and search for **@BotFather**.
2. Send the `/newbot` command.
3. Follow the prompts to choose a name and username for your bot.
4. BotFather will give you an **API Token** (it looks like a long string of letters and numbers). **Keep this secret!**

### 2. Install Python
Make sure you have Python installed on your computer. You can download it from [python.org](https://www.python.org/downloads/). Python 3.8 or higher is recommended.

### 3. Install Dependencies
Open your terminal (or Command Prompt) in the folder where you saved this bot (`Pro_Admin_Bot`). Run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```

### 4. Configure Your Bot
1. Open `bot.py` in any text editor.
2. Find the line that says:
   `BOT_TOKEN = "YOUR_BOT_TOKEN"`
3. Replace `"YOUR_BOT_TOKEN"` with the actual token you got from BotFather. Save the file.

### 5. Run the Bot
In your terminal, while in the `Pro_Admin_Bot` directory, run:

```bash
python bot.py
```

You should see a message saying "Bot is starting...". Your bot is now live!

## ⚙️ How to Use in Your Group

1. Add the bot to your Telegram group just like you would add a regular user.
2. **Important:** Promote the bot to **Administrator** in your group settings. It needs permissions to delete messages, restrict users, and ban users.
3. Once it's an admin, it will start working automatically!

### Admin Commands
As a group admin, you can reply to a user's message with these commands:
- `/mute [minutes]` (e.g., `/mute 10`) - Mutes the user for the specified time. Defaults to 10 minutes if no time is provided.
- `/ban` - Permanently bans the user from the group.

Enjoy your automated, spam-free community! 🎉
