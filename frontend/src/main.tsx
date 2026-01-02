import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Force English locale for entire application
document.documentElement.lang = 'en-US'
document.documentElement.setAttribute('lang', 'en-US')
document.documentElement.setAttribute('xml:lang', 'en-US')

// Set document language meta tag
if (document.querySelector('meta[http-equiv="Content-Language"]')) {
  document.querySelector('meta[http-equiv="Content-Language"]')?.setAttribute('content', 'en-US')
} else {
  const meta = document.createElement('meta')
  meta.setAttribute('http-equiv', 'Content-Language')
  meta.setAttribute('content', 'en-US')
  document.head.appendChild(meta)
}

// Force locale for date inputs
if (typeof Intl !== 'undefined') {
  // Set default locale
  const originalToLocaleString = Date.prototype.toLocaleString
  Date.prototype.toLocaleString = function(...args: any[]) {
    if (args.length === 0 || (args.length === 1 && typeof args[0] === 'string')) {
      return originalToLocaleString.call(this, 'en-US', args[1] || {})
    }
    return originalToLocaleString.apply(this, args as any)
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

