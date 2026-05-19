import os
import time
import random
import praw
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="Automated Promo Bot 1.0 by /u/your_username",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Store Link
STORE_URL = "https://aidreamscape.sell.app/"

# Subreddits to monitor
SUBREDDITS = ["Entrepreneur", "SideProject", "marketing", "startups", "freelance"]

# Keywords to look for in posts
TARGET_KEYWORDS = [
    "seo", "blogging", "content creation", "cold email", "lead generation",
    "automate", "crypto alerts", "tracking prices"
]

# Track replied posts to avoid duplicate comments
replied_file = "replied_posts.txt"
if not os.path.exists(replied_file):
    open(replied_file, 'w').close()

def get_replied_posts():
    with open(replied_file, 'r') as f:
        return set(f.read().splitlines())

def save_replied_post(post_id):
    with open(replied_file, 'a') as f:
        f.write(post_id + '\n')

def generate_reply(post_title, post_body):
    """Uses AI to generate a contextual, non-spammy reply."""
    prompt = f"""
    You are an entrepreneur sharing a helpful tip on Reddit.
    Read the following Reddit post and write a short, helpful, and natural-sounding comment (2-3 sentences).
    Do NOT sound like a marketer or a bot. Be conversational.
    At the end of your helpful advice, organically mention that you use some Python automation scripts from this store: {STORE_URL} that have saved you a ton of time.

    Post Title: {post_title}
    Post Body: {post_body}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def main():
    print("🤖 Starting Reddit Promo Bot...")
    replied_posts = get_replied_posts()

    # Create a string of subreddits separated by + (e.g., "Entrepreneur+marketing")
    subreddit_string = "+".join(SUBREDDITS)
    subreddit = reddit.subreddit(subreddit_string)

    try:
        print(f"Scanning the newest posts in: {subreddit_string}...")

        # Check the newest 25 posts across those subreddits
        for submission in subreddit.new(limit=25):

            if submission.id in replied_posts:
                continue

            # Check if any keyword is in the title or body
            text_to_check = (submission.title + " " + submission.selftext).lower()
            if any(keyword in text_to_check for keyword in TARGET_KEYWORDS):
                print(f"\nFound relevant post: {submission.title}")
                print("Generating AI response...")

                reply_text = generate_reply(submission.title, submission.selftext)

                if reply_text:
                    print(f"Generated Reply: {reply_text}")
                    print("Waiting 10 seconds before posting...")
                    time.sleep(10) # Pause before action

                    # UNCOMMENT THE LINE BELOW TO ACTUALLY POST THE COMMENT.
                    # Currently set to 'print only' for safety during testing.
                    # submission.reply(reply_text)

                    save_replied_post(submission.id)
                    print("✅ Reply posted successfully (simulated)!")

                    # Wait 5-15 minutes between posts to avoid Reddit spam filters
                    delay = random.randint(300, 900)
                    print(f"Sleeping for {delay} seconds to avoid ban...")
                    time.sleep(delay)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()