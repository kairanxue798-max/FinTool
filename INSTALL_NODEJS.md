# Installing Node.js on macOS

## Method 1: Official Installer (Recommended - Easiest)

### Step 1: Download Node.js
1. Visit: **https://nodejs.org/**
2. Click the **"LTS"** (Long Term Support) version button
3. This will download a `.pkg` file (e.g., `node-v20.11.0.pkg`)

### Step 2: Install
1. Open the downloaded `.pkg` file
2. Follow the installation wizard
3. Click "Continue" through all steps
4. Enter your password when prompted
5. Click "Install"

### Step 3: Verify Installation
Open a **new terminal** and run:
```bash
node --version
npm --version
```

You should see version numbers like:
```
v20.11.0
10.2.4
```

## Method 2: Using Homebrew (If you have it)

If you have Homebrew installed:
```bash
brew install node
```

## Method 3: Using nvm (Node Version Manager)

For managing multiple Node.js versions:
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal, then:
nvm install --lts
nvm use --lts
```

## After Installation

### 1. Restart Your Terminal
Close and reopen your terminal so it picks up the new PATH.

### 2. Verify Installation
```bash
node --version
npm --version
```

### 3. Start the Frontend
```bash
cd /Users/xuekairan/fin/frontend
npm install
npm run dev
```

### 4. Open the Web App
Go to: **http://localhost:3000**

## Troubleshooting

### "command not found: node"
- Make sure you restarted your terminal
- Check PATH: `echo $PATH`
- Node.js should be in `/usr/local/bin` or `/opt/homebrew/bin`

### "Permission denied"
- Make sure you entered your password during installation
- Try: `sudo npm install -g npm` (if needed)

### Still not working?
- Check if Node.js is installed: `which node`
- Check installation location: `ls -la /usr/local/bin/node`
- Restart your computer if needed

## What You'll Get

After installation, you'll have:
- ✅ **Node.js** - JavaScript runtime
- ✅ **npm** - Package manager (comes with Node.js)
- ✅ Ability to run the frontend development server

## Next Steps After Installation

1. ✅ Verify: `node --version` and `npm --version`
2. ✅ Install frontend dependencies: `cd frontend && npm install`
3. ✅ Start frontend: `npm run dev`
4. ✅ Open browser: `http://localhost:3000`
5. ✅ Upload CSV and use the chatbox!

