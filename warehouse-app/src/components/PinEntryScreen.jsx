import React, { useState, useEffect } from 'react'

function PinEntryScreen({ onPinEntered }) {
  const [pin, setPin] = useState('')
  const [error, setError] = useState(false)
  const [success, setSuccess] = useState(false)
  const PIN_LENGTH = 4

  useEffect(() => {
    if (pin.length === PIN_LENGTH) {
      // Validate PIN (demo: 1234 is correct)
      if (pin === '1234') {
        setSuccess(true)
        setTimeout(() => {
          onPinEntered(pin, true)
        }, 400)
      } else {
        setError(true)
        setPin('')
        setTimeout(() => setError(false), 1500)
      }
    }
  }, [pin, onPinEntered])

  const handleKeyPress = (key) => {
    if (pin.length < PIN_LENGTH) {
      setPin(prev => prev + key)
    }
  }

  const handleDelete = () => {
    setPin(prev => prev.slice(0, -1))
  }

  if (success) {
    return (
      <div className="screen screen-success">
        <h1 className="screen-title">✓</h1>
        <p className="screen-subtitle">ГОТОВО</p>
      </div>
    )
  }

  return (
    <div className="screen">
      <h1 className="screen-title">ВВЕДІТЬ PIN</h1>

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

      <div className="hint-text" style={{ marginTop: 'auto', opacity: 0.5 }}>
        Демо PIN: 1234
      </div>
    </div>
  )
}

export default PinEntryScreen
