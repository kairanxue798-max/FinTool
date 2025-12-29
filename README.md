# FinTool V1 - Financial Statement Generator

A comprehensive financial analysis tool that automatically generates financial statements (Balance Sheet, Profit & Loss, Cash Flow) from CSV uploads. Features multi-entity support, KPI calculations, FX rate integration, and an AI-powered chatbot for financial insights.

## 🌟 Features

### Core Functionality
- **CSV Upload & Processing**: Upload financial transaction data via CSV files
- **Financial Statement Generation**: Automatically generates:
  - Balance Sheet (BS)
  - Profit & Loss Statement (PL)
  - Cash Flow Statement (CF)

### Multi-Entity Support
- Filter transactions by entity/subsidiary
- Compare performance across multiple entities
- Entity-specific financial analysis

### KPI Calculations
- **AR Aging**: Accounts Receivable aging analysis
- **DSO**: Days Sales Outstanding calculation
- **Revenue Analytics**:
  - Revenue YTD (Year-to-Date)
  - Revenue variance compared to previous month
  - Trailing 3 months rolling revenue
  - TOP N revenue transactions
  - Unusual transaction detection (weekend postings)

### FX Rate Integration
- Fetch foreign exchange rates from ATO (Australian Taxation Office) website
- Select date for historical FX rates
- Currency conversion support

### AI-Powered Chatbot
- Ask questions about your financial data
- Subsidiary comparison and analysis
- Revenue analysis by entity
- Profit & Loss insights
- Works without OpenAI API key (fallback analysis available)

### Modern UI/UX
- Interactive dots grid background with dollar icon
- Glassmorphism design elements
- Responsive layout
- Smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fin
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

## 📊 CSV Format

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

## 🎯 Usage

1. **Upload CSV**: Click the upload area and select your CSV file
2. **View Statements**: Financial statements will be generated automatically
3. **Filter Data**: Use the filter panel to filter by entity and date range
4. **Check FX Rates**: Use the FX Rate panel to view exchange rates
5. **Ask Questions**: Use the chatbot to ask questions like:
   - "Which subsidiary has the highest revenue?"
   - "Compare revenue across all entities"
   - "What's the total revenue?"
   - "Show me profit and loss"

## 🏗️ Project Structure

```
fin/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── services/
│       ├── ai_agent.py         # AI chatbot service
│       ├── financial_statements.py  # Statement generation
│       ├── fx_rate_service.py  # FX rate fetching
│       └── kpi_calculator.py   # KPI calculations
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main React component
│   │   └── components/        # React components
│   ├── package.json           # Node dependencies
│   └── vite.config.ts         # Vite configuration
├── example_data/              # Sample CSV files
└── README.md                  # This file
```

## 🔧 API Endpoints

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

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Pandas**: Data manipulation and analysis
- **OpenAI API**: AI-powered analysis (optional)
- **BeautifulSoup**: Web scraping for FX rates

### Frontend
- **React**: UI framework
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **GSAP**: Animation library
- **CSS3**: Modern styling with glassmorphism

## 📝 Version History

### V1.0 (Current)
- Initial release
- CSV upload and processing
- Financial statement generation (BS, PL, CF)
- Multi-entity support
- KPI calculations (AR Aging, DSO, Revenue analytics)
- FX rate integration (ATO)
- AI chatbot with fallback analysis
- Modern UI with interactive background

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- ATO (Australian Taxation Office) for FX rate data
- OpenAI for AI capabilities (optional)

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**FinTool V1** - Making financial analysis easier and more accessible.
