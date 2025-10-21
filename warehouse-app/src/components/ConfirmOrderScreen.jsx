import React, { useState } from 'react'

function ConfirmOrderScreen({ orderId = 'OUT/00123', onSuccess }) {
  const [status, setStatus] = useState('pending') // pending, success, error

  const handleConfirm = () => {
    // Simulate API call
    // For demo: 80% success, 20% order changed error
    const success = Math.random() > 0.2

    if (success) {
      setStatus('success')
      setTimeout(() => {
        onSuccess()
      }, 2000)
    } else {
      setStatus('error')
      // In real app, would reload order data and go back to scanning
      setTimeout(() => {
        setStatus('pending')
      }, 3000)
    }
  }

  if (status === 'success') {
    return (
      <div className="screen screen-success">
        <h1 className="screen-title">
          НЕСИ НА УПАКУВАННЯ
        </h1>
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div className="screen screen-error">
        <h1 className="screen-title" style={{ fontSize: 'clamp(70px, 11vw, 100px)' }}>
          ЗАМОВЛЕННЯ ЗМІНИЛОСЯ
        </h1>
        <div className="screen-subtitle" style={{ color: 'white', fontSize: 'clamp(50px, 7vw, 80px)' }}>
          Тепер ПОТРІБНО: 7
        </div>
        <div className="screen-subtitle" style={{ color: 'white', fontSize: 'clamp(50px, 7vw, 80px)' }}>
          СКАНУЄМО ЗАНОВО
        </div>
      </div>
    )
  }

  return (
    <div className="screen" style={{ justifyContent: 'center', gap: 40 }}>
      <button
        className="button button-green"
        onClick={handleConfirm}
        style={{ minHeight: 120 }}
      >
        <div>ЗАТВЕРДИТИ ЦЕ ЗАМОВЛЕННЯ</div>
        <div style={{ fontSize: 'clamp(35px, 5vw, 50px)', marginTop: 10, fontWeight: 500 }}>
          ({orderId})
        </div>
      </button>

      <div className="hint-text" style={{ opacity: 0.5 }}>
        Натисніть для підтвердження
      </div>
    </div>
  )
}

export default ConfirmOrderScreen
