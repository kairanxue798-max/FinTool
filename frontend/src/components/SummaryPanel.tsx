import { useMemo } from 'react'
import './SummaryPanel.css'

interface SummaryPanelProps {
  transactions: any[]
}

function SummaryPanel({ transactions }: SummaryPanelProps) {
  const metadata = useMemo(() => {
    if (!transactions || transactions.length === 0) {
      return null
    }

    // Calculate total rows
    const totalRows = transactions.length

    // Calculate unique accounts
    const uniqueAccounts = new Set(
      transactions
        .map(t => t.account || t.Account || '')
        .filter(account => account && account.trim() !== '')
    )
    const uniqueAccountsCount = uniqueAccounts.size

    // Calculate date range
    const dates = transactions
      .map(t => {
        const dateStr = t.date || t.Date || t.transaction_date || ''
        if (!dateStr) return null
        // Try to parse the date
        const date = new Date(dateStr)
        return isNaN(date.getTime()) ? null : date
      })
      .filter((date): date is Date => date !== null)
      .sort((a, b) => a.getTime() - b.getTime())

    let dateRange = 'N/A'
    if (dates.length > 0) {
      const startDate = dates[0]
      const endDate = dates[dates.length - 1]
      
      const formatDate = (date: Date) => {
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      }
      
      if (startDate.getTime() === endDate.getTime()) {
        dateRange = formatDate(startDate)
      } else {
        dateRange = `${formatDate(startDate)} – ${formatDate(endDate)}`
      }
    }

    return {
      totalRows,
      uniqueAccountsCount,
      dateRange
    }
  }, [transactions])

  if (!metadata) {
    return null
  }

  return (
    <div className="summary-panel">
      <div className="summary-panel-header">
        <h3 className="summary-panel-title">
          <span className="summary-icon">📊</span>
          File Summary
        </h3>
      </div>
      <div className="summary-panel-content">
        <div className="summary-item">
          <div className="summary-item-label">Total Transactions</div>
          <div className="summary-item-value">{metadata.totalRows.toLocaleString()}</div>
        </div>
        <div className="summary-item">
          <div className="summary-item-label">Unique Accounts</div>
          <div className="summary-item-value">{metadata.uniqueAccountsCount.toLocaleString()}</div>
        </div>
        <div className="summary-item">
          <div className="summary-item-label">Date Range</div>
          <div className="summary-item-value">{metadata.dateRange}</div>
        </div>
      </div>
    </div>
  )
}

export default SummaryPanel

