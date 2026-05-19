from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap

def create_glassmorphism_thumbnail(title, subtitle, filename, neon_color, bg_color=(15, 23, 42)): # Dark slate background
    width, height = 1200, 630 # Standard social/cover size
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Background Gradient/Shapes (Subtle Neon Glows)
    glow1 = Image.new('RGBA', (width, height), (0,0,0,0))
    draw_glow = ImageDraw.Draw(glow1)
    # Convert hex to RGB for neon_color if it's hex, assuming it's RGB tuple for now
    draw_glow.ellipse((-200, -200, 600, 600), fill=neon_color + (50,)) # Top left glow
    draw_glow.ellipse((width-500, height-500, width+200, height+200), fill=(139, 92, 246, 50)) # Bottom right purple glow

    # Blur the glows heavily
    glow1 = glow1.filter(ImageFilter.GaussianBlur(radius=100))
    img.paste(glow1, (0,0), glow1)

    # 2. Glass Panel
    glass_x1, glass_y1 = 150, 100
    glass_x2, glass_y2 = width - 150, height - 100

    glass_panel = Image.new('RGBA', (glass_x2 - glass_x1, glass_y2 - glass_y1), (255, 255, 255, 15)) # Semi-transparent white

    # Add a thin subtle border to glass panel
    glass_draw = ImageDraw.Draw(glass_panel)
    glass_draw.rectangle((0, 0, glass_panel.width-1, glass_panel.height-1), outline=(255, 255, 255, 50), width=2)

    img.paste(glass_panel, (glass_x1, glass_y1), glass_panel)

    # 3. Typography
    try:
        # Try to use a nice font if available, fallback to default
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    # Title (wrapped)
    wrapper = textwrap.TextWrapper(width=25)
    wrapped_title = wrapper.wrap(text=title)

    y_text = glass_y1 + 80
    for line in wrapped_title:
        # Center text horizontally
        # Get text bounding box for accurate centering in Pillow 10+
        bbox = draw.textbbox((0,0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_text = (width - text_width) / 2

        # Draw shadow
        draw.text((x_text + 4, y_text + 4), line, fill=(0, 0, 0, 150), font=title_font)
        # Draw text
        draw.text((x_text, y_text), line, fill=(255, 255, 255), font=title_font)

        y_text += title_font.size + 15

    # Subtitle
    y_text += 40
    bbox = draw.textbbox((0,0), subtitle, font=subtitle_font)
    text_width = bbox[2] - bbox[0]
    x_text = (width - text_width) / 2
    draw.text((x_text, y_text), subtitle, fill=(148, 163, 184), font=subtitle_font) # Slate gray

    # 4. Save
    os.makedirs('thumbnails', exist_ok=True)
    img.save(filename, quality=95)

# Generate Thumbnails for all 10 products
products = [
    ("The Ultimate Business\nAutomation Toolkit", "3-in-1 Premium Python Scripts", "thumbnails/01_toolkit.png", (16, 185, 129)), # Emerald
    ("AI Content Blogger Pro", "Automated SEO Blog Generation", "thumbnails/02_blogger.png", (59, 130, 246)), # Blue
    ("Crypto Price Tracker Bot", "Real-time Telegram Alerts", "thumbnails/03_crypto.png", (245, 158, 11)), # Amber
    ("Cold Email Automator", "B2B Outreach with SMTP/Gmail", "thumbnails/04_email.png", (236, 72, 153)), # Pink
    ("Reddit Promo Bot", "AI-Powered Organic Marketing", "thumbnails/05_reddit.png", (255, 69, 0)), # Reddit Orange
    ("Discord Manager Bot", "Automate Server Moderation", "thumbnails/06_discord.png", (88, 101, 242)), # Discord Blurple
    ("Universal Video Downloader", "YT/TikTok/IG MP4 Extraction", "thumbnails/07_video.png", (239, 68, 68)), # Red
    ("Universal Web Scraper", "Extract Any Site Data to CSV", "thumbnails/08_scraper.png", (14, 165, 233)) # Sky Blue
]

for title, subtitle, filename, color in products:
    create_glassmorphism_thumbnail(title, subtitle, filename, color)
    print(f"Generated: {filename}")
