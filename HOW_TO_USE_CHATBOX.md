# How to Use the Financial AI Chatbox

## ⚠️ Important: You're Looking at the API Docs, Not the Chatbox!

What you're seeing at `http://localhost:8000/docs` is the **API documentation** (for developers). 

The **actual chatbox interface** is in the **web application** at `http://localhost:3000`.

## 🎯 How to Access the Chatbox

### Step 1: Make Sure Frontend is Running

Open a **new terminal** and run:
```bash
cd /Users/xuekairan/fin/frontend
npm install  # Only needed first time
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

### Step 2: Open the Web Application

Open your web browser and go to:
```
http://localhost:3000
```

### Step 3: Upload Your CSV File

1. On the main page, you'll see a file upload area
2. Click "Select File" or drag and drop your CSV
3. Use the sample file: `example_data/sample_transactions.csv`

### Step 4: Find the Chatbox

After uploading, scroll down past:
- ✅ Financial Statements (Balance Sheet, P&L, Cash Flow tabs)
- ✅ You'll see: **"🤖 Financial AI Assistant"** section
- ✅ This is the chatbox!

## 💬 How to Use the Chatbox

The chatbox looks like a messaging app:

1. **Type your question** in the text box at the bottom
2. **Press Enter** or click the **➤** button to send
3. **See the response** appear in the chat area above

### Example:
```
[Text box at bottom]
"What's the variance in revenue?"
[Click ➤ or press Enter]

[AI Response appears above]
"Based on your financial data..."
```

## 📸 What the Chatbox Looks Like

The chatbox has:
- **Header**: "🤖 Financial AI Assistant" with description
- **Message area**: Shows conversation history (scrollable)
- **Input box**: Text area at the bottom where you type
- **Send button**: ➤ button to send your message
- **User messages**: Appear on the right (blue/purple)
- **AI messages**: Appear on the left (gray) with 🤖 icon

## 🔍 If You Don't See the Chatbox

1. **Make sure you uploaded a CSV file first**
   - The chatbox appears after financial statements are generated
   
2. **Scroll down on the page**
   - It's below the Financial Statements section
   
3. **Check browser console** (F12) for errors
   - Make sure backend is running on port 8000

## 🆚 Difference: API Docs vs Web Interface

| API Documentation (Swagger) | Web Interface (Chatbox) |
|----------------------------|------------------------|
| `http://localhost:8000/docs` | `http://localhost:3000` |
| For developers/testing | For end users |
| JSON input/output | Natural language chat |
| Technical interface | User-friendly interface |
| Manual JSON formatting | Just type and send |

## ✅ Quick Checklist

- [ ] Frontend running on port 3000?
- [ ] Opened http://localhost:3000 in browser?
- [ ] Uploaded CSV file?
- [ ] Scrolled down to see chatbox?
- [ ] Can see text input box at bottom?

## 🎯 Next Steps

1. **Start frontend**: `cd frontend && npm run dev`
2. **Open browser**: Go to `http://localhost:3000`
3. **Upload CSV**: Use sample file or your own
4. **Find chatbox**: Scroll down past financial statements
5. **Start chatting**: Type your question and press Enter!

The chatbox is much easier to use than the API docs - just type naturally! 🚀

