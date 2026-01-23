# Screenshots Guide

This directory contains screenshots of the FinTool application for display on GitHub.

## How to Add Screenshots

### Step 1: Take Screenshots

1. **Main Dashboard** (`main-dashboard.png`)
   - Open `http://localhost:3000/` in your browser
   - Take a full-page screenshot showing the main upload interface
   - On macOS: `Cmd + Shift + 4`, then press `Space` to capture the window

2. **Financial Statements** (`financial-statements.png`)
   - Upload a CSV file and generate statements
   - Capture the Balance Sheet, Profit & Loss, and Cash Flow sections
   - Make sure the statements are visible and readable

3. **FX Rate Panel** (`fx-rate-panel.png`)
   - Navigate to the FX Rate panel
   - Select a month (e.g., 2026-01)
   - Capture the FX rates table showing currency codes and rates

4. **AI Chatbot** (`ai-chatbot.png`)
   - Open the AI chatbot panel
   - Show a conversation with suggested questions and responses
   - Capture the chat interface with example Q&A

### Step 2: Save Screenshots

Save all screenshots in this directory (`screenshots/`) with these exact filenames:
- `main-dashboard.png`
- `financial-statements.png`
- `fx-rate-panel.png`
- `ai-chatbot.png`

### Step 3: Commit and Push

```bash
# Add screenshots
git add screenshots/*.png

# Commit
git commit -m "docs: Add application screenshots"

# Push to GitHub
git push origin main
```

The screenshots will automatically appear on the GitHub repository homepage in the README.md file.

## Screenshot Tips

- **Resolution**: Use high-resolution screenshots (at least 1920x1080 or higher)
- **Format**: PNG format recommended for best quality
- **Browser**: Use Chrome or Safari for consistent appearance
- **Window**: Capture the entire browser window, not just the viewport
- **Content**: Make sure important UI elements are visible and not cut off

