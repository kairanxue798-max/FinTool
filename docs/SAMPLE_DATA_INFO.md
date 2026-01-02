# Comprehensive Sample Data

## 📊 New Comprehensive Sample CSV

**Location**: `/Users/xuekairan/fin/example_data/comprehensive_sample.csv`

### Features:
- ✅ **236 transactions** (much more comprehensive!)
- ✅ **3 Entities**: Subsidiary A, Subsidiary B, Subsidiary C
- ✅ **3 Months of data**: January, February, March 2024
- ✅ **Multiple account types**: Revenue, Expenses, Assets, Liabilities, Equity
- ✅ **Realistic amounts**: Varied transaction amounts
- ✅ **Weekend transactions**: Some transactions on weekends for unusual transaction detection

### Data Breakdown:

#### Subsidiary A
- 90+ transactions
- Higher revenue amounts
- More diverse expense categories
- Multiple revenue streams

#### Subsidiary B
- 75+ transactions
- Moderate revenue
- Standard expense structure

#### Subsidiary C
- 70+ transactions
- Smaller scale operations
- Different revenue patterns

### Perfect for Testing:
- ✅ Multi-entity filtering
- ✅ Date range filtering
- ✅ Revenue analytics (YTD, variance, trailing 3M)
- ✅ AR Aging reports
- ✅ DSO calculations
- ✅ TOP N revenue transactions
- ✅ Unusual transaction detection (weekend postings)
- ✅ Comprehensive financial statements

## 📝 CSV Format

```csv
date,account,amount,type,entity
2024-01-01,Cash,150000,debit,Subsidiary A
2024-01-02,Revenue,75000,credit,Subsidiary A
...
```

### Columns:
- `date`: Transaction date (YYYY-MM-DD)
- `account`: Account name
- `amount`: Transaction amount
- `type`: "debit" or "credit"
- `entity`: Entity/Subsidiary name (optional but recommended)

## 🎯 How to Use

1. **Upload the comprehensive sample**:
   - File: `example_data/comprehensive_sample.csv`
   - 236 transactions ready to test

2. **Test Filters**:
   - Select "Subsidiary A" from entity dropdown
   - Set date range: 2024-01-01 to 2024-01-31
   - See filtered results!

3. **Test All Features**:
   - Revenue YTD (will show all 3 months)
   - Revenue variance (compare months)
   - AR Aging (with multiple AR transactions)
   - DSO calculation
   - TOP N revenue
   - Unusual transactions (weekend postings included)

## 📈 What You'll See

With this comprehensive data, you'll get:
- **Balance Sheet**: Multiple assets, liabilities, equity items
- **Profit & Loss**: Revenue from 3 entities, various expenses
- **Cash Flow**: Operating, investing, financing activities
- **Rich KPI Data**: Enough data for meaningful calculations

Enjoy testing with realistic, comprehensive financial data! 🚀

