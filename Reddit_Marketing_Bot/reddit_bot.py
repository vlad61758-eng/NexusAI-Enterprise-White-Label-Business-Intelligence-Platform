import os
import time
import logging
import praw
import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables (API keys)
load_dotenv()

# Configuration
STORE_LINK = "https://whop.com/aidreamscape" # Replace with actual Whop link
PRODUCT_NAME = "Pro AI Telegram Admin Bot"
SUBREDDITS = ["Entrepreneur", "SideHustle", "TelegramBots", "CryptoCurrency", "Business"]
KEYWORDS = ["telegram spam", "bot", "manage community", "telegram group", "spam protection", "automate telegram"]

# Initialize Gemini AI (Free API)
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    logging.error("GEMINI_API_KEY not found in environment variables. Check your .env file.")
    exit(1)

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # Fast and cost-effective model

# Initialize Reddit API (PRAW)
try:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="MarketingBot/1.0 by AIDreamscape",
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD")
    )
    logging.info(f"Successfully connected to Reddit as: {reddit.user.me()}")
except Exception as e:
    logging.error(f"Failed to connect to Reddit API: {e}. Check your .env credentials.")
    exit(1)


def generate_reply(post_title, post_text):
    """Uses Gemini AI to generate a natural, helpful reply."""
    prompt = f"""
    You are an expert community manager and developer offering helpful advice on Reddit.
    A user posted this:
    Title: "{post_title}"
    Text: "{post_text}"

    Write a short, friendly, and highly relevant reply (2-4 sentences).
    Acknowledge their problem, give a tiny piece of general advice, and then subtly recommend using an automated tool.
    Mention that the "{PRODUCT_NAME}" is a great plug-and-play solution.
    Include this link naturally at the end: {STORE_LINK}
    Do NOT sound like a spam bot. Sound like a real person sharing a tool they know. Do not use hashtags.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Failed to generate AI content: {e}")
        return None

def main():
    logging.info("Starting Reddit AI Marketing Bot...")
    subreddit_string = "+".join(SUBREDDITS)
    subreddit = reddit.subreddit(subreddit_string)

    # Keep track of replied posts to avoid duplicate replies
    replied_file = "replied_posts.txt"
    if not os.path.exists(replied_file):
        open(replied_file, 'w').close()

    with open(replied_file, "r") as f:
        replied_posts = f.read().splitlines()

    try:
        # Stream new submissions in real-time
        for submission in subreddit.stream.submissions(skip_existing=True):
            if submission.id in replied_posts:
                continue

            text_to_check = (submission.title + " " + submission.selftext).lower()

            # Check if post contains any of our target keywords
            if any(keyword in text_to_check for keyword in KEYWORDS):
                logging.info(f"Target found! Post: {submission.title} (r/{submission.subreddit})")

                # Generate AI response
                reply_text = generate_reply(submission.title, submission.selftext)

                if reply_text:
                    try:
                        # Ensure we don't reply too fast to avoid Reddit shadowbans
                        logging.info("Waiting 30 seconds before replying to appear human...")
                        time.sleep(30)

                        # Post the comment
                        # submission.reply(reply_text) # UNCOMMENT THIS TO ACTUALLY POST ON REDDIT

                        logging.info(f"SUCCESS: Replied to post {submission.id}")
                        print(f"--- Generated Reply ---\n{reply_text}\n-----------------------")

                        # Save ID to prevent double-posting
                        with open(replied_file, "a") as f:
                            f.write(submission.id + "\n")

                    except praw.exceptions.RedditAPIException as e:
                        logging.error(f"Reddit API Rate Limit or Error: {e}")
                        # Usually happens if account is new (low karma). Sleep for 10 mins.
                        time.sleep(600)

    except KeyboardInterrupt:
        logging.info("Bot manually stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
