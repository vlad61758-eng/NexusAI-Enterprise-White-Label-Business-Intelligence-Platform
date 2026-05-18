#!/bin/bash
# Script to package the Business Automation Toolkit for sale

echo "📦 Packaging The Ultimate Business Automation Toolkit..."

# Remove any old zip
rm -f Ultimate_Business_Automation_Toolkit.zip

# Clean pycache to avoid shipping unnecessary files
find business_automation_toolkit -name "__pycache__" -type d -exec rm -rf {} +
find business_automation_toolkit -name "*.pyc" -delete

# Create the zip archive of the toolkit folder contents
# Exclude tests folder if you don't want to sell it, but here we include everything.
# We will zip the folder itself so it extracts cleanly into one folder.
zip -r Ultimate_Business_Automation_Toolkit.zip business_automation_toolkit/ -x "*/__pycache__/*" -x "*/.pytest_cache/*" -x "*/.git/*"

echo "✅ Packaging complete: Ultimate_Business_Automation_Toolkit.zip is ready for marketplace upload."
