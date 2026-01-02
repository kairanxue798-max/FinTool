# How to Start the Servers

## Quick Start Commands

### Terminal 1 - Start Backend (Python FastAPI)
```bash
cd /Users/xuekairan/fin/backend
source venv/bin/activate
python main.py
```

**Website Link**: http://localhost:8000/docs (API Documentation)

### Terminal 2 - Start Frontend (React)
```bash
cd /Users/xuekairan/fin/frontend
npm install  # First time only
npm run dev
```

**Website Link**: http://localhost:3000 (Main Application)

## Important Notes

1. **You need TWO terminal windows** - one for backend, one for frontend
2. **Keep both terminals open** while testing
3. **Backend must be running** before frontend can work properly

## If Node.js is Not Installed

Install Node.js first:
- Visit: https://nodejs.org/
- Download and install the LTS version
- Then run `npm install` in the frontend directory

## Testing the Application

1. Open browser to: **http://localhost:3000**
2. Upload the sample CSV: `example_data/sample_transactions.csv`
3. View your financial statements!

