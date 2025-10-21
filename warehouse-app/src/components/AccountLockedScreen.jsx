import React from 'react'

function AccountLockedScreen() {
  const handleClose = () => {
    // In production, this would close the app or redirect
    window.location.reload()
  }

  return (
    <div className="screen" style={{ background: '#B71C1C' }}>
      <div className="screen-icon" style={{ fontSize: 'clamp(100px, 18vw, 160px)', color: 'white' }}>
        🔒
      </div>

      <h1 className="screen-title" style={{ color: 'white', fontSize: 'clamp(70px, 11vw, 120px)' }}>
        АКАУНТ ДЕАКТИВОВАНО
      </h1>

      <p className="screen-subtitle" style={{ color: 'white', fontSize: 'clamp(35px, 5vw, 50px)' }}>
        Зверніться до адміністратора
      </p>

      <button
        className="button button-gray"
        onClick={handleClose}
        style={{ marginTop: 60, background: 'rgba(255,255,255,0.3)', color: 'white' }}
      >
        ЗАКРИТИ ЗАСТОСУНОК
      </button>
    </div>
  )
}

export default AccountLockedScreen
