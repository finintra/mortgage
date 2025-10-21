import React from 'react'

function ErrorExtraItemScreen() {
  return (
    <div className="screen screen-error">
      <div className="screen-icon" style={{ fontSize: 'clamp(120px, 20vw, 180px)', color: 'white' }}>
        ⚠
      </div>
      <h1 className="screen-title">
        ЦЕ ЛИШНІЙ ТОВАР
      </h1>
    </div>
  )
}

export default ErrorExtraItemScreen
