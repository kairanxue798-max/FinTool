# How to Push FinTool V1 to GitHub - Step by Step

## Where to Run the Commands

You need to run the commands in a **Terminal** (command line interface). Here's how to open it:

### On macOS (Your System):

**Method 1: Using Spotlight (Easiest)**
1. Press `Cmd + Space` (Command key + Spacebar)
2. Type: `Terminal`
3. Press `Enter`
4. Terminal window will open

**Method 2: Using Finder**
1. Open Finder
2. Go to Applications → Utilities
3. Double-click on "Terminal"

**Method 3: Using Cursor/VS Code**
1. In Cursor, go to: Terminal → New Terminal
2. Or press: `Ctrl + ~` (Control + Tilde key)

## Step-by-Step Instructions

### Step 1: Open Terminal
Use one of the methods above to open Terminal.

### Step 2: Navigate to Your Project
In the Terminal, type:
```bash
cd /Users/xuekairan/fin
```
Press `Enter`

### Step 3: Verify You're in the Right Place
Type:
```bash
pwd
```
Press `Enter` - It should show: `/Users/xuekairan/fin`

### Step 4: Check Git Status (Optional)
Type:
```bash
git status
```
Press `Enter` - You should see "On branch main" and "nothing to commit"

### Step 5: Create GitHub Repository First
**Before running push commands**, you need to create the repository on GitHub:

1. Open your web browser
2. Go to: https://github.com/new
3. Sign in to GitHub (or create an account if needed)
4. Fill in:
   - Repository name: `FinTool` (or your preferred name)
   - Description: "Financial Statement Generator - FinTool V1"
   - Choose Public or Private
   - **IMPORTANT**: Do NOT check "Add a README file" (we already have one)
   - **IMPORTANT**: Do NOT add .gitignore or license (we have these)
5. Click the green "Create repository" button

### Step 6: Push Your Code
After creating the repository, GitHub will show you a page with commands. 

**In your Terminal**, run these commands one by one (replace `YOUR_USERNAME` with your actual GitHub username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/FinTool.git
```
Press `Enter`

```bash
git branch -M main
```
Press `Enter`

```bash
git push -u origin main
```
Press `Enter` - This will ask for your GitHub username and password/token

```bash
git push origin v1.0
```
Press `Enter` - This pushes the V1.0 tag

## Example with Real Username

If your GitHub username is `johnsmith`, the commands would be:

```bash
git remote add origin https://github.com/johnsmith/FinTool.git
git branch -M main
git push -u origin main
git push origin v1.0
```

## Authentication

When you run `git push`, you'll be asked for:
- **Username**: Your GitHub username
- **Password**: You'll need a **Personal Access Token** (not your GitHub password)

### How to Create Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "FinTool V1"
4. Select scopes: Check `repo` (this gives full repository access)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. When Terminal asks for password, paste the token instead

## Troubleshooting

### "Command not found: git"
- Git might not be installed. Install it from: https://git-scm.com/download/mac

### "remote origin already exists"
- Run: `git remote remove origin`
- Then run the `git remote add origin` command again

### "Permission denied"
- Make sure you're using the correct GitHub username
- Use Personal Access Token instead of password

### "Repository not found"
- Make sure you created the repository on GitHub first
- Check that the repository name matches exactly

## Verify It Worked

1. Go to: https://github.com/YOUR_USERNAME/FinTool
2. You should see all your files
3. Click "Releases" on the right side
4. You should see "v1.0" tag

## Quick Reference

**Terminal Shortcuts:**
- `Cmd + T` - New Terminal tab
- `Cmd + K` - Clear Terminal screen
- `Cmd + C` - Cancel current command
- `Up Arrow` - Previous command
- `Tab` - Auto-complete file/folder names

**Common Commands:**
- `pwd` - Show current directory
- `ls` - List files in current directory
- `cd folder_name` - Go into a folder
- `cd ..` - Go up one folder
- `cd ~` - Go to home directory

