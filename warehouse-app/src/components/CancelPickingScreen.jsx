import React from 'react'

function CancelPickingScreen({ onConfirm, onCancel }) {
  return (
    <div className="screen" style={{ gap: '30px' }}>
      <div style={{ fontSize: 'clamp(80px, 15vw, 120px)', color: '#F44336' }}>
        ⚠️
      </div>

      <h1 className="screen-title" style={{ color: '#F44336', fontSize: 'clamp(50px, 10vw, 85px)', lineHeight: 1.1 }}>
        ВІДМІНИТИ ЗБІРКУ?
      </h1>

      <p className="screen-subtitle" style={{ fontSize: 'clamp(28px, 5vw, 45px)', color: '#666', lineHeight: 1.3, marginBottom: '20px' }}>
        Прогрес буде втрачено
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', width: '90%', maxWidth: 500 }}>
        <button
          className="button button-red"
          onClick={onConfirm}
          style={{ minHeight: 75, fontSize: 'clamp(30px, 6vw, 50px)', padding: '15px' }}
        >
          ТАК, ВІДМІНИТИ
        </button>
        <button
          className="button button-gray"
          onClick={onCancel}
          style={{ minHeight: 75, fontSize: 'clamp(30px, 6vw, 50px)', padding: '15px' }}
        >
          НІ, ПРОДОВЖИТИ
        </button>
      </div>
    </div>
  )
}

export default CancelPickingScreen
