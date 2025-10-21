import React, { useState, useEffect, useRef } from 'react'

function BadgeScanScreen({ onBadgeScanned }) {
  const [error, setError] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    // Auto-focus input on mount
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  useEffect(() => {
    // Simulate barcode scanner listener
    const handleScan = (e) => {
      // In production, this would listen to actual scanner input
      // For demo: press 'b' to simulate badge scan, 'x' for invalid badge
      if (e.key === 'b') {
        setInputValue('BADGE-12345')
        onBadgeScanned('BADGE-12345')
      } else if (e.key === 'x') {
        setError(true)
        setTimeout(() => setError(false), 1000)
      }
    }

    window.addEventListener('keypress', handleScan)
    return () => window.removeEventListener('keypress', handleScan)
  }, [onBadgeScanned])

  const handleInputChange = (e) => {
    setInputValue(e.target.value)
  }

  const handleInputSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onBadgeScanned(inputValue)
    }
  }

  const handleCameraClick = async () => {
    // In production, this would trigger camera-based barcode scanning
    // Using libraries like html5-qrcode or @zxing/browser
    alert('Камера відкриється для сканування штрихкоду')

    // Example implementation would be:
    // const result = await scanBarcodeWithCamera()
    // if (result) {
    //   setInputValue(result)
    //   onBadgeScanned(result)
    // }
  }

  if (error) {
    return (
      <div className="screen screen-error">
        <h1 className="screen-title">
          БЕЙДЖ НЕ ВПІЗНАНО.<br />
          СКАНУЙТЕ ЩЕ РАЗ
        </h1>
      </div>
    )
  }

  return (
    <div className="screen">
      <h1 className="screen-title">СКАНУЙТЕ БЕЙДЖ</h1>

      <div className="screen-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="4" y="6" width="16" height="12" rx="2" />
          <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
          <line x1="8" y1="10" x2="8" y2="14" />
          <line x1="10" y1="10" x2="10" y2="14" />
          <line x1="12" y1="10" x2="12" y2="14" />
          <line x1="14" y1="10" x2="14" y2="14" />
          <line x1="16" y1="10" x2="16" y2="14" />
        </svg>
      </div>

      <p className="screen-subtitle">
        Піднесіть сканер до штрихкоду бейджа
      </p>

      {/* Input zone with camera button */}
      <form onSubmit={handleInputSubmit} className="scan-input-zone">
        <div className="scan-input-container">
          <input
            ref={inputRef}
            type="text"
            className="scan-input"
            placeholder="Скануйте або введіть"
            value={inputValue}
            onChange={handleInputChange}
            autoFocus
          />
          <button
            type="button"
            className="camera-button"
            onClick={handleCameraClick}
            aria-label="Відкрити камеру"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
          </button>
        </div>
        <p className="input-hint">Або натисніть камеру для сканування</p>
      </form>

      <div className="hint-text" style={{ marginTop: 'auto', opacity: 0.5 }}>
        Демо: натисніть 'b' для сканування
      </div>
    </div>
  )
}

export default BadgeScanScreen
