import React from 'react'

function SuccessScanScreen() {
  return (
    <div className="screen screen-success">
      <div className="screen-title" style={{ fontSize: 'clamp(150px, 25vw, 250px)' }}>
        ✓
      </div>
      <div className="screen-subtitle" style={{ color: 'white', fontSize: 'clamp(80px, 12vw, 120px)' }}>
        +1
      </div>
    </div>
  )
}

export default SuccessScanScreen
