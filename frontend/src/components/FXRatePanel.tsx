import { useState, useEffect } from 'react'
import './FXRatePanel.css'

interface FXRate {
  currency: string
  rate: string
  date: string
}

const FALLBACK_RATES: Array<{ currency: string; rate: number }> = [
  { currency: 'USD', rate: 0.65 },
  { currency: 'EUR', rate: 0.60 },
  { currency: 'GBP', rate: 0.52 },
  { currency: 'JPY', rate: 97.5 },
  { currency: 'CNY', rate: 4.7 },
  { currency: 'HKD', rate: 5.08 },
  { currency: 'SGD', rate: 0.88 },
  { currency: 'NZD', rate: 1.08 },
  { currency: 'CAD', rate: 0.89 },
  { currency: 'CHF', rate: 0.58 },
]

function FXRatePanel() {
  const [selectedDate, setSelectedDate] = useState<string>('')
  const [fxRates, setFxRates] = useState<FXRate[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Set default date to current month
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    setSelectedDate(`${year}-${month}`)
  }, [])

  const getFallbackRates = (date: string): FXRate[] =>
    FALLBACK_RATES.map(rate => ({
      currency: rate.currency,
      rate: String(rate.rate),
      date,
    }))

  const fetchATOFXRates = async (date: string) => {
    if (!date) return

    setLoading(true)
    setError(null)

    try {
      // Extract year and month from date (YYYY-MM format)
      const [year, month] = date.split('-')
      
      if (!year || !month) {
        throw new Error('Invalid date format')
      }
      
      // Call backend to fetch ATO rates
      const response = await fetch(`/api/fx/ato-rates?year=${year}&month=${month}`)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: Failed to fetch FX rates`)
      }

      const data = await response.json()
      
      if (data.success && data.data) {
        if (data.data.rates && Object.keys(data.data.rates).length > 0) {
          // Convert rates object to array
          const ratesArray: FXRate[] = Object.entries(data.data.rates).map(([currency, rate]) => ({
            currency,
            rate: String(rate),
            date: data.data.date || date
          }))
          setFxRates(ratesArray)
          
          // Show note if using fallback rates
          if (data.data.source === 'fallback' && data.data.note) {
            setError(null) // Don't show as error, but could show as info
          }
        } else {
          setFxRates([])
          setError('No rates found for selected period')
        }
      } else {
        setFxRates([])
        setError('Invalid response from server')
      }
    } catch (err: any) {
      console.error('FX Rate fetch error:', err)
      setError(err.message || 'Failed to fetch FX rates from ATO. Using fallback rates.')
      // Still try to show fallback rates
      setFxRates(getFallbackRates(date))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (selectedDate) {
      fetchATOFXRates(selectedDate)
    }
  }, [selectedDate])

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(e.target.value)
  }

  return (
    <div className="fx-rate-panel">
      <div className="fx-header">
        <h3>💱 Foreign Exchange Rates (ATO)</h3>
        <a 
          href="https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-2026-financial-year" 
          target="_blank" 
          rel="noopener noreferrer"
          className="ato-link"
        >
          View on ATO Website →
        </a>
      </div>

      <div className="fx-controls">
        <div className="fx-date-selector">
          <label htmlFor="fx-date">Select Month:</label>
          <input
            id="fx-date"
            type="month"
            className="fx-date-input"
            value={selectedDate}
            onChange={handleDateChange}
            lang="en-US"
            data-lang="en-US"
          />
        </div>
      </div>

      {loading && (
        <div className="fx-loading">
          <div className="spinner"></div>
          <span>Loading FX rates from ATO...</span>
        </div>
      )}

      {!loading && fxRates.length > 0 && (
        <div className="fx-rates-table-container">
          <div className="fx-rates-info">
            <span>Base Currency: <strong>AUD</strong></span>
            <span>Period: <strong>{selectedDate}</strong></span>
          </div>
          <div className="fx-rates-table-wrapper">
            <table className="fx-rates-table">
              <thead>
                <tr>
                  <th>Currency</th>
                  <th>Rate (AUD per unit)</th>
                </tr>
              </thead>
              <tbody>
                {fxRates.map((rate, index) => (
                  <tr key={index}>
                    <td className="currency-code">{rate.currency}</td>
                    <td className="rate-value">{parseFloat(rate.rate).toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {!loading && !error && fxRates.length === 0 && selectedDate && (
        <div className="fx-empty">
          No rates available for selected period. Please try a different month.
        </div>
      )}
    </div>
  )
}

export default FXRatePanel

