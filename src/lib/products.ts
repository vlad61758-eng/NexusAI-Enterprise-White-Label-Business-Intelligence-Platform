export interface Product {
  id: string;
  name: string;
  shortDescription: string;
  description: string;
  price: number;
  currency: string;
  bestseller: boolean;
  features: string[];
  setupInstructions: string;
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
    features: ["Auto-find clients based on keywords", "Personalized cold outreach messages", "Telegram & WhatsApp integration", "Daily lead reports"],
    setupInstructions: "1. Unzip the file. 2. Edit `.env` with your API keys. 3. Run `npm run start`."
  },
  {
    id: "ecommerce-content-generator",
    name: "E-commerce Content Generator",
    shortDescription: "Micro-SaaS for mass generation of SEO-optimized product descriptions.",
    description: "Easily generate hundreds of high-converting, SEO-optimized product descriptions using AI. Perfect for large catalogs.",
    price: 99,
    currency: "USDT",
    bestseller: false,
    features: ["Mass generation from CSV", "SEO keyword optimization", "Multiple language support", "Direct Shopify integration"],
    setupInstructions: "1. Access the web portal. 2. Input your OpenAI API key. 3. Upload your product list."
  },
  {
    id: "smart-support-agent",
    name: "Smart Support Agent 24/7",
    shortDescription: "Smart bot for frontline customer support in online stores.",
    description: "A 24/7 AI agent that handles common customer inquiries, checks order status, and escalates complex issues to human agents.",
    price: 120,
    currency: "USDT",
    bestseller: true,
    features: ["Instant response times", "Order tracking integration", "Multi-platform (Web, TG, WA)", "Custom knowledge base ingestion"],
    setupInstructions: "1. Deploy to Vercel/Heroku. 2. Connect your store's API. 3. Add the widget script to your site."
  },
  {
    id: "docuparse-ai",
    name: "DocuParse AI",
    shortDescription: "Automated extraction of data from PDF invoices to spreadsheets.",
    description: "Save hundreds of hours by automatically extracting line items, totals, and vendor details from PDF invoices directly into Excel or Google Sheets.",
    price: 75,
    currency: "USDT",
    bestseller: false,
    features: ["High accuracy OCR", "Table extraction", "Export to CSV/Excel", "Google Sheets API integration"],
    setupInstructions: "1. Run the Python script. 2. Point it to your folder of PDFs. 3. Get the parsed CSV."
  },
  {
    id: "3d-asset-ai-optimizer",
    name: "3D Asset AI Optimizer",
    shortDescription: "Python script for automating topology creation and optimizing 3D models.",
    description: "Automatically decimate and retopologize high-poly 3D models into game-ready assets with optimized UVs.",
    price: 140,
    currency: "USDT",
    bestseller: false,
    features: ["Auto-retopology", "UV mapping generation", "LOD generation", "Batch processing support"],
    setupInstructions: "1. Install Blender and Python. 2. Run the script via Blender's CLI. 3. Specify input/output directories."
  },
  {
    id: "social-media-auto-poster",
    name: "Social Media Auto-Poster AI",
    shortDescription: "Content generator and scheduler for social media a month in advance.",
    description: "Generate a full month of engaging posts, including images and captions, and schedule them automatically across multiple platforms.",
    price: 85,
    currency: "USDT",
    bestseller: true,
    features: ["Image & Text generation", "Multi-platform scheduling (X, IG, LinkedIn)", "Content calendar view", "Hashtag optimization"],
    setupInstructions: "1. Set up social media API credentials. 2. Define your niche and tone. 3. Let AI generate and schedule."
  },
  {
    id: "competitor-price-tracker",
    name: "Competitor Price Tracker",
    shortDescription: "Parser bot that analyzes competitor prices in real-time.",
    description: "Keep your prices competitive by tracking your competitors' pricing across various marketplaces in real-time.",
    price: 50,
    currency: "USDT",
    bestseller: false,
    features: ["Real-time scraping", "Alerts on price drops", "Historical price charts", "Proxy support"],
    setupInstructions: "1. Configure target URLs in `config.json`. 2. Add proxies. 3. Run the tracking script."
  },
  {
    id: "cold-email-outreach-ai",
    name: "Cold Email Outreach AI",
    shortDescription: "System for inbox warmup and smart cold B2B emailing.",
    description: "Ensure high deliverability with automated email warmup and send highly personalized cold emails powered by AI.",
    price: 150,
    currency: "USDT",
    bestseller: true,
    features: ["Automated inbox warmup", "AI personalized first lines", "Spam word checker", "A/B testing flows"],
    setupInstructions: "1. Connect your SMTP/IMAP. 2. Import your lead list. 3. Launch the campaign."
  },
  {
    id: "community-moderation-bot",
    name: "Community Moderation Bot",
    shortDescription: "AI moderator for Discord/Telegram recognizing toxicity.",
    description: "Maintain a healthy community with an AI bot that detects and automatically acts on toxic behavior, spam, and NSFW content.",
    price: 60,
    currency: "USDT",
    bestseller: false,
    features: ["Toxicity & sentiment analysis", "Custom rule enforcement", "Auto-kick/ban functionality", "Detailed moderation logs"],
    setupInstructions: "1. Invite the bot to your server. 2. Set moderation strictness in the dashboard. 3. Enable."
  },
  {
    id: "real-estate-listing-ai",
    name: "Real Estate Listing AI",
    shortDescription: "Generator of professional real estate descriptions from photos.",
    description: "Upload photos of a property and let AI generate a compelling, professional listing description ready for Zillow or your website.",
    price: 90,
    currency: "USDT",
    bestseller: false,
    features: ["Image-to-text analysis", "SEO optimized descriptions", "Highlighting key property features", "Tone customization"],
    setupInstructions: "1. Upload property images. 2. Select property type. 3. Copy the generated text."
  }
];
