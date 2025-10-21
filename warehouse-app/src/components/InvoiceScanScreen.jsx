import React, { useState, useEffect } from 'react'

function InvoiceScanScreen({ onInvoiceScanned }) {
  const [error, setError] = useState(false)

  useEffect(() => {
    // Simulate invoice scanner listener
    const handleScan = (e) => {
      // For demo: press 'i' to simulate invoice scan, 'w' for wrong invoice
      if (e.key === 'i') {
        onInvoiceScanned('OUT/00123')
      } else if (e.key === 'w') {
        setError(true)
        setTimeout(() => setError(false), 1000)
      }
    }

    window.addEventListener('keypress', handleScan)
    return () => window.removeEventListener('keypress', handleScan)
  }, [onInvoiceScanned])

  if (error) {
    return (
      <div className="screen screen-error">
        <h1 className="screen-title">
          НЕ ТА НАКЛАДНА.<br />
          СКАНУЙ ПРАВИЛЬНУ
        </h1>
      </div>
    )
  }

  return (
    <div className="screen">
      <h1 className="screen-title">СКАНУЙ НАКЛАДНУ (OUT...)</h1>

      <div className="screen-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="8" y1="12" x2="16" y2="12" />
          <line x1="8" y1="16" x2="16" y2="16" />
        </svg>
      </div>

      <p className="screen-subtitle">
        Піднесіть сканер до накладної
      </p>

      <div className="hint-text" style={{ marginTop: 'auto', opacity: 0.5 }}>
        Демо: натисніть 'i' для сканування
      </div>
    </div>
  )
}

export default InvoiceScanScreen
