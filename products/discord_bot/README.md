# Discord Community Manager Bot 🤖🛡️

A powerful Python bot to manage your Discord server. It automatically welcomes new users, deletes spam/scam messages, and gives admins simple commands to clean up chats.

## Features
- **Auto-Welcome:** Greets new members when they join.
- **Auto-Moderation:** Instantly deletes messages containing specific words (like "scam", "crypto giveaway").
- **Chat Cleaner:** Admins can type `!clear 10` to instantly delete the last 10 messages.

## Setup Instructions

### 1. Create a Discord Bot App
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click "New Application" and name your bot.
3. Go to the "Bot" tab on the left.
4. Scroll down to **Privileged Gateway Intents** and enable:
   - Server Members Intent
   - Message Content Intent
   - (Save changes!)
5. Click "Reset Token" and copy the new token.

### 2. Invite Bot to Your Server
1. In the Developer Portal, go to "OAuth2" -> "URL Generator".
2. Check `bot` under Scopes.
3. Check `Administrator` under Bot Permissions.
4. Copy the generated URL at the bottom, paste it in your browser, and invite the bot to your server.

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Bot
Create a `.env` file in this folder and add your token:
```text
DISCORD_TOKEN=your_token_here
```

### 5. Run the Bot
```bash
python bot.py
```