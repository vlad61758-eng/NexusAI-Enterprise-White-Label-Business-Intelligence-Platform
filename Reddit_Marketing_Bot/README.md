# Reddit AI Marketing Bot 🤖📈

This automated script generates free, targeted organic traffic for your digital products by scanning relevant Reddit communities (subreddits) and replying to potential customers with natural, AI-generated recommendations.

This is the ultimate "Zero-Cost" marketing strategy for your Whop store.

## 🚀 How It Works
1. **Scans:** The bot constantly monitors subreddits like `r/Entrepreneur`, `r/TelegramBots`, and `r/SideHustle`.
2. **Identifies:** It looks for posts containing keywords like "telegram spam", "automate group", etc.
3. **Generates:** It uses Google's Gemini AI to read the post context and write a helpful, human-like response.
4. **Promotes:** It naturally weaves a link to your Whop store (`https://whop.com/aidreamscape`) into the advice.

## 🛠️ Step 1: Get Free API Keys

You need two free API keys for this to work.

### 1. Get Google Gemini API Key (Free AI)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **"Create API key"**.
4. Copy the key and save it.

### 2. Get Reddit API Credentials (Free)
1. Create a Reddit account (preferably a new one that looks like a real person, give it some avatar and a few normal comments first).
2. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps).
3. Scroll down and click **"Create another app..."** (or "Create app").
4. Fill in the details:
   - **name:** MarketingBot (or anything)
   - **type:** Select **"script"**
   - **description:** Optional
   - **about url:** Optional
   - **redirect uri:** `http://localhost:8080`
5. Click **"Create app"**.
6. You will now see:
   - Your **Client ID** (under the name "MarketingBot", looks like `xX_abc123_Xx`)
   - Your **Client Secret** (labeled "secret", a long string)

## ⚙️ Step 2: Setup

1. Make sure you have Python installed.
2. Open your terminal/command prompt in the `Reddit_Marketing_Bot` folder.
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a new file in this folder named exactly `.env`.
5. Open the `.env` file in a text editor and add your keys like this (replace the placeholders with your actual keys):

   ```env
   # Google Gemini
   GEMINI_API_KEY=your_gemini_api_key_here

   # Reddit
   REDDIT_CLIENT_ID=your_reddit_client_id_here
   REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
   REDDIT_USERNAME=your_reddit_username_here
   REDDIT_PASSWORD=your_reddit_password_here
   ```
6. Save the `.env` file.

## ▶️ Step 3: Run the Bot

1. Open `reddit_bot.py` in a text editor.
2. Find line 89: `# submission.reply(reply_text) # UNCOMMENT THIS TO ACTUALLY POST ON REDDIT`
3. Remove the `#` at the start of that line to activate live posting. (Leave it commented if you just want to test and see what the AI generates without actually posting).
4. Run the script:
   ```bash
   python reddit_bot.py
   ```

**⚠️ Important Tips for Success:**
- **Karma is King:** Brand new Reddit accounts have posting limits. If your bot crashes with a "Rate Limit" error, it means Reddit is telling you to wait. The script automatically pauses for 10 minutes when this happens. To avoid this, use a Reddit account that is a few weeks old and has at least 50-100 "Karma" (upvotes on normal posts/comments).
- **Don't Spam:** The bot is configured to wait 30 seconds before posting to look human. Do not remove this delay, or Reddit will ban the account instantly.
