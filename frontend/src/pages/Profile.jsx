import { useState, useEffect } from 'react'
import { useAuth, useUser } from '@clerk/clerk-react'
import api from '../services/api'
import './Profile.css'

function Profile() {
  const { getToken } = useAuth()
  const { user } = useUser()
  const [userPicks, setUserPicks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUserPicks()
  }, [])

  const loadUserPicks = async () => {
    try {
      setLoading(true)
      const picks = await api.getUserPicks(getToken)
      setUserPicks(picks)
    } catch (error) {
      console.error('Failed to load user picks:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="profile-loading">Loading profile...</div>
  }

  return (
    <div className="profile">
      <h1>Profile</h1>
      
      <div className="profile-info">
        <div className="info-card">
          <h2>User Information</h2>
          <div className="info-item">
            <span className="info-label">Email:</span>
            <span className="info-value">{user?.primaryEmailAddress?.emailAddress || 'N/A'}</span>
          </div>
          <div className="info-item">
            <span className="info-label">User ID:</span>
            <span className="info-value">{user?.id || 'N/A'}</span>
          </div>
        </div>
      </div>

      <div className="picks-section">
        <h2>My Saved Picks ({userPicks.length})</h2>
        
        {userPicks.length === 0 ? (
          <div className="no-picks">
            <p>You haven't saved any picks yet.</p>
            <p>Start exploring predictions and save your favorites!</p>
          </div>
        ) : (
          <div className="picks-list">
            {userPicks.map((pick) => (
              <div key={pick.id} className="pick-card">
                <div className="pick-header">
                  <span className="pick-type">{pick.prediction_type.toUpperCase()}</span>
                  <span className="pick-date">
                    {new Date(pick.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="pick-content">
                  <div className="pick-symbol">
                    {pick.symbol_or_event}
                  </div>
                  <div className="pick-confidence">
                    Confidence: {(pick.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Profile
