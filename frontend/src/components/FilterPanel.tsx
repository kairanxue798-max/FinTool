import { useState, useEffect } from 'react'
import './FilterPanel.css'

interface FilterPanelProps {
  transactions: any[]
  onFilterChange: (filters: { entity: string | null; startDate: string | null; endDate: string | null }) => void
}

function FilterPanel({ transactions, onFilterChange }: FilterPanelProps) {
  const [entities, setEntities] = useState<string[]>([])
  const [selectedEntity, setSelectedEntity] = useState<string>('')
  const [startDate, setStartDate] = useState<string>('')
  const [endDate, setEndDate] = useState<string>('')

  useEffect(() => {
    // Extract unique entities from transactions
    const uniqueEntities = new Set<string>()
    transactions.forEach(transaction => {
      const entity = transaction.entity || transaction.subsidiary || transaction.company
      if (entity) {
        uniqueEntities.add(entity)
      }
    })
    setEntities(Array.from(uniqueEntities).sort())
  }, [transactions])

  useEffect(() => {
    // Notify parent of filter changes
    onFilterChange({
      entity: selectedEntity || null,
      startDate: startDate || null,
      endDate: endDate || null
    })
  }, [selectedEntity, startDate, endDate, onFilterChange])

  const handleClearFilters = () => {
    setSelectedEntity('')
    setStartDate('')
    setEndDate('')
  }

  return (
    <div className="filter-panel">
      <div className="filter-header">
        <h3>🔍 Filters</h3>
        <button className="clear-filters-btn" onClick={handleClearFilters}>
          Clear All
        </button>
      </div>
      
      <div className="filter-controls">
        <div className="filter-group">
          <label htmlFor="entity-filter">Entity / Subsidiary</label>
          <select
            id="entity-filter"
            className="filter-select"
            value={selectedEntity}
            onChange={(e) => setSelectedEntity(e.target.value)}
          >
            <option value="">All Entities</option>
            {entities.map((entity) => (
              <option key={entity} value={entity}>
                {entity}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="start-date">Start Date</label>
          <input
            id="start-date"
            type="date"
            className="filter-input"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            lang="en"
            placeholder="YYYY-MM-DD"
          />
        </div>

        <div className="filter-group">
          <label htmlFor="end-date">End Date</label>
          <input
            id="end-date"
            type="date"
            className="filter-input"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            lang="en"
            placeholder="YYYY-MM-DD"
          />
        </div>
      </div>

      {(selectedEntity || startDate || endDate) && (
        <div className="active-filters">
          <span className="active-filter-label">Active Filters:</span>
          {selectedEntity && (
            <span className="filter-badge">
              Entity: {selectedEntity}
            </span>
          )}
          {startDate && (
            <span className="filter-badge">
              From: {startDate}
            </span>
          )}
          {endDate && (
            <span className="filter-badge">
              To: {endDate}
            </span>
          )}
        </div>
      )}
    </div>
  )
}

export default FilterPanel

