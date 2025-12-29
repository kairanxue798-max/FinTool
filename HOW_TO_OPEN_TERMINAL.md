# How to Open a New Terminal on macOS

## Method 1: Using Spotlight (Easiest)

1. **Press** `Command (⌘) + Space` to open Spotlight
2. **Type**: `Terminal`
3. **Press** `Enter` or click on "Terminal"
4. A new terminal window will open!

## Method 2: Using Finder

1. **Open Finder**
2. Go to **Applications** → **Utilities**
3. **Double-click** on **Terminal**
4. A new terminal window will open!

## Method 3: Using Dock

1. Look at the bottom of your screen (Dock)
2. If Terminal is there, **click** it
3. If not, you can add it:
   - Open Terminal using Method 1 or 2
   - Right-click Terminal icon in Dock
   - Choose "Options" → "Keep in Dock"

## Method 4: Keyboard Shortcut (If configured)

Some Macs have Terminal in the Dock - just click it!

## What You'll See

When Terminal opens, you'll see something like:
```
Last login: Mon Dec 29 16:00:00 on ttys000
xuekairan@MacBook-Pro ~ %
```

This is your command prompt - you can type commands here!

## After Opening Terminal

Once you have a new terminal open, run these commands:

### 1. Check if Node.js is installed:
```bash
node --version
```

If you see a version number (like `v20.11.0`), Node.js is installed! ✅

If you see `command not found`, Node.js is not installed yet. ❌

### 2. If Node.js is installed, verify npm:
```bash
npm --version
```

### 3. Then start the frontend:
```bash
cd /Users/xuekairan/fin/frontend
npm install
npm run dev
```

## Quick Tips

- **New Terminal Window**: `Command (⌘) + N` (when Terminal is open)
- **New Terminal Tab**: `Command (⌘) + T` (when Terminal is open)
- **Close Terminal**: `Command (⌘) + Q` or click the red X button

## Visual Guide

```
┌─────────────────────────────────────┐
│  Terminal                           │
├─────────────────────────────────────┤
│  xuekairan@MacBook-Pro ~ %          │
│  [You type commands here]           │
│                                     │
└─────────────────────────────────────┘
```

## Need Help?

If you can't find Terminal:
- Try Spotlight: `⌘ + Space`, type "Terminal"
- Or check: Applications → Utilities → Terminal

