from typing import Dict, List
from datetime import datetime
import pandas as pd
import numpy as np


class FinancialStatementGenerator:
    """
    Generates financial statements from transaction data
    """
    
    def __init__(self):
        self.asset_accounts = ['Cash', 'Accounts Receivable', 'Inventory', 'Property', 'Equipment', 'Investments']
        self.liability_accounts = ['Accounts Payable', 'Loans', 'Debt', 'Accrued Expenses']
        self.equity_accounts = ['Capital', 'Retained Earnings', 'Equity']
        self.revenue_accounts = ['Revenue', 'Sales', 'Income', 'Interest Income']
        self.expense_accounts = ['Cost of Goods Sold', 'Operating Expenses', 'Salaries', 'Rent', 'Utilities', 'Marketing', 'Depreciation']
    
    def generate_balance_sheet(self, transactions: List[Dict]) -> Dict:
        """
        Generate Balance Sheet from transactions
        """
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Calculate assets
        assets = {}
        total_assets = 0
        for account in self.asset_accounts:
            asset_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(asset_transactions) > 0:
                # Assets increase with debits, decrease with credits
                asset_amount = float(asset_transactions[
                    asset_transactions['type'].str.lower() == 'debit'
                ]['amount'].sum() - asset_transactions[
                    asset_transactions['type'].str.lower() == 'credit'
                ]['amount'].sum())
                if asset_amount > 0:
                    assets[account] = asset_amount
                    total_assets += asset_amount
        
        # Calculate liabilities
        liabilities = {}
        total_liabilities = 0
        for account in self.liability_accounts:
            liability_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(liability_transactions) > 0:
                # Liabilities increase with credits, decrease with debits
                liability_amount = float(liability_transactions[
                    liability_transactions['type'].str.lower() == 'credit'
                ]['amount'].sum() - liability_transactions[
                    liability_transactions['type'].str.lower() == 'debit'
                ]['amount'].sum())
                if liability_amount > 0:
                    liabilities[account] = liability_amount
                    total_liabilities += liability_amount
        
        # Calculate equity
        equity = {}
        total_equity = 0
        for account in self.equity_accounts:
            equity_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(equity_transactions) > 0:
                equity_amount = float(equity_transactions[
                    equity_transactions['type'].str.lower() == 'credit'
                ]['amount'].sum() - equity_transactions[
                    equity_transactions['type'].str.lower() == 'debit'
                ]['amount'].sum())
                if equity_amount > 0:
                    equity[account] = equity_amount
                    total_equity += equity_amount
        
        # Get net income from P&L
        net_income = self._calculate_net_income(df)
        if 'Retained Earnings' not in equity:
            equity['Retained Earnings'] = 0
        equity['Retained Earnings'] += net_income
        total_equity += net_income
        
        return {
            "as_of_date": datetime.now().strftime("%Y-%m-%d"),
            "assets": {
                "items": assets,
                "total": float(total_assets)
            },
            "liabilities": {
                "items": liabilities,
                "total": float(total_liabilities)
            },
            "equity": {
                "items": equity,
                "total": float(total_equity)
            },
            "total_liabilities_and_equity": float(total_liabilities + total_equity)
        }
    
    def generate_profit_loss(self, transactions: List[Dict]) -> Dict:
        """
        Generate Profit & Loss statement from transactions
        """
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Calculate revenue
        revenue = {}
        total_revenue = 0
        for account in self.revenue_accounts:
            revenue_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(revenue_transactions) > 0:
                revenue_amount = float(revenue_transactions[
                    revenue_transactions['type'].str.lower() == 'credit'
                ]['amount'].sum())
                if revenue_amount > 0:
                    revenue[account] = revenue_amount
                    total_revenue += revenue_amount
        
        # Calculate expenses
        expenses = {}
        total_expenses = 0
        for account in self.expense_accounts:
            expense_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(expense_transactions) > 0:
                expense_amount = float(expense_transactions[
                    expense_transactions['type'].str.lower() == 'debit'
                ]['amount'].sum())
                if expense_amount > 0:
                    expenses[account] = expense_amount
                    total_expenses += expense_amount
        
        net_income = total_revenue - total_expenses
        
        return {
            "period": self._get_period(df),
            "revenue": {
                "items": revenue,
                "total": float(total_revenue)
            },
            "expenses": {
                "items": expenses,
                "total": float(total_expenses)
            },
            "net_income": float(net_income)
        }
    
    def generate_cash_flow(self, transactions: List[Dict]) -> Dict:
        """
        Generate Cash Flow statement from transactions
        """
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Operating activities (revenue and operating expenses)
        operating_cash = df[
            (df['account'].str.contains('Cash', case=False, na=False)) &
            (df['account'].str.contains('Revenue|Sales|Operating|Expenses', case=False, na=False))
        ]
        operating_inflow = float(operating_cash[
            operating_cash['type'].str.lower() == 'debit'
        ]['amount'].sum())
        operating_outflow = float(operating_cash[
            operating_cash['type'].str.lower() == 'credit'
        ]['amount'].sum())
        net_operating = operating_inflow - operating_outflow
        
        # Investing activities
        investing_cash = df[
            (df['account'].str.contains('Cash', case=False, na=False)) &
            (df['account'].str.contains('Investment|Property|Equipment', case=False, na=False))
        ]
        investing_inflow = float(investing_cash[
            investing_cash['type'].str.lower() == 'debit'
        ]['amount'].sum())
        investing_outflow = float(investing_cash[
            investing_cash['type'].str.lower() == 'credit'
        ]['amount'].sum())
        net_investing = investing_inflow - investing_outflow
        
        # Financing activities
        financing_cash = df[
            (df['account'].str.contains('Cash', case=False, na=False)) &
            (df['account'].str.contains('Loan|Debt|Capital|Equity', case=False, na=False))
        ]
        financing_inflow = float(financing_cash[
            financing_cash['type'].str.lower() == 'debit'
        ]['amount'].sum())
        financing_outflow = float(financing_cash[
            financing_cash['type'].str.lower() == 'credit'
        ]['amount'].sum())
        net_financing = financing_inflow - financing_outflow
        
        net_change_in_cash = net_operating + net_investing + net_financing
        
        return {
            "period": self._get_period(df),
            "operating_activities": {
                "inflow": float(operating_inflow),
                "outflow": float(operating_outflow),
                "net": float(net_operating)
            },
            "investing_activities": {
                "inflow": float(investing_inflow),
                "outflow": float(investing_outflow),
                "net": float(net_investing)
            },
            "financing_activities": {
                "inflow": float(financing_inflow),
                "outflow": float(financing_outflow),
                "net": float(net_financing)
            },
            "net_change_in_cash": float(net_change_in_cash)
        }
    
    def _calculate_net_income(self, df: pd.DataFrame) -> float:
        """Calculate net income from transactions"""
        revenue = 0
        expenses = 0
        
        for account in self.revenue_accounts:
            revenue_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(revenue_transactions) > 0:
                revenue += float(revenue_transactions[
                    revenue_transactions['type'].str.lower() == 'credit'
                ]['amount'].sum())
        
        for account in self.expense_accounts:
            expense_transactions = df[df['account'].str.contains(account, case=False, na=False)]
            if len(expense_transactions) > 0:
                expenses += float(expense_transactions[
                    expense_transactions['type'].str.lower() == 'debit'
                ]['amount'].sum())
        
        return float(revenue - expenses)
    
    def _get_period(self, df: pd.DataFrame) -> str:
        """Extract period from transaction dates"""
        if len(df) == 0:
            return "N/A"
        min_date = df['date'].min()
        max_date = df['date'].max()
        return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"

