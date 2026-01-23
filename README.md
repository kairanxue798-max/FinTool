# FinTool - Financial Statement Generator

A comprehensive financial analysis tool that automatically generates financial statements (Balance Sheet, Profit & Loss, Cash Flow) from CSV uploads. Features multi-entity support, KPI calculations, FX rate integration, and an AI-powered chatbot for financial insights.

## Key Features

- **Automated Financial Statements**: Upload CSV files to generate Financial Statements
- **File Summary Panel**: Automatic display of key metadata (total transactions, unique accounts, date range)
- **Multi-Entity Support**: Filter and compare performance across subsidiaries and entities
- **KPI Analytics**: AR Aging, DSO, Revenue YTD, variance analysis, trailing metrics, and unusual transaction detection
- **FX Rate Integration**: Fetch foreign exchange rates from ATO (Australian Taxation Office) with historical data support
- **AI-Powered Chatbot**: Ask questions about your financial data with categorized suggested questions
- **Modern UI/UX**: Professional design system with responsive layout and smooth animations

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation and analysis
- **OpenAI API** - AI-powered analysis (optional, fallback available)
- **BeautifulSoup** - Web scraping for FX rates

### Frontend
- **React** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **GSAP** - Animation library
- **CSS3** - Modern styling with Corporate Trust design system

## Project Structure

```
fin/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   └── services/
│       ├── ai_agent.py         # AI chatbot service
│       ├── financial_statements.py  # Statement generation logic
│       ├── fx_rate_service.py  # FX rate fetching service
│       └── kpi_calculator.py   # KPI calculations
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main React component
│   │   ├── components/        # React components
│   │   └── index.css          # Global styles
│   ├── package.json           # Node dependencies
│   └── vite.config.ts         # Vite configuration
├── example_data/              # Sample CSV files
├── docs/                      # Documentation and development notes
└── README.md                  # This file
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kairanxue798-max/FinTool.git
   cd FinTool
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables (Optional)**
   Create `backend/.env` file for OpenAI API key (optional):
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Note: The tool works without OpenAI API key using fallback analysis.

### Running the Application

1. **Start Backend Server**
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```
   Backend will run on `http://localhost:8000`

2. **Start Frontend Server** (in a new terminal)
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

3. **Access the Application**
   Open your browser and navigate to: `http://localhost:3000`

##  How to Use

### 1. Upload Financial Data
- Click the upload area or drag and drop your CSV file
- The file summary panel will automatically display key metadata

### 2. Generate Financial Statements
- After upload, financial statements are generated automatically:
  - **Balance Sheet**: Assets, Liabilities, and Equity
  - **Profit & Loss**: Revenue, Expenses, and Net Income
  - **Cash Flow**: Operating, Investing, and Financing activities

### 3. Filter and Analyze
- Use the filter panel to filter by entity/subsidiary and date range
- View FX rates using the FX Rate panel
- Statements automatically update based on filters

### 4. Ask Questions and Get Insights
- Use the AI chatbot to ask questions about your financial data
- Click suggested questions from categorized groups:
  - **Performance**: Revenue YTD, Variance, Trailing 3M, TOP N Revenue
  - **Risk and Unusual Transaction**: Unusual transaction detection
  - **Cash and Working Capital**: AR Aging, DSO, FX Rates
- Or type your own questions like:
  - "Which subsidiary has the highest revenue?"
  - "Compare revenue across all entities"
  - "What's the total revenue?"
  - "Show me profit and loss"

##  CSV Format

Your CSV file should include the following columns:
- `date`: Transaction date (YYYY-MM-DD)
- `account`: Account name (e.g., "Revenue", "Expenses", "Cash")
- `amount`: Transaction amount (numeric)
- `type`: Transaction type ("credit" or "debit")
- `entity` or `subsidiary`: Entity/subsidiary name (optional but recommended)

### Example CSV
```csv
date,account,amount,type,entity
2024-01-15,Revenue,5000,credit,Subsidiary A
2024-01-16,Operating Expenses,2000,debit,Subsidiary A
2024-01-17,Revenue,3000,credit,Subsidiary B
```

Sample data files are available in `example_data/` directory.

##  API Endpoints

### Financial Statements
- `POST /api/upload-csv` - Upload CSV file
- `POST /api/generate-statements` - Generate financial statements

### KPI Endpoints
- `POST /api/kpi/ar-aging` - AR Aging report
- `POST /api/kpi/dso` - Days Sales Outstanding
- `POST /api/kpi/revenue-ytd` - Revenue YTD
- `POST /api/kpi/revenue-variance` - Revenue variance
- `POST /api/kpi/trailing-3m` - Trailing 3 months revenue
- `POST /api/kpi/top-n` - TOP N revenue transactions
- `POST /api/kpi/unusual-transactions` - Unusual transactions

### FX Rate Endpoints
- `GET /api/fx/ato-rates?year=YYYY&month=MM` - Get ATO FX rates
- `POST /api/fx/convert` - Currency conversion

### AI Chat
- `POST /api/ai/chat` - Chat with AI assistant

##  Notes

This repository contains the latest version of FinTool. Prior iterations are preserved in git history but are not maintained separately.

##  Screenshots

_Coming soon: Screenshots of the application interface_

##  Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- ATO (Australian Taxation Office) for FX rate data
- OpenAI for AI capabilities (optional)

##  Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**FinTool** - Making financial analysis easier and more accessible.
