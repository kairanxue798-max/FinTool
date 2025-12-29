# Quick Start Guide

Get up and running with the Financial Statement Generator in 5 minutes!

## Prerequisites Check

- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ npm or yarn installed

## Step 1: Clone and Setup

```bash
# If you haven't already, navigate to the project directory
cd fin

# Run the setup script (macOS/Linux)
./setup.sh

# Or manually:
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit .env to add OPENAI_API_KEY (optional)

# Frontend
cd ../frontend
npm install
```

## Step 2: Start the Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Start the Frontend

Open a new terminal:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

## Step 4: Test the Application

1. Open your browser to `http://localhost:3000`
2. Use the sample CSV file at `example_data/sample_transactions.csv`
3. Drag and drop or click to upload
4. View your generated financial statements!

## CSV Format

Your CSV should have these columns:
- `date`: Transaction date (YYYY-MM-DD)
- `account`: Account name
- `amount`: Transaction amount
- `type`: "debit" or "credit"

See `example_data/sample_transactions.csv` for a sample.

## Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Make sure port 3000 is not in use
- Check that node_modules is installed: `npm install`

### API connection errors
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

## Next Steps

- Add your OpenAI API key to `backend/.env` for full AI features
- Customize account categories in `backend/services/financial_statements.py`
- Deploy to production (see main README.md)

