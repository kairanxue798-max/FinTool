from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class KPICalculator:
    """
    Calculate various financial KPIs including AR Aging and DSO
    """
    
    def calculate_ar_aging(self, transactions: List[Dict], as_of_date: str = None) -> Dict:
        """
        Calculate Accounts Receivable Aging Report
        """
        if not as_of_date:
            as_of_date = datetime.now().strftime("%Y-%m-%d")
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        as_of = pd.to_datetime(as_of_date)
        
        # Filter AR transactions
        ar_transactions = df[
            df['account'].str.contains('Accounts Receivable|Receivable|AR', case=False, na=False)
        ].copy()
        
        if len(ar_transactions) == 0:
            return {
                "as_of_date": as_of_date,
                "aging_buckets": {
                    "current": 0,
                    "1-30_days": 0,
                    "31-60_days": 0,
                    "61-90_days": 0,
                    "over_90_days": 0
                },
                "total_ar": 0
            }
        
        # Calculate age in days
        ar_transactions['age_days'] = (as_of - ar_transactions['date']).dt.days
        ar_transactions['amount'] = pd.to_numeric(ar_transactions['amount'], errors='coerce')
        
        # Only include debit entries (AR increases with debits)
        ar_debits = ar_transactions[ar_transactions['type'].str.lower() == 'debit'].copy()
        
        # Calculate aging buckets
        current = float(ar_debits[ar_debits['age_days'] <= 0]['amount'].sum())
        days_1_30 = float(ar_debits[(ar_debits['age_days'] > 0) & (ar_debits['age_days'] <= 30)]['amount'].sum())
        days_31_60 = float(ar_debits[(ar_debits['age_days'] > 30) & (ar_debits['age_days'] <= 60)]['amount'].sum())
        days_61_90 = float(ar_debits[(ar_debits['age_days'] > 60) & (ar_debits['age_days'] <= 90)]['amount'].sum())
        over_90 = float(ar_debits[ar_debits['age_days'] > 90]['amount'].sum())
        
        total_ar = current + days_1_30 + days_31_60 + days_61_90 + over_90
        
        return {
            "as_of_date": as_of_date,
            "aging_buckets": {
                "current": current,
                "1-30_days": days_1_30,
                "31-60_days": days_31_60,
                "61-90_days": days_61_90,
                "over_90_days": over_90
            },
            "total_ar": total_ar,
            "details": ar_debits.to_dict('records') if len(ar_debits) > 0 else []
        }
    
    def calculate_dso(self, transactions: List[Dict], period_days: int = 30) -> Dict:
        """
        Calculate Days Sales Outstanding (DSO)
        DSO = (Accounts Receivable / Total Credit Sales) * Number of Days
        """
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Get end date and start date
        end_date = df['date'].max()
        start_date = end_date - timedelta(days=period_days)
        
        # Calculate Accounts Receivable (ending balance)
        ar_transactions = df[
            (df['account'].str.contains('Accounts Receivable|Receivable|AR', case=False, na=False)) &
            (df['date'] <= end_date)
        ]
        ar_debits = ar_transactions[ar_transactions['type'].str.lower() == 'debit']['amount'].sum()
        ar_credits = ar_transactions[ar_transactions['type'].str.lower() == 'credit']['amount'].sum()
        ending_ar = float(ar_debits - ar_credits)
        
        # Calculate credit sales (revenue) for the period
        revenue_transactions = df[
            (df['account'].str.contains('Revenue|Sales|Income', case=False, na=False)) &
            (df['date'] >= start_date) &
            (df['date'] <= end_date) &
            (df['type'].str.lower() == 'credit')
        ]
        total_revenue = float(revenue_transactions['amount'].sum())
        
        # Calculate DSO
        if total_revenue > 0:
            avg_daily_sales = total_revenue / period_days
            dso = float(ending_ar / avg_daily_sales) if avg_daily_sales > 0 else 0
        else:
            dso = 0
            avg_daily_sales = 0
        
        return {
            "period_days": period_days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "ending_ar": ending_ar,
            "total_revenue": total_revenue,
            "avg_daily_sales": avg_daily_sales,
            "dso": round(dso, 2)
        }
    
    def calculate_revenue_ytd(self, transactions: List[Dict], entity: str = None) -> Dict:
        """Calculate Year-to-Date Revenue"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        if entity:
            df = df[df.get('entity', '') == entity]
        
        current_year = datetime.now().year
        ytd_transactions = df[
            (df['date'].dt.year == current_year) &
            (df['account'].str.contains('Revenue|Sales|Income', case=False, na=False)) &
            (df['type'].str.lower() == 'credit')
        ]
        
        total_ytd = float(ytd_transactions['amount'].sum())
        
        # Monthly breakdown
        monthly_revenue = {}
        for month in range(1, 13):
            month_data = ytd_transactions[ytd_transactions['date'].dt.month == month]
            monthly_revenue[datetime(current_year, month, 1).strftime("%B")] = float(month_data['amount'].sum())
        
        return {
            "year": current_year,
            "ytd_total": total_ytd,
            "monthly_breakdown": monthly_revenue,
            "entity": entity
        }
    
    def calculate_revenue_variance(self, transactions: List[Dict], entity: str = None) -> Dict:
        """Calculate revenue variance compared to previous month"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        if entity:
            df = df[df.get('entity', '') == entity]
        
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        
        # Current month revenue
        current_month_rev = df[
            (df['date'].dt.month == current_month) &
            (df['date'].dt.year == current_year) &
            (df['account'].str.contains('Revenue|Sales|Income', case=False, na=False)) &
            (df['type'].str.lower() == 'credit')
        ]['amount'].sum()
        
        # Previous month revenue
        prev_month = current_month - 1
        prev_year = current_year
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        
        prev_month_rev = df[
            (df['date'].dt.month == prev_month) &
            (df['date'].dt.year == prev_year) &
            (df['account'].str.contains('Revenue|Sales|Income', case=False, na=False)) &
            (df['type'].str.lower() == 'credit')
        ]['amount'].sum()
        
        variance = float(current_month_rev - prev_month_rev)
        variance_pct = float((variance / prev_month_rev * 100) if prev_month_rev > 0 else 0)
        
        return {
            "current_month": f"{current_year}-{current_month:02d}",
            "previous_month": f"{prev_year}-{prev_month:02d}",
            "current_revenue": float(current_month_rev),
            "previous_revenue": float(prev_month_rev),
            "variance": variance,
            "variance_percentage": round(variance_pct, 2),
            "entity": entity
        }
    
    def calculate_trailing_3m_revenue(self, transactions: List[Dict], entity: str = None) -> Dict:
        """Calculate trailing 3 months rolling revenue"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        if entity:
            df = df[df.get('entity', '') == entity]
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        trailing_rev = df[
            (df['date'] >= start_date) &
            (df['date'] <= end_date) &
            (df['account'].str.contains('Revenue|Sales|Income', case=False, na=False)) &
            (df['type'].str.lower() == 'credit')
        ]['amount'].sum()
        
        return {
            "period": "Trailing 3 Months",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "total_revenue": float(trailing_rev),
            "entity": entity
        }
    
    def find_top_n_revenue(self, transactions: List[Dict], n: int = 10, entity: str = None) -> Dict:
        """Find TOP N revenue transactions"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        if entity:
            df = df[df.get('entity', '') == entity]
        
        revenue_transactions = df[
            (df['account'].str.contains('Revenue|Sales|Income', case=False, na=False)) &
            (df['type'].str.lower() == 'credit')
        ].copy()
        
        top_n = revenue_transactions.nlargest(n, 'amount')[['date', 'account', 'amount']].to_dict('records')
        
        return {
            "top_n": n,
            "transactions": [
                {
                    "date": row['date'].strftime("%Y-%m-%d") if isinstance(row['date'], pd.Timestamp) else str(row['date']),
                    "account": row['account'],
                    "amount": float(row['amount'])
                }
                for row in top_n
            ],
            "entity": entity
        }
    
    def find_unusual_transactions(self, transactions: List[Dict], entity: str = None) -> Dict:
        """Find transactions posted on weekends"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        if entity:
            df = df[df.get('entity', '') == entity]
        
        # Find weekend transactions (Saturday = 5, Sunday = 6)
        df['day_of_week'] = df['date'].dt.dayofweek
        weekend_transactions = df[df['day_of_week'].isin([5, 6])].copy()
        
        unusual = weekend_transactions[['date', 'account', 'amount', 'type']].to_dict('records')
        
        return {
            "unusual_type": "Weekend Postings",
            "count": len(unusual),
            "transactions": [
                {
                    "date": row['date'].strftime("%Y-%m-%d") if isinstance(row['date'], pd.Timestamp) else str(row['date']),
                    "day": row['date'].strftime("%A") if isinstance(row['date'], pd.Timestamp) else "",
                    "account": row['account'],
                    "amount": float(row['amount']),
                    "type": row['type']
                }
                for row in unusual
            ],
            "entity": entity
        }

