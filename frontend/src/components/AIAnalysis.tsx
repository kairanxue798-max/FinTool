import { useState } from 'react'
import { buildApiUrl } from '../utils/api'
import './AIAnalysis.css'

interface AIAnalysisProps {
  financialData: {
    balance_sheet: any
    profit_loss: any
    cash_flow: any
  }
}

function AIAnalysis({ financialData }: AIAnalysisProps) {
  const [varianceAnalysis, setVarianceAnalysis] = useState<any>(null)
  const [kpiAnalysis, setKpiAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [kpiTargets, setKpiTargets] = useState({
    'Net Income': 100000,
    'Total Revenue': 500000,
    'Total Assets': 1000000,
  })

  const handleVarianceAnalysis = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // For demo purposes, we'll use current period as both current and previous
      // In a real scenario, you'd have separate periods
      const response = await fetch(buildApiUrl('/api/ai/variance-analysis'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_period: financialData.profit_loss,
          previous_period: {
            ...financialData.profit_loss,
            revenue: { total: financialData.profit_loss.revenue.total * 0.9 },
            expenses: { total: financialData.profit_loss.expenses.total * 1.1 },
          },
          period_name: 'Current Period',
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate variance analysis')
      }

      const data = await response.json()
      setVarianceAnalysis(data.analysis)
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleKPIAnalysis = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(buildApiUrl('/api/ai/kpi-analysis'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          financial_data: {
            'Net Income': financialData.profit_loss.net_income,
            'Total Revenue': financialData.profit_loss.revenue.total,
            'Total Assets': financialData.balance_sheet.assets.total,
          },
          kpi_targets: kpiTargets,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate KPI analysis')
      }

      const data = await response.json()
      setKpiAnalysis(data.analysis)
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const updateKpiTarget = (kpi: string, value: number) => {
    setKpiTargets({ ...kpiTargets, [kpi]: value })
  }

  return (
    <div className="ai-analysis">
      <h2>🤖 AI-Powered Analysis</h2>
      
      <div className="analysis-section">
        <div className="analysis-card">
          <h3>Variance Analysis</h3>
          <p>Compare current period performance with previous period</p>
          <button
            className="analysis-button"
            onClick={handleVarianceAnalysis}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Run Variance Analysis'}
          </button>

          {varianceAnalysis && (
            <div className="analysis-results">
              <div className="summary">
                <h4>Summary</h4>
                <p>{varianceAnalysis.summary}</p>
              </div>

              {varianceAnalysis.key_variances && varianceAnalysis.key_variances.length > 0 && (
                <div className="variances">
                  <h4>Key Variances</h4>
                  <table className="analysis-table">
                    <thead>
                      <tr>
                        <th>Item</th>
                        <th>Current</th>
                        <th>Previous</th>
                        <th>Variance</th>
                        <th>% Change</th>
                      </tr>
                    </thead>
                    <tbody>
                      {varianceAnalysis.key_variances.map((v: any, idx: number) => (
                        <tr key={idx}>
                          <td>{v.item}</td>
                          <td>${v.current?.toLocaleString() || 0}</td>
                          <td>${v.previous?.toLocaleString() || 0}</td>
                          <td className={v.variance >= 0 ? 'positive' : 'negative'}>
                            ${v.variance?.toLocaleString() || 0}
                          </td>
                          <td>{v.percentage_change?.toFixed(2) || 0}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {varianceAnalysis.recommendations && (
                <div className="recommendations">
                  <h4>Recommendations</h4>
                  <ul>
                    {varianceAnalysis.recommendations.map((rec: string, idx: number) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="analysis-card">
          <h3>KPI Achievement Analysis</h3>
          <p>Analyze performance against key performance indicators</p>
          
          <div className="kpi-targets">
            <h4>Set KPI Targets</h4>
            {Object.entries(kpiTargets).map(([kpi, target]) => (
              <div key={kpi} className="kpi-input">
                <label>{kpi}:</label>
                <input
                  type="number"
                  value={target}
                  onChange={(e) => updateKpiTarget(kpi, parseFloat(e.target.value) || 0)}
                />
              </div>
            ))}
          </div>

          <button
            className="analysis-button"
            onClick={handleKPIAnalysis}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Run KPI Analysis'}
          </button>

          {kpiAnalysis && (
            <div className="analysis-results">
              <div className="summary">
                <h4>Overall Performance</h4>
                <p>{kpiAnalysis.overall_performance}</p>
              </div>

              {kpiAnalysis.kpi_results && kpiAnalysis.kpi_results.length > 0 && (
                <div className="kpi-results">
                  <h4>KPI Results</h4>
                  <table className="analysis-table">
                    <thead>
                      <tr>
                        <th>KPI</th>
                        <th>Target</th>
                        <th>Actual</th>
                        <th>Achievement %</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {kpiAnalysis.kpi_results.map((kpi: any, idx: number) => (
                        <tr key={idx}>
                          <td>{kpi.kpi_name}</td>
                          <td>${kpi.target?.toLocaleString() || 0}</td>
                          <td>${kpi.actual?.toLocaleString() || 0}</td>
                          <td>{kpi.achievement_percentage?.toFixed(2) || 0}%</td>
                          <td>
                            <span className={`status-badge ${kpi.status}`}>
                              {kpi.status === 'achieved' ? '✓ Achieved' : '✗ Not Achieved'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {kpiAnalysis.action_items && (
                <div className="action-items">
                  <h4>Action Items</h4>
                  <ul>
                    {kpiAnalysis.action_items.map((item: string, idx: number) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {error && (
        <div className="error-message">
          <p>❌ {error}</p>
        </div>
      )}
    </div>
  )
}

export default AIAnalysis

