# Testing Guide

## Website Links

Once both servers are running:
- **Frontend (Website)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## Step-by-Step Testing Instructions

### 1. Setup (First Time Only)

#### Backend Setup:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Frontend Setup:
```bash
cd frontend
npm install
```

### 2. Start Backend Server

Open Terminal 1:
```bash
cd /Users/xuekairan/fin/backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!**

### 3. Start Frontend Server

Open Terminal 2 (new terminal window):
```bash
cd /Users/xuekairan/fin/frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

**Keep this terminal open too!**

### 4. Open the Website

Open your web browser and go to:
```
http://localhost:3000
```

### 5. Test the Application

1. **Upload CSV File**:
   - Click "Select File" or drag and drop
   - Use the sample file: `example_data/sample_transactions.csv`
   - Or create your own CSV with columns: `date`, `account`, `amount`, `type`

2. **View Financial Statements**:
   - After upload, you'll see three tabs:
     - **Balance Sheet**: Shows assets, liabilities, and equity
     - **Profit & Loss**: Shows revenue, expenses, and net income
     - **Cash Flow**: Shows operating, investing, and financing activities

3. **Test AI Features**:
   - Click "Run Variance Analysis" to compare periods
   - Set KPI targets and click "Run KPI Analysis"
   - Note: Full AI features require OpenAI API key in `backend/.env`

### 6. Test API Directly (Optional)

You can also test the API directly:

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Upload CSV (example)
curl -X POST http://localhost:8000/api/upload-csv \
  -F "file=@example_data/sample_transactions.csv"
```

Or visit the interactive API docs:
```
http://localhost:8000/docs
```

## Sample CSV File

A sample CSV file is provided at:
```
example_data/sample_transactions.csv
```

Format:
```csv
date,account,amount,type
2024-01-01,Cash,100000,debit
2024-01-02,Revenue,50000,credit
```

## Troubleshooting

### Port Already in Use
If port 8000 or 3000 is already in use:
- Backend: Change port in `backend/main.py` (line with `uvicorn.run`)
- Frontend: Change port in `frontend/vite.config.ts`

### Backend Not Starting
```bash
# Check if dependencies are installed
cd backend
source venv/bin/activate
pip list | grep fastapi

# Reinstall if needed
pip install -r requirements.txt
```

### Frontend Not Starting
```bash
# Check if node_modules exists
cd frontend
ls node_modules

# Reinstall if needed
npm install
```

### CORS Errors
- Make sure backend is running on port 8000
- Check `backend/main.py` CORS settings

### Can't Connect to API
- Verify backend is running: `curl http://localhost:8000/api/health`
- Check browser console for errors (F12)
- Ensure both servers are running

## Quick Test Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Can access http://localhost:3000 in browser
- [ ] Can upload CSV file
- [ ] Financial statements are generated
- [ ] Can switch between BS, PL, CF tabs
- [ ] AI analysis buttons work (may need API key)

## Next Steps After Testing

1. Add OpenAI API key for full AI features
2. Customize account categories for your business
3. Deploy to production
4. Set up GitHub repository

