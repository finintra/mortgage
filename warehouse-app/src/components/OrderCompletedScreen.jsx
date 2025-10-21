import React, { useState } from 'react'

function OrderCompletedScreen({ ttnCount = 5, onConfirm }) {
  const [confirmed, setConfirmed] = useState(false)

  const handleConfirm = () => {
    setConfirmed(true)
    setTimeout(() => {
      onConfirm()
    }, 300)
  }

  return (
    <div className="screen" style={{ padding: 0 }}>
      {/* Green header */}
      <div style={{
        width: '100%',
        background: '#4CAF50',
        padding: '40px 20px',
        textAlign: 'center'
      }}>
        <h1 className="screen-title" style={{ color: 'white', margin: 0 }}>
          ЗАМОВЛЕННЯ ЗІБРАНО
        </h1>
      </div>

      {/* Content */}
      <div className="scrollable-content" style={{ flex: 1, justifyContent: 'center' }}>
        <div className="instruction-text" style={{ marginBottom: 40 }}>
          НАКЛЕЙТЕ ТТНки НА ТОВАРИ
        </div>

        <div style={{
          fontSize: 'clamp(80px, 12vw, 120px)',
          fontWeight: 700,
          textAlign: 'center',
          marginBottom: 60
        }}>
          {ttnCount} ШТУК
        </div>

        <button
          className={`button ${confirmed ? 'button-green' : 'button-gray'}`}
          onClick={handleConfirm}
          style={{
            transition: 'all 0.3s'
          }}
        >
          НАКЛІЄНО {ttnCount} ШТУК
        </button>
      </div>
    </div>
  )
}

export default OrderCompletedScreen
