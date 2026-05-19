import os
import google.generativeai as genai
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    print("Please add it: GEMINI_API_KEY=your_key_here")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_blog_post(keyword):
    """Generates an SEO-optimized blog post using Gemini AI."""
    print(f"\nGenerating content for keyword: '{keyword}'...")

    prompt = f"""
    Write a comprehensive, SEO-optimized blog post about: "{keyword}".
    Requirements:
    - Catchy, click-worthy title (H1)
    - At least 3 subheadings (H2)
    - Engaging introduction and strong conclusion
    - Professional but accessible tone
    - Approximately 500-700 words
    Output in Markdown format.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content for '{keyword}': {e}")
        return None

def save_post(keyword, content):
    """Saves the generated content to a markdown file."""
    # Create output directory if it doesn't exist
    if not os.path.exists("generated_blogs"):
        os.makedirs("generated_blogs")

    # Format filename safely
    filename = keyword.lower().replace(" ", "_").replace("/", "_") + ".md"
    filepath = os.path.join("generated_blogs", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Saved to: {filepath}")

def main():
    print("🤖 Welcome to the AI Content Auto-Blogger!")
    print("Make sure you have your target keywords in 'keywords.txt'.")

    if not os.path.exists("keywords.txt"):
        print("Creating a sample 'keywords.txt' file for you...")
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write("Future of Artificial Intelligence in Business\nHow to Start a Digital Marketing Agency\nTop 10 Remote Work Tools for Teams")
        print("Please edit 'keywords.txt' with your own keywords and run the script again.")
        return

    with open("keywords.txt", "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]

    if not keywords:
        print("Error: keywords.txt is empty.")
        return

    print(f"Found {len(keywords)} keywords to process.\n")

    for idx, keyword in enumerate(keywords):
        content = generate_blog_post(keyword)
        if content:
            save_post(keyword, content)

        # Add a delay between requests to avoid rate limits
        if idx < len(keywords) - 1:
            print("Waiting 10 seconds before next request to respect API limits...")
            time.sleep(10)

    print("\n🎉 All blog posts generated successfully! Check the 'generated_blogs' folder.")

if __name__ == "__main__":
    main()
