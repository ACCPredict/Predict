import { useState } from 'react'
import { useAuth } from '@clerk/clerk-react'
import api from '../services/api'
import './StockPredictions.css'

function StockPredictions() {
  const { getToken } = useAuth()
  const [symbol, setSymbol] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!symbol.trim()) return

    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const data = await api.getStockPrediction(symbol.toUpperCase(), getToken)
      setPrediction(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  const handleSavePick = async () => {
    if (!prediction) return

    try {
      await api.savePick({
        prediction_type: 'stock',
        symbol_or_event: prediction.symbol,
        prediction: prediction,
        confidence: prediction.confidence
      }, getToken)
      alert('Pick saved successfully!')
    } catch (err) {
      alert('Failed to save pick')
    }
  }

  return (
    <div className="stock-predictions">
      <h1>Stock Predictions</h1>
      
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Enter stock symbol (e.g., AAPL, MSFT, GOOGL)"
          className="search-input"
        />
        <button type="submit" disabled={loading} className="search-button">
          {loading ? 'Loading...' : 'Get Prediction'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {prediction && (
        <div className="prediction-card">
          <div className="prediction-header">
            <h2>{prediction.symbol}</h2>
            <button onClick={handleSavePick} className="save-button">
              Save Pick
            </button>
          </div>
          
          <div className="prediction-details">
            <div className="prediction-item">
              <span className="label">Direction:</span>
              <span className={`value direction-${prediction.direction}`}>
                {prediction.direction.toUpperCase()}
              </span>
            </div>
            
            <div className="prediction-item">
              <span className="label">Probability:</span>
              <span className="value">
                {(prediction.probability * 100).toFixed(1)}%
              </span>
            </div>
            
            <div className="prediction-item">
              <span className="label">Confidence:</span>
              <span className="value">
                {(prediction.confidence * 100).toFixed(1)}%
              </span>
            </div>
            
            {prediction.current_price && (
              <div className="prediction-item">
                <span className="label">Current Price:</span>
                <span className="value">${prediction.current_price.toFixed(2)}</span>
              </div>
            )}
            
            {prediction.price_target && (
              <div className="prediction-item">
                <span className="label">Price Target:</span>
                <span className="value">${prediction.price_target.toFixed(2)}</span>
              </div>
            )}
            
            <div className="prediction-item">
              <span className="label">Model Version:</span>
              <span className="value">{prediction.model_version}</span>
            </div>
          </div>

          <div className="probability-bar">
            <div 
              className="probability-fill"
              style={{ width: `${prediction.probability * 100}%` }}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default StockPredictions
