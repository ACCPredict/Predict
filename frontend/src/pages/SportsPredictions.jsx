import { useState, useEffect } from 'react'
import { useAuth } from '@clerk/clerk-react'
import api from '../services/api'
import './SportsPredictions.css'

function SportsPredictions() {
  const { getToken } = useAuth()
  const [sport, setSport] = useState('basketball_nba')
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadPredictions()
  }, [sport])

  const loadPredictions = async () => {
    setLoading(true)
    setError(null)
    setPredictions([])

    try {
      const data = await api.getSportsPredictions(sport, getToken)
      setPredictions(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load predictions')
    } finally {
      setLoading(false)
    }
  }

  const handleSavePick = async (prediction) => {
    try {
      await api.savePick({
        prediction_type: 'sports',
        symbol_or_event: prediction.event_id,
        prediction: prediction,
        confidence: prediction.confidence
      }, getToken)
      alert('Pick saved successfully!')
    } catch (err) {
      alert('Failed to save pick')
    }
  }

  return (
    <div className="sports-predictions">
      <h1>Sports Predictions</h1>
      
      <div className="sport-selector">
        <label htmlFor="sport-select">Sport:</label>
        <select
          id="sport-select"
          value={sport}
          onChange={(e) => setSport(e.target.value)}
          className="sport-select"
        >
          <option value="basketball_nba">NBA</option>
          <option value="americanfootball_nfl">NFL</option>
          <option value="icehockey_nhl">NHL</option>
          <option value="baseball_mlb">MLB</option>
          <option value="soccer_epl">Premier League</option>
        </select>
        <button onClick={loadPredictions} disabled={loading} className="refresh-button">
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading && predictions.length === 0 && (
        <div className="loading-message">Loading predictions...</div>
      )}

      {!loading && predictions.length === 0 && !error && (
        <div className="no-predictions">No predictions available for this sport.</div>
      )}

      <div className="predictions-grid">
        {predictions.map((prediction, idx) => (
          <div key={idx} className="prediction-card">
            <div className="prediction-header">
              <h3>Event {prediction.event_id.slice(0, 8)}</h3>
              <button 
                onClick={() => handleSavePick(prediction)}
                className="save-button"
              >
                Save
              </button>
            </div>
            
            <div className="prediction-details">
              {prediction.team && (
                <div className="prediction-item">
                  <span className="label">Team:</span>
                  <span className="value">{prediction.team}</span>
                </div>
              )}
              
              <div className="prediction-item">
                <span className="label">Outcome:</span>
                <span className={`value outcome-${prediction.outcome}`}>
                  {prediction.outcome.toUpperCase()}
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
              
              {prediction.odds && (
                <div className="prediction-item">
                  <span className="label">Odds:</span>
                  <span className="value">{prediction.odds}</span>
                </div>
              )}
              
              {prediction.implied_probability && (
                <div className="prediction-item">
                  <span className="label">Implied Prob:</span>
                  <span className="value">
                    {(prediction.implied_probability * 100).toFixed(1)}%
                  </span>
                </div>
              )}
            </div>

            <div className="probability-bar">
              <div 
                className="probability-fill"
                style={{ width: `${prediction.probability * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SportsPredictions
