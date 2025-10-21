import React from 'react'

function ErrorNotInOrderScreen() {
  return (
    <div className="screen screen-error">
      <div className="screen-icon" style={{ fontSize: 'clamp(120px, 20vw, 180px)', color: 'white' }}>
        ✕
      </div>
      <h1 className="screen-title" style={{ fontSize: 'clamp(80px, 12vw, 120px)' }}>
        ЦЬОГО ТОВАРУ НЕМАЄ У ЗАМОВЛЕННІ
      </h1>
    </div>
  )
}

export default ErrorNotInOrderScreen
