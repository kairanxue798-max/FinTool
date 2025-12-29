import { useState } from 'react'
import './FinancialStatements.css'

interface FinancialStatementsProps {
  data: {
    balance_sheet: any
    profit_loss: any
    cash_flow: any
  }
}

function FinancialStatements({ data }: FinancialStatementsProps) {
  const [activeTab, setActiveTab] = useState<'bs' | 'pl' | 'cf'>('bs')

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  const renderBalanceSheet = () => {
    const bs = data.balance_sheet
    return (
      <div className="statement-content">
        <h3>Balance Sheet - As of {bs.as_of_date}</h3>
        <div className="statement-section">
          <h4>Assets</h4>
          <table className="financial-table">
            <tbody>
              {Object.entries(bs.assets.items).map(([key, value]: [string, any]) => (
                <tr key={key}>
                  <td className="account-name">{key}</td>
                  <td className="amount">{formatCurrency(value)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total Assets</strong></td>
                <td><strong>{formatCurrency(bs.assets.total)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <h4>Liabilities</h4>
          <table className="financial-table">
            <tbody>
              {Object.entries(bs.liabilities.items).map(([key, value]: [string, any]) => (
                <tr key={key}>
                  <td className="account-name">{key}</td>
                  <td className="amount">{formatCurrency(value)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total Liabilities</strong></td>
                <td><strong>{formatCurrency(bs.liabilities.total)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <h4>Equity</h4>
          <table className="financial-table">
            <tbody>
              {Object.entries(bs.equity.items).map(([key, value]: [string, any]) => (
                <tr key={key}>
                  <td className="account-name">{key}</td>
                  <td className="amount">{formatCurrency(value)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total Equity</strong></td>
                <td><strong>{formatCurrency(bs.equity.total)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <table className="financial-table">
            <tbody>
              <tr className="grand-total-row">
                <td><strong>Total Liabilities and Equity</strong></td>
                <td><strong>{formatCurrency(bs.total_liabilities_and_equity)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    )
  }

  const renderProfitLoss = () => {
    const pl = data.profit_loss
    return (
      <div className="statement-content">
        <h3>Profit & Loss Statement</h3>
        <p className="period">Period: {pl.period}</p>
        
        <div className="statement-section">
          <h4>Revenue</h4>
          <table className="financial-table">
            <tbody>
              {Object.entries(pl.revenue.items).map(([key, value]: [string, any]) => (
                <tr key={key}>
                  <td className="account-name">{key}</td>
                  <td className="amount">{formatCurrency(value)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total Revenue</strong></td>
                <td><strong>{formatCurrency(pl.revenue.total)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <h4>Expenses</h4>
          <table className="financial-table">
            <tbody>
              {Object.entries(pl.expenses.items).map(([key, value]: [string, any]) => (
                <tr key={key}>
                  <td className="account-name">{key}</td>
                  <td className="amount">{formatCurrency(value)}</td>
                </tr>
              ))}
              <tr className="total-row">
                <td><strong>Total Expenses</strong></td>
                <td><strong>{formatCurrency(pl.expenses.total)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <table className="financial-table">
            <tbody>
              <tr className={`grand-total-row ${pl.net_income >= 0 ? 'positive' : 'negative'}`}>
                <td><strong>Net Income</strong></td>
                <td><strong>{formatCurrency(pl.net_income)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    )
  }

  const renderCashFlow = () => {
    const cf = data.cash_flow
    return (
      <div className="statement-content">
        <h3>Cash Flow Statement</h3>
        <p className="period">Period: {cf.period}</p>
        
        <div className="statement-section">
          <h4>Operating Activities</h4>
          <table className="financial-table">
            <tbody>
              <tr>
                <td className="account-name">Cash Inflow</td>
                <td className="amount positive">{formatCurrency(cf.operating_activities.inflow)}</td>
              </tr>
              <tr>
                <td className="account-name">Cash Outflow</td>
                <td className="amount negative">{formatCurrency(cf.operating_activities.outflow)}</td>
              </tr>
              <tr className="total-row">
                <td><strong>Net Operating Cash Flow</strong></td>
                <td><strong className={cf.operating_activities.net >= 0 ? 'positive' : 'negative'}>
                  {formatCurrency(cf.operating_activities.net)}
                </strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <h4>Investing Activities</h4>
          <table className="financial-table">
            <tbody>
              <tr>
                <td className="account-name">Cash Inflow</td>
                <td className="amount positive">{formatCurrency(cf.investing_activities.inflow)}</td>
              </tr>
              <tr>
                <td className="account-name">Cash Outflow</td>
                <td className="amount negative">{formatCurrency(cf.investing_activities.outflow)}</td>
              </tr>
              <tr className="total-row">
                <td><strong>Net Investing Cash Flow</strong></td>
                <td><strong className={cf.investing_activities.net >= 0 ? 'positive' : 'negative'}>
                  {formatCurrency(cf.investing_activities.net)}
                </strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <h4>Financing Activities</h4>
          <table className="financial-table">
            <tbody>
              <tr>
                <td className="account-name">Cash Inflow</td>
                <td className="amount positive">{formatCurrency(cf.financing_activities.inflow)}</td>
              </tr>
              <tr>
                <td className="account-name">Cash Outflow</td>
                <td className="amount negative">{formatCurrency(cf.financing_activities.outflow)}</td>
              </tr>
              <tr className="total-row">
                <td><strong>Net Financing Cash Flow</strong></td>
                <td><strong className={cf.financing_activities.net >= 0 ? 'positive' : 'negative'}>
                  {formatCurrency(cf.financing_activities.net)}
                </strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="statement-section">
          <table className="financial-table">
            <tbody>
              <tr className={`grand-total-row ${cf.net_change_in_cash >= 0 ? 'positive' : 'negative'}`}>
                <td><strong>Net Change in Cash</strong></td>
                <td><strong>{formatCurrency(cf.net_change_in_cash)}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    )
  }

  return (
    <div className="financial-statements">
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'bs' ? 'active' : ''}`}
          onClick={() => setActiveTab('bs')}
        >
          Balance Sheet
        </button>
        <button
          className={`tab ${activeTab === 'pl' ? 'active' : ''}`}
          onClick={() => setActiveTab('pl')}
        >
          Profit & Loss
        </button>
        <button
          className={`tab ${activeTab === 'cf' ? 'active' : ''}`}
          onClick={() => setActiveTab('cf')}
        >
          Cash Flow
        </button>
      </div>

      <div className="statement-container">
        {activeTab === 'bs' && renderBalanceSheet()}
        {activeTab === 'pl' && renderProfitLoss()}
        {activeTab === 'cf' && renderCashFlow()}
      </div>
    </div>
  )
}

export default FinancialStatements

