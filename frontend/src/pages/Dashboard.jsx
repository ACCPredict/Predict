import { useState, useEffect } from 'react'
import { useAuth } from '@clerk/clerk-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '../services/api'
import './Dashboard.css'

function Dashboard() {
  const { getToken } = useAuth()
  const [accuracyData, setAccuracyData] = useState([])
  const [userPicks, setUserPicks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [accuracy, picks] = await Promise.all([
        api.getAccuracyMetrics(null, getToken),
        api.getUserPicks(getToken)
      ])
      setAccuracyData(accuracy)
      setUserPicks(picks.slice(0, 5)) // Show recent 5 picks
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>
  }

  // Prepare chart data
  const chartData = accuracyData.map(metric => ({
    type: metric.prediction_type,
    accuracy: (metric.accuracy_rate * 100).toFixed(1),
    total: metric.total_predictions
  }))

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h2>Accuracy Metrics</h2>
          {accuracyData.length > 0 ? (
            <div className="metrics-list">
              {accuracyData.map((metric, idx) => (
                <div key={idx} className="metric-item">
                  <span className="metric-type">{metric.prediction_type}</span>
                  <span className="metric-value">
                    {(metric.accuracy_rate * 100).toFixed(1)}%
                  </span>
                  <span className="metric-count">
                    {metric.correct_predictions} / {metric.total_predictions}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p>No accuracy data available yet.</p>
          )}
        </div>

        <div className="dashboard-card">
          <h2>Accuracy Chart</h2>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="type" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="accuracy" stroke="#8884d8" name="Accuracy %" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p>No chart data available.</p>
          )}
        </div>

        <div className="dashboard-card">
          <h2>Recent Picks</h2>
          {userPicks.length > 0 ? (
            <div className="picks-list">
              {userPicks.map((pick) => (
                <div key={pick.id} className="pick-item">
                  <div className="pick-header">
                    <span className="pick-type">{pick.prediction_type}</span>
                    <span className="pick-symbol">{pick.symbol_or_event}</span>
                  </div>
                  <div className="pick-confidence">
                    Confidence: {(pick.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No saved picks yet.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
