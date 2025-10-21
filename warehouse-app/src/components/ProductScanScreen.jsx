import React, { useState, useEffect } from 'react'

function ProductScanScreen({ order, onProductScanned, onCancelPicking }) {
  // Demo state - in production this would come from props/state management
  const [currentItem] = useState({
    sku: 'SKU-12345',
    name: 'Назва товару приклад',
    required: 5,
    scanned: 2
  })

  const remaining = currentItem.required - currentItem.scanned

  useEffect(() => {
    // Simulate product scanner listener
    const handleScan = (e) => {
      // For demo: press 'p' to simulate product scan
      if (e.key === 'p') {
        onProductScanned('PRODUCT-BARCODE')
      }
    }

    window.addEventListener('keypress', handleScan)
    return () => window.removeEventListener('keypress', handleScan)
  }, [onProductScanned])

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

        {/* Hint about what to do */}
        <div className="hint-text" style={{ marginTop: 30 }}>
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
