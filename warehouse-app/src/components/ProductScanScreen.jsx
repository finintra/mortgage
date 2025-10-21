import React, { useState, useEffect, useRef } from 'react'

function ProductScanScreen({ order, onProductScanned, onCancelPicking }) {
  // Demo state - in production this would come from props/state management
  const [currentItem] = useState({
    sku: 'SKU-12345',
    name: 'Назва товару приклад',
    required: 5,
    scanned: 2
  })

  const [inputValue, setInputValue] = useState('')
  const inputRef = useRef(null)

  const remaining = currentItem.required - currentItem.scanned

  useEffect(() => {
    // Auto-focus input on mount
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  useEffect(() => {
    // Simulate product scanner listener
    const handleScan = (e) => {
      // For demo: press 'p' to simulate product scan
      if (e.key === 'p') {
        setInputValue('PRODUCT-BARCODE')
        onProductScanned('PRODUCT-BARCODE')
      }
    }

    window.addEventListener('keypress', handleScan)
    return () => window.removeEventListener('keypress', handleScan)
  }, [onProductScanned])

  const handleInputChange = (e) => {
    setInputValue(e.target.value)
  }

  const handleInputSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onProductScanned(inputValue)
      setInputValue('') // Clear input after scan
    }
  }

  const handleCameraClick = async () => {
    // In production, this would trigger camera-based barcode scanning
    alert('Камера відкриється для сканування товару')
  }

  return (
    <div className="screen" style={{ justifyContent: 'flex-start', padding: 0 }}>
      {/* Order header - fixed at top */}
      <div className="order-header">
        {order?.id || 'OUT/00123'}
      </div>

      {/* Scrollable content */}
      <div className="scrollable-content">
        {/* Current product instruction */}
        <div className="instruction-text">
          СКАНУЙ: {currentItem.sku}
        </div>
        <div className="hint-text" style={{ fontSize: 'clamp(35px, 5vw, 50px)', marginBottom: 30 }}>
          {currentItem.name}
        </div>

        {/* Large counters - the most important part */}
        <div className="counters-container">
          {/* Remaining counter */}
          <div className="counter-block counter-remaining">
            <div className="counter-label">ЗАЛИШОК</div>
            <div className="counter-value">{remaining}</div>
          </div>

          {/* Already scanned counter */}
          <div className="counter-block counter-scanned">
            <div className="counter-label">ВЖЕ</div>
            <div className="counter-value">{currentItem.scanned}</div>
          </div>

          {/* Total needed counter */}
          <div className="counter-block counter-total">
            <div className="counter-label">ПОТРІБНО ВСЬОГО</div>
            <div className="counter-value">{currentItem.required}</div>
          </div>
        </div>

        {/* Input zone with camera button */}
        <form onSubmit={handleInputSubmit} className="scan-input-zone">
          <div className="scan-input-container">
            <input
              ref={inputRef}
              type="text"
              className="scan-input"
              placeholder="Скануйте товар"
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

        {/* Hint about what to do */}
        <div className="hint-text" style={{ marginTop: 10 }}>
          Тільки скан товару або ВІДМІНА ЗБІРКИ
        </div>
      </div>

      {/* Fixed bottom section with cancel button */}
      <div className="fixed-bottom">
        <button
          className="button button-orange"
          onClick={onCancelPicking}
        >
          ВІДМІНИТИ ЗБІРКУ
        </button>

        <div className="hint-text" style={{ opacity: 0.5, fontSize: 'clamp(20px, 3vw, 25px)' }}>
          Демо: натисніть 'p' для сканування товару
        </div>
      </div>
    </div>
  )
}

export default ProductScanScreen
