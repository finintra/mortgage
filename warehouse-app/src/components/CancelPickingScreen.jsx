import React, { useState, useEffect } from 'react'

function CancelPickingScreen({ onConfirm, onCancel }) {
  const [pin, setPin] = useState('')
  const [error, setError] = useState(false)
  const PIN_LENGTH = 4

  useEffect(() => {
    if (pin.length === PIN_LENGTH) {
      // Validate PIN (demo: 1234 is correct)
      if (pin === '1234') {
        onConfirm()
      } else {
        setError(true)
        setPin('')
        setTimeout(() => setError(false), 1500)
      }
    }
  }, [pin, onConfirm])

  const handleKeyPress = (key) => {
    if (pin.length < PIN_LENGTH) {
      setPin(prev => prev + key)
    }
  }

  const handleDelete = () => {
    setPin(prev => prev.slice(0, -1))
  }

  return (
    <div className="screen">
      <h1 className="screen-title" style={{ color: '#F44336', fontSize: 'clamp(80px, 12vw, 120px)' }}>
        ВІДМІНИТИ ЗБІРКУ?
      </h1>

      <p className="screen-subtitle" style={{ fontSize: 'clamp(40px, 6vw, 60px)' }}>
        Введіть PIN для підтвердження
      </p>

      {error && (
        <p className="error-message">НЕВІРНИЙ PIN</p>
      )}

      <div className="pin-container">
        <div className="pin-dots">
          {[...Array(PIN_LENGTH)].map((_, i) => (
            <div
              key={i}
              className={`pin-dot ${i < pin.length ? 'filled' : ''}`}
            />
          ))}
        </div>

        <div className="pin-keypad">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(num => (
            <button
              key={num}
              className="pin-key"
              onClick={() => handleKeyPress(num.toString())}
            >
              {num}
            </button>
          ))}
          <button
            className="pin-key"
            onClick={() => handleKeyPress('0')}
            style={{ gridColumn: '2' }}
          >
            0
          </button>
          <button
            className="pin-key delete"
            onClick={handleDelete}
          >
            Видалити
          </button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 20, width: '90%', maxWidth: 600, marginTop: 40 }}>
        <button
          className="button button-gray"
          onClick={onCancel}
          style={{ flex: 1, fontSize: 'clamp(35px, 5vw, 50px)' }}
        >
          СКАСУВАТИ
        </button>
        <button
          className="button button-red"
          onClick={() => pin.length === PIN_LENGTH && onConfirm()}
          style={{ flex: 1, fontSize: 'clamp(35px, 5vw, 50px)', opacity: pin.length === PIN_LENGTH ? 1 : 0.5 }}
        >
          ПІДТВЕРДИТИ
        </button>
      </div>

      <div className="hint-text" style={{ marginTop: 'auto', opacity: 0.5 }}>
        Демо PIN: 1234
      </div>
    </div>
  )
}

export default CancelPickingScreen
