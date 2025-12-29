# 🚀 New Practical Financial Features

## ✅ Features Added

### 1. Multi-Entity/Subsidiary Support
- **Backend**: Extract entities from CSV (entity, subsidiary, company columns)
- **Frontend**: Entity selector (coming soon)
- **Filtering**: All calculations can be filtered by entity

### 2. KPI Metrics

#### AR Aging Report
- **Endpoint**: `POST /api/kpi/ar-aging`
- **Calculates**: Accounts Receivable aging buckets
  - Current
  - 1-30 days
  - 31-60 days
  - 61-90 days
  - Over 90 days

#### DSO (Days Sales Outstanding)
- **Endpoint**: `POST /api/kpi/dso`
- **Calculates**: Days Sales Outstanding metric
- **Formula**: (Ending AR / Avg Daily Sales) × Period Days

### 3. Foreign Exchange Rates
- **Current Rates**: `GET /api/fx/rates?base_currency=USD`
- **Historical Rates**: `GET /api/fx/rates?base_currency=USD&date=2024-01-15`
- **Currency Conversion**: `POST /api/fx/convert`
- **Source**: exchangerate-api.io (free tier)
- **Date Selection**: Select any date for historical rates

### 4. Revenue Analytics (via Chatbox)

All available through the AI chatbot with suggested questions:

#### Revenue YTD
- **Question**: "What's the revenue YTD?"
- **Calculates**: Year-to-date revenue with monthly breakdown

#### Revenue Variance
- **Question**: "Show me revenue variance compared to previous month"
- **Calculates**: Current month vs previous month variance

#### Trailing 3 Months Rolling Revenue
- **Question**: "Calculate trailing 3 months rolling revenue"
- **Calculates**: Last 90 days revenue total

#### TOP N Revenue Transactions
- **Question**: "Show me TOP 10 revenue transactions"
- **Returns**: Largest revenue transactions

#### Unusual Transactions
- **Question**: "Find unusual transactions posted on weekends"
- **Detects**: Transactions posted on Saturday/Sunday

## 📋 CSV Format Updates

Your CSV can now include an optional `entity` column:

```csv
date,account,amount,type,entity
2024-01-01,Revenue,50000,credit,Subsidiary A
2024-01-02,Revenue,30000,credit,Subsidiary B
```

## 🤖 Enhanced Chatbox

The chatbot now includes:
- ✅ Suggested question chips (click to use)
- ✅ Enhanced AI prompts for revenue analytics
- ✅ Multi-entity awareness
- ✅ FX rate queries support

### Suggested Questions:
1. Revenue YTD
2. Revenue Variance
3. Trailing 3M Revenue
4. TOP N Revenue
5. Unusual Transactions
6. AR Aging
7. DSO Calculation
8. FX Rates

## 🔧 API Endpoints

### KPI Endpoints
- `POST /api/kpi/ar-aging` - AR Aging Report
- `POST /api/kpi/dso` - Days Sales Outstanding
- `POST /api/kpi/revenue-ytd` - Year-to-Date Revenue
- `POST /api/kpi/revenue-variance` - Revenue Variance
- `POST /api/kpi/trailing-3m` - Trailing 3 Months Revenue
- `POST /api/kpi/top-n` - TOP N Revenue Transactions
- `POST /api/kpi/unusual-transactions` - Unusual Transactions

### FX Endpoints
- `GET /api/fx/rates` - Get FX rates (current or historical)
- `POST /api/fx/convert` - Convert currency

### Entity Endpoints
- `POST /api/entities` - Extract entities from transactions

## 📝 Usage Examples

### Via Chatbox:
```
User: "What's the revenue YTD?"
AI: [Calculates and returns YTD revenue with monthly breakdown]

User: "Show me revenue variance compared to previous month"
AI: [Shows current vs previous month variance with percentage]

User: "Find unusual transactions posted on weekends"
AI: [Lists all weekend transactions]
```

### Via API:
```bash
# Get AR Aging
curl -X POST http://localhost:8000/api/kpi/ar-aging \
  -H "Content-Type: application/json" \
  -d '{"transactions": [...], "as_of_date": "2024-12-29"}'

# Get FX Rates
curl http://localhost:8000/api/fx/rates?base_currency=USD&date=2024-01-15
```

## 🎯 Next Steps

1. **Restart Backend** to load new endpoints
2. **Refresh Frontend** to see new chatbox features
3. **Try Suggested Questions** in the chatbox
4. **Upload CSV with entity column** for multi-entity support

## 📚 Documentation

- See API docs: http://localhost:8000/docs
- All endpoints are documented in Swagger UI

