import { useState } from 'react'
import FileUpload from './components/FileUpload'
import FinancialStatements from './components/FinancialStatements'
import AIAnalysis from './components/AIAnalysis'
import FinancialChatbot from './components/FinancialChatbot'
import InteractiveDotsGrid from './components/InteractiveDotsGrid'
import FilterPanel from './components/FilterPanel'
import FXRatePanel from './components/FXRatePanel'
import SummaryPanel from './components/SummaryPanel'
import './App.css'

interface FinancialData {
  balance_sheet: any
  profit_loss: any
  cash_flow: any
}

function App() {
  const [allTransactions, setAllTransactions] = useState<any[]>([]) // Store unfiltered transactions
  const [transactions, setTransactions] = useState<any[]>([]) // Displayed transactions (may be filtered)
  const [financialData, setFinancialData] = useState<FinancialData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<{
    entity: string | null
    startDate: string | null
    endDate: string | null
  }>({
    entity: null,
    startDate: null,
    endDate: null
  })

  const handleFileUpload = async (file: File) => {
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('file', file)

      const uploadResponse = await fetch('/api/upload-csv', {
        method: 'POST',
        body: formData,
      })

      if (!uploadResponse.ok) {
        throw new Error('Failed to upload CSV')
      }

      const uploadData = await uploadResponse.json()
      // Store all transactions (unfiltered)
      setAllTransactions(uploadData.transactions)
      setTransactions(uploadData.transactions)

      // Generate financial statements with all transactions initially
      const statementsResponse = await fetch('/api/generate-statements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: {
            transactions: uploadData.transactions,
          },
        }),
      })

      if (!statementsResponse.ok) {
        throw new Error('Failed to generate financial statements')
      }

      const statementsData = await statementsResponse.json()
      setFinancialData({
        balance_sheet: statementsData.balance_sheet,
        profit_loss: statementsData.profit_loss,
        cash_flow: statementsData.cash_flow,
      })
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Handle filter changes
  const handleFilterChange = (newFilters: {
    entity: string | null
    startDate: string | null
    endDate: string | null
  }) => {
    setFilters(newFilters)
    
    // Re-apply filters to transactions and regenerate statements
    if (allTransactions.length > 0) {
      const filteredTransactions = allTransactions.filter((t: any) => {
        if (newFilters.entity) {
          const entity = t.entity || t.subsidiary || t.company
          if (entity !== newFilters.entity) return false
        }
        if (newFilters.startDate && t.date < newFilters.startDate) return false
        if (newFilters.endDate && t.date > newFilters.endDate) return false
        return true
      })

      setTransactions(filteredTransactions)

      if (filteredTransactions.length === 0) {
        setFinancialData(null)
        setError('No transactions match the selected filters. Please adjust your filters.')
        return
      }

      setError(null) // Clear previous errors

      // Regenerate statements with filtered data
      fetch('/api/generate-statements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: {
            transactions: filteredTransactions,
          },
        }),
      })
        .then(async res => {
          if (!res.ok) {
            const errorData = await res.json().catch(() => ({}))
            throw new Error(errorData.detail || `HTTP ${res.status}: Failed to regenerate statements`)
          }
          return res.json()
        })
        .then(data => {
          if (data.balance_sheet && data.profit_loss && data.cash_flow) {
            setFinancialData({
              balance_sheet: data.balance_sheet,
              profit_loss: data.profit_loss,
              cash_flow: data.cash_flow,
            })
            setError(null)
          } else {
            throw new Error('Invalid response format from server')
          }
        })
        .catch(err => {
          console.error('Error regenerating statements:', err)
          setError(err.message || 'Failed to regenerate statements with filters. Please try again.')
          // Keep previous financial data on error so user can see what was there
        })
    }
  }

  return (
    <div className="app">
      <InteractiveDotsGrid />
      <header className="app-header">
        <h1>💰 Financial Statement Generator</h1>
        <p>Upload CSV files to generate Financial Statements</p>
      </header>

      <main className="app-main">
        <FXRatePanel />
        
        <FileUpload onFileUpload={handleFileUpload} loading={loading} />
        
        {allTransactions.length > 0 && (
          <>
            <SummaryPanel transactions={allTransactions} />
            <FilterPanel 
              transactions={allTransactions} 
              onFilterChange={handleFilterChange}
            />
          </>
        )}
        
        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

        {financialData && (
          <>
            <FinancialStatements data={financialData} />
            <AIAnalysis financialData={financialData} />
          </>
        )}
        
        {/* Chatbot is always available, even without financial statements */}
        <FinancialChatbot 
          financialData={financialData || undefined} 
          transactions={transactions}
          selectedEntity={filters.entity || undefined}
        />
      </main>
    </div>
  )
}

export default App

