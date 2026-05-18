export interface Product {
  id: string;
  name: string;
  shortDescription: string;
  description: string;
  price: number;
  currency: string;
  bestseller: boolean;
  features: string[];
  includedFiles: string[];
  setupInstructions: string[];
}

export const products: Product[] = [
  {
    id: "ai-leadgen-bot",
    name: "AI LeadGen Bot",
    shortDescription: "Automatic client search and proposal outreach for Telegram/WhatsApp.",
    description: "An AI-powered bot that automates finding leads and sending personalized proposals directly on Telegram and WhatsApp.",
    price: 150,
    currency: "USDT",
    bestseller: true,
    features: ["Auto-find clients based on keywords using NLP", "Personalized cold outreach messages tailored by OpenAI", "Seamless Telegram & WhatsApp API integration", "Daily Excel lead reports sent to your inbox", "Anti-ban rotation system with proxy support"],
    includedFiles: ["bot_source_code.py (Main Script)", "requirements.txt (Dependencies)", ".env.example (Config template)", "readme_and_setup_guide.pdf"],
    setupInstructions: ["Extract the provided `.zip` archive to your local machine or VPS.", "Rename `.env.example` to `.env` and fill in your OpenAI and Telegram API keys.", "Install Python dependencies by running `pip install -r requirements.txt`.", "Run the bot with the command `python bot_source_code.py`."]
  },
  {
    id: "ecommerce-content-generator",
    name: "E-commerce Content Generator",
    shortDescription: "Micro-SaaS for mass generation of SEO-optimized product descriptions.",
    description: "Easily generate hundreds of high-converting, SEO-optimized product descriptions using AI. Perfect for large catalogs.",
    price: 99,
    currency: "USDT",
    bestseller: false,
    features: ["Mass generation from CSV data", "Advanced SEO keyword optimization", "Support for 20+ languages natively", "Direct Shopify API push integration"],
    includedFiles: ["generator_app.js (Node.js backend)", "shopify_connector.js", "frontend_dashboard (React App)", "installation_guide.md"],
    setupInstructions: ["Install Node.js on your server.", "Run `npm install` in the project directory.", "Add your OpenAI API key and Shopify Admin token to `.env`.", "Start the dashboard using `npm run start` and upload your CSV."]
  },
  {
    id: "smart-support-agent",
    name: "Smart Support Agent 24/7",
    shortDescription: "Smart bot for frontline customer support in online stores.",
    description: "A 24/7 AI agent that handles common customer inquiries, checks order status, and escalates complex issues to human agents.",
    price: 120,
    currency: "USDT",
    bestseller: true,
    features: ["Sub-second instant response times", "Order tracking API integration (Shopify/WooCommerce)", "Multi-platform deployment (Web widget, TG, WA)", "Custom knowledge base ingestion via PDF/URL"],
    includedFiles: ["support_agent_core.py", "web_widget.js", "docker-compose.yml", "knowledge_base_template.csv"],
    setupInstructions: ["Deploy using the provided `docker-compose.yml` file.", "Upload your store's FAQ and policies to the knowledge base folder.", "Connect your store's API in the dashboard settings.", "Embed `web_widget.js` into your website's footer."]
  },
  {
    id: "docuparse-ai",
    name: "DocuParse AI",
    shortDescription: "Automated extraction of data from PDF invoices to spreadsheets.",
    description: "Save hundreds of hours by automatically extracting line items, totals, and vendor details from PDF invoices directly into Excel or Google Sheets.",
    price: 75,
    currency: "USDT",
    bestseller: false,
    features: ["High accuracy OCR utilizing state-of-the-art vision models", "Complex table extraction and formatting", "Direct export to CSV, Excel, or JSON", "Google Sheets API native integration"],
    includedFiles: ["docuparse_engine.py", "google_sheets_auth.json", "sample_invoices/ (Test Data)", "readme.md"],
    setupInstructions: ["Install required system libraries (Tesseract OCR).", "Install Python requirements via `pip`.", "Place your PDF invoices in the `/input` directory.", "Run `python docuparse_engine.py` and retrieve the parsed `.csv` in the `/output` folder."]
  },
  {
    id: "3d-asset-ai-optimizer",
    name: "3D Asset AI Optimizer",
    shortDescription: "Python script for automating topology creation and optimizing 3D models.",
    description: "Automatically decimate and retopologize high-poly 3D models into game-ready assets with optimized UVs.",
    price: 140,
    currency: "USDT",
    bestseller: false,
    features: ["AI-driven auto-retopology preserving edge loops", "Automatic UV mapping generation", "LOD (Level of Detail) generation (LOD0 to LOD3)", "Batch processing support for entire folders"],
    includedFiles: ["blender_addon.zip", "standalone_script.py", "optimization_presets.json", "tutorial_video.mp4"],
    setupInstructions: ["Install Blender (version 3.0+).", "Go to Edit > Preferences > Add-ons and install `blender_addon.zip`.", "Select your high-poly model in the viewport.", "Click 'Optimize' in the new AI tool panel and wait for processing."]
  },
  {
    id: "social-media-auto-poster",
    name: "Social Media Auto-Poster AI",
    shortDescription: "Content generator and scheduler for social media a month in advance.",
    description: "Generate a full month of engaging posts, including images and captions, and schedule them automatically across multiple platforms.",
    price: 85,
    currency: "USDT",
    bestseller: true,
    features: ["DALL-E 3 Image & GPT-4 Text generation", "Multi-platform scheduling (X, Instagram, LinkedIn)", "Visual content calendar dashboard", "Algorithmic hashtag optimization"],
    includedFiles: ["social_poster.js", "database_schema.sql", "frontend_calendar/", "setup_guide.pdf"],
    setupInstructions: ["Import the `database_schema.sql` into your MySQL/PostgreSQL instance.", "Set up developer API credentials for X, Instagram, and LinkedIn.", "Configure your niche, tone of voice, and brand colors in `config.json`.", "Start the application and let AI generate your first month of content."]
  },
  {
    id: "competitor-price-tracker",
    name: "Competitor Price Tracker",
    shortDescription: "Parser bot that analyzes competitor prices in real-time.",
    description: "Keep your prices competitive by tracking your competitors' pricing across various marketplaces in real-time.",
    price: 50,
    currency: "USDT",
    bestseller: false,
    features: ["Real-time distributed scraping architecture", "Instant Telegram alerts on price drops", "Historical price charts and analytics", "Built-in residential proxy rotation support"],
    includedFiles: ["scraper_bot.py", "proxy_manager.py", "target_urls_template.csv", "readme.md"],
    setupInstructions: ["Add your competitor product URLs to `target_urls_template.csv`.", "Add your proxy list to the configuration file to prevent IP bans.", "Set your Telegram Chat ID for notifications.", "Run the tracking script in the background using `tmux` or `systemd`."]
  },
  {
    id: "cold-email-outreach-ai",
    name: "Cold Email Outreach AI",
    shortDescription: "System for inbox warmup and smart cold B2B emailing.",
    description: "Ensure high deliverability with automated email warmup and send highly personalized cold emails powered by AI.",
    price: 150,
    currency: "USDT",
    bestseller: true,
    features: ["Automated peer-to-peer inbox warmup network", "AI generated personalized first lines for higher reply rates", "Real-time spam word checker and deliverability score", "Complex A/B testing and follow-up flows"],
    includedFiles: ["outreach_platform.zip", "warmup_scripts/", "email_templates.json", "installation_video.mp4"],
    setupInstructions: ["Deploy the `outreach_platform.zip` to your VPS.", "Connect your SMTP/IMAP settings for your sending domains.", "Turn on 'Warmup Mode' for at least 7 days before sending.", "Import your lead CSV, configure your AI prompt, and launch the campaign."]
  },
  {
    id: "community-moderation-bot",
    name: "Community Moderation Bot",
    shortDescription: "AI moderator for Discord/Telegram recognizing toxicity.",
    description: "Maintain a healthy community with an AI bot that detects and automatically acts on toxic behavior, spam, and NSFW content.",
    price: 60,
    currency: "USDT",
    bestseller: false,
    features: ["Deep learning toxicity & sentiment analysis", "Customizable rule enforcement logic", "Auto-kick/ban functionality with appeal system", "Detailed moderation logs and analytics dashboard"],
    includedFiles: ["discord_bot.js", "telegram_bot.py", "models/ (AI weights)", "config.yml"],
    setupInstructions: ["Create a Bot token via Discord Developer Portal or BotFather.", "Edit `config.yml` with your bot token and moderation strictness levels.", "Run the respective bot script (`node discord_bot.js` or `python telegram_bot.py`).", "Invite the bot to your server and grant it Admin permissions."]
  },
  {
    id: "real-estate-listing-ai",
    name: "Real Estate Listing AI",
    shortDescription: "Generator of professional real estate descriptions from photos.",
    description: "Upload photos of a property and let AI generate a compelling, professional listing description ready for Zillow or your website.",
    price: 90,
    currency: "USDT",
    bestseller: false,
    features: ["Advanced computer vision image-to-text analysis", "SEO optimized descriptions tailored for Zillow/Redfin", "Automatic highlighting of premium property features", "Tone customization (Luxury, Cozy, Modern)"],
    includedFiles: ["real_estate_ai.py", "web_interface/", "prompt_templates.json", "readme.md"],
    setupInstructions: ["Start the local web interface via `npm start` in the `web_interface/` folder.", "Run the backend processing engine `python real_estate_ai.py`.", "Open the browser interface and upload property images.", "Select the property type and desired tone, then generate the listing text."]
  }
];
