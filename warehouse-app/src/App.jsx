import React, { useState, useEffect } from 'react'

// Import all screen components
import BadgeScanScreen from './components/BadgeScanScreen'
import PinEntryScreen from './components/PinEntryScreen'
import InvoiceScanScreen from './components/InvoiceScanScreen'
import ProductScanScreen from './components/ProductScanScreen'
import SuccessScanScreen from './components/SuccessScanScreen'
import ErrorExtraItemScreen from './components/ErrorExtraItemScreen'
import ErrorNotInOrderScreen from './components/ErrorNotInOrderScreen'
import LineCompletedScreen from './components/LineCompletedScreen'
import OrderCompletedScreen from './components/OrderCompletedScreen'
import ConfirmOrderScreen from './components/ConfirmOrderScreen'
import CancelPickingScreen from './components/CancelPickingScreen'
import AccountLockedScreen from './components/AccountLockedScreen'

function App() {
  const [currentScreen, setCurrentScreen] = useState('badge-scan')
  const [appState, setAppState] = useState({
    user: null,
    currentOrder: null,
    currentProduct: null,
    scannedCount: 0,
    requiredCount: 0,
  })

  // Demo: Handle keyboard input for testing
  useEffect(() => {
    const handleKeyPress = (e) => {
      // Press 'n' to navigate through screens (for testing)
      if (e.key === 'n') {
        const screens = [
          'badge-scan',
          'pin-entry',
          'invoice-scan',
          'product-scan',
          'order-completed',
          'confirm-order'
        ]
        const currentIndex = screens.indexOf(currentScreen)
        const nextIndex = (currentIndex + 1) % screens.length
        setCurrentScreen(screens[nextIndex])
      }
    }
    window.addEventListener('keypress', handleKeyPress)
    return () => window.removeEventListener('keypress', handleKeyPress)
  }, [currentScreen])

  const handleBadgeScanned = (badgeId) => {
    // Simulate badge validation
    if (badgeId === 'INVALID') {
      // Show error briefly, then return to scan
      setTimeout(() => {
        setCurrentScreen('badge-scan')
      }, 1000)
    } else {
      setAppState(prev => ({ ...prev, user: { badgeId } }))
      setCurrentScreen('pin-entry')
    }
  }

  const handlePinEntered = (pin, success) => {
    if (success) {
      setCurrentScreen('invoice-scan')
    }
    // Error state is handled within PinEntryScreen
  }

  const handleInvoiceScanned = (invoiceId) => {
    setAppState(prev => ({
      ...prev,
      currentOrder: {
        id: invoiceId,
        items: [
          { sku: 'SKU-001', name: 'Товар 1', required: 5, scanned: 0 },
          { sku: 'SKU-002', name: 'Товар 2', required: 3, scanned: 0 },
        ]
      }
    }))
    setCurrentScreen('product-scan')
  }

  const handleProductScanned = (barcode) => {
    // This would normally validate the barcode against the order
    // For now, just increment the counter
    setCurrentScreen('success-scan')
    setTimeout(() => {
      setCurrentScreen('product-scan')
    }, 400)
  }

  const handleCancelPicking = () => {
    setCurrentScreen('cancel-picking')
  }

  const handleConfirmCancel = () => {
    setCurrentScreen('badge-scan')
    setAppState({
      user: null,
      currentOrder: null,
      currentProduct: null,
      scannedCount: 0,
      requiredCount: 0,
    })
  }

  const renderScreen = () => {
    switch (currentScreen) {
      case 'badge-scan':
        return <BadgeScanScreen onBadgeScanned={handleBadgeScanned} />

      case 'pin-entry':
        return <PinEntryScreen onPinEntered={handlePinEntered} />

      case 'invoice-scan':
        return <InvoiceScanScreen onInvoiceScanned={handleInvoiceScanned} />

      case 'product-scan':
        return (
          <ProductScanScreen
            order={appState.currentOrder}
            onProductScanned={handleProductScanned}
            onCancelPicking={handleCancelPicking}
          />
        )

      case 'success-scan':
        return <SuccessScanScreen />

      case 'error-extra':
        return <ErrorExtraItemScreen />

      case 'error-not-in-order':
        return <ErrorNotInOrderScreen />

      case 'line-completed':
        return <LineCompletedScreen />

      case 'order-completed':
        return (
          <OrderCompletedScreen
            ttnCount={5}
            onConfirm={() => setCurrentScreen('confirm-order')}
          />
        )

      case 'confirm-order':
        return (
          <ConfirmOrderScreen
            orderId={appState.currentOrder?.id}
            onSuccess={() => setCurrentScreen('badge-scan')}
          />
        )

      case 'cancel-picking':
        return (
          <CancelPickingScreen
            onConfirm={handleConfirmCancel}
            onCancel={() => setCurrentScreen('product-scan')}
          />
        )

      case 'account-locked':
        return <AccountLockedScreen />

      default:
        return <BadgeScanScreen onBadgeScanned={handleBadgeScanned} />
    }
  }

  return (
    <div className="app">
      {renderScreen()}
    </div>
  )
}

export default App
