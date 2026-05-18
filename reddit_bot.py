import os
import sys
import time
import logging
import praw
import google.generativeai as genai
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("RedditBot")

# Load configuration
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# The URL to your newly created automated Flask store
STORE_URL = os.getenv("STORE_URL", "https://your-server-ip-or-domain.com")

if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, GEMINI_API_KEY]):
    logger.error("Missing Reddit or Gemini credentials in .env file.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=f"AILeadGenBot by u/{REDDIT_USERNAME}",
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
)

TARGET_SUBREDDITS = ["Entrepreneur", "freelance", "marketing", "sales", "smallbusiness"]

def generate_reply(post_title, post_text):
    """Uses Gemini to generate a natural, helpful reply recommending the AI LeadGen tool."""
    system_prompt = (
        "You are an experienced entrepreneur sharing advice on Reddit. "
        "A user is asking how to find B2B clients or leads. "
        "Write a short, highly natural, friendly, and non-salesy Reddit comment (1-2 paragraphs). "
        "Empathize with them first, then casually mention that you automated this by using a "
        "Telegram AI Lead Generator that scans niche groups 24/7 for keywords and auto-replies. "
        f"Tell them they can get the exact script and instructions here: {STORE_URL}. "
        "Do NOT sound like a corporate bot. Use casual Reddit lingo."
    )

    prompt = f"{system_prompt}\n\nUser Post Title:\n{post_title}\n\nUser Post Content:\n{post_text}"

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

def run_bot():
    logger.info("Starting Reddit LeadGen Bot...")
    subreddit = reddit.subreddit("+".join(TARGET_SUBREDDITS))

    # Listen to new posts continuously
    for submission in subreddit.stream.submissions(skip_existing=True):
        title_lower = submission.title.lower()
        text_lower = submission.selftext.lower()

        # Simple keyword matching to find people looking for leads/clients
        keywords = ["find clients", "get clients", "b2b leads", "looking for leads", "how to find customers"]

        if any(kw in title_lower or kw in text_lower for kw in keywords):
            logger.info(f"Found potential lead! Post: {submission.title}")

            try:
                # Generate AI reply
                reply_text = generate_reply(submission.title, submission.selftext)

                # Simulate human reading time
                logger.info("Generating reply... waiting 30 seconds to appear natural.")
                time.sleep(30)

                # Post comment
                submission.reply(reply_text)
                logger.info(f"Successfully replied to post: {submission.url}")

                # Sleep to avoid Reddit rate limits (avoid getting banned)
                logger.info("Sleeping for 15 minutes before finding the next post...")
                time.sleep(900)

            except Exception as e:
                logger.error(f"Error replying to post: {e}")

if __name__ == "__main__":
    while True:
        try:
            run_bot()
        except Exception as e:
            logger.error(f"Fatal error, restarting in 60s: {e}")
            time.sleep(60)
