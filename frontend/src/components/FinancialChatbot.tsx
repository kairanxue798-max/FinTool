import { useState, useRef, useEffect } from 'react'
import './FinancialChatbot.css'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface FinancialChatbotProps {
  financialData?: {
    balance_sheet?: any
    profit_loss?: any
    cash_flow?: any
  }
  transactions?: any[]
  selectedEntity?: string
}

function FinancialChatbot({ financialData, transactions = [], selectedEntity }: FinancialChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m your financial AI assistant. I can help you with:\n\n• Multi-entity/subsidiary analysis\n• KPI metrics (AR Aging, DSO)\n• Revenue analytics (YTD, variance, trailing 3M, TOP N)\n• Foreign exchange rates\n• Unusual transaction detection\n• Financial statement insights\n\nTry asking me with the suggested questions below! 👇',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const question = input.trim().toLowerCase()
    setInput('')
    setLoading(true)

    try {
      // Check if it's a KPI/revenue analytics question and call appropriate endpoint
      let kpiResult = null
      
      if (question.includes('revenue ytd') || question.includes('ytd revenue')) {
        const response = await fetch('/api/kpi/revenue-ytd', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('revenue variance') || question.includes('variance')) {
        const response = await fetch('/api/kpi/revenue-variance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('trailing 3') || question.includes('3 months')) {
        const response = await fetch('/api/kpi/trailing-3m', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('top') && (question.includes('revenue') || question.includes('transaction'))) {
        const response = await fetch('/api/kpi/top-n', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('unusual') || question.includes('weekend')) {
        const response = await fetch('/api/kpi/unusual-transactions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('ar aging') || question.includes('aging')) {
        const response = await fetch('/api/kpi/ar-aging', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('dso') || question.includes('days sales outstanding')) {
        const response = await fetch('/api/kpi/dso', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transactions, entity: selectedEntity, period_days: 30 })
        })
        if (response.ok) {
          kpiResult = await response.json()
        }
      } else if (question.includes('fx rate') || question.includes('exchange rate')) {
        const dateMatch = question.match(/\d{4}-\d{2}-\d{2}/)
        const date = dateMatch ? dateMatch[0] : null
        const url = `/api/fx/rates?base_currency=USD${date ? `&date=${date}` : ''}`
        const response = await fetch(url)
        if (response.ok) {
          kpiResult = await response.json()
        }
      }

      // Prepare financial data context
      const financialContext = financialData ? {
        balance_sheet: financialData.balance_sheet,
        profit_loss: financialData.profit_loss,
        cash_flow: financialData.cash_flow
      } : null

      // Prepare conversation history
      const conversationHistory = messages.slice(-10).map(msg => ({
        role: msg.role,
        content: msg.content
      }))

      // Build message with KPI result if available
      let enhancedMessage = userMessage.content
      if (kpiResult && kpiResult.data) {
        enhancedMessage += `\n\nKPI Calculation Result:\n${JSON.stringify(kpiResult.data, null, 2)}`
      }

      // Check if we have transactions for subsidiary questions
      const questionLower = userMessage.content.toLowerCase()
      const needsTransactions = questionLower.includes('subsidiary') || 
                                questionLower.includes('entity') || 
                                questionLower.includes('highest revenue') ||
                                questionLower.includes('compare') && questionLower.includes('revenue')
      
      if (needsTransactions && (!transactions || transactions.length === 0)) {
        const warningMessage: Message = {
          role: 'assistant',
          content: 'I need transaction data to answer questions about subsidiaries. Please upload a CSV file with your financial transactions first. The CSV should include columns like: date, account, amount, type, and entity (or subsidiary).',
          timestamp: new Date()
        }
        setMessages(prev => [...prev, warningMessage])
        return
      }

      // Prepare request payload
      const requestPayload = {
        message: enhancedMessage,
        financial_data: financialContext,
        transactions: transactions && transactions.length > 0 ? transactions : null,
        conversation_history: conversationHistory,
        entity: selectedEntity
      }
      
      console.log('Sending chat request:', {
        messageLength: enhancedMessage.length,
        hasFinancialData: !!financialContext,
        transactionCount: transactions?.length || 0,
        hasEntity: !!selectedEntity
      })

      // Directly make the chat request - let it fail naturally if backend is down
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestPayload),
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorDetail = 'Failed to get AI response'
        try {
          const errorJson = JSON.parse(errorText)
          errorDetail = errorJson.detail || errorJson.message || errorDetail
        } catch {
          errorDetail = errorText || errorDetail
        }
        throw new Error(`${errorDetail} (Status: ${response.status})`)
      }

      const data = await response.json()
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response || data.data?.response || 'I apologize, but I couldn\'t generate a response. Please try again.',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error: any) {
      console.error('Chatbot error:', error)
      let errorMsg = error.message || 'Unknown error occurred'
      
      // Provide more helpful error messages
      if (errorMsg.includes('Failed to fetch') || errorMsg.includes('NetworkError') || errorMsg.includes('ERR_CONNECTION_REFUSED')) {
        // Test if backend is actually running
        try {
          const testResponse = await fetch('/api/health', { 
            method: 'GET',
            signal: AbortSignal.timeout(3000)
          })
          if (testResponse.ok) {
            errorMsg = 'Backend is running but chat endpoint failed. Please check backend logs or try again.'
          } else {
            errorMsg = `Backend health check returned status ${testResponse.status}. Please check if backend is running correctly.`
          }
        } catch (testError: any) {
          errorMsg = `Cannot connect to backend server on port 8000.\n\nTroubleshooting:\n1. Check if backend is running: open terminal and run "curl http://localhost:8000/api/health"\n2. Restart backend: cd backend && source venv/bin/activate && python main.py\n3. Check browser console (F12) for detailed errors\n4. Try refreshing the page`
        }
      }
      
      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMsg}\n\nPlease make sure the backend server is running and try again.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const formatMessage = (content: string) => {
    // Split by newlines and create paragraphs
    const lines = content.split('\n')
    return lines.map((line, index) => {
      if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
        return <li key={index}>{line.trim().substring(1).trim()}</li>
      }
      if (line.trim() === '') {
        return <br key={index} />
      }
      return <p key={index}>{line}</p>
    })
  }

  return (
    <div className="financial-chatbot">
      <div className="chatbot-header">
        <h3>🤖 Financial AI Assistant</h3>
        <p>Ask me anything about your financial data</p>
      </div>

      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              {message.role === 'assistant' && (
                <div className="message-avatar">🤖</div>
              )}
              <div className="message-text">
                {formatMessage(message.content)}
              </div>
              {message.role === 'user' && (
                <div className="message-avatar">👤</div>
              )}
            </div>
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant-message">
            <div className="message-content">
              <div className="message-avatar">🤖</div>
              <div className="message-text">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chatbot-input-container">
        <textarea
          className="chatbot-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about variance analysis, KPIs, financial insights..."
          rows={2}
          disabled={loading}
        />
        <button
          className="chatbot-send-button"
          onClick={handleSend}
          disabled={loading || !input.trim()}
        >
          {loading ? '⏳' : '➤'}
        </button>
      </div>

      {!financialData && (
        <div className="chatbot-warning">
          💡 Upload financial data first for more accurate analysis
        </div>
      )}

      <div className="suggested-questions">
        <h4>💡 Try asking me:</h4>
        <div className="question-chips">
          <button
            className="question-chip"
            onClick={() => setInput("What's the revenue YTD?")}
          >
            Revenue YTD
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Show me revenue variance compared to previous month")}
          >
            Revenue Variance
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Calculate trailing 3 months rolling revenue")}
          >
            Trailing 3M Revenue
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Show me TOP 10 revenue transactions")}
          >
            TOP N Revenue
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Find unusual transactions posted on weekends")}
          >
            Unusual Transactions
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Calculate AR Aging report")}
          >
            AR Aging
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("What's the DSO (Days Sales Outstanding)?")}
          >
            DSO Calculation
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Show me FX rates for USD")}
          >
            FX Rates
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Which subsidiary has the highest revenue?")}
          >
            Highest Revenue Entity
          </button>
          <button
            className="question-chip"
            onClick={() => setInput("Compare revenue across all subsidiaries")}
          >
            Compare Entities
          </button>
        </div>
      </div>
    </div>
  )
}

export default FinancialChatbot

