import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Helper function to get API client with auth token
export const getApiClient = async (getToken) => {
  const token = await getToken()
  
  return axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
    },
  })
}

// API functions
export const api = {
  // Stock predictions
  getStockPrediction: async (symbol, getToken) => {
    const client = await getApiClient(getToken)
    const response = await client.get(`/stocks/predictions?symbol=${symbol}`)
    return response.data
  },

  // Sports predictions
  getSportsPredictions: async (sport = 'basketball_nba', getToken) => {
    const client = await getApiClient(getToken)
    const response = await client.get(`/sports/predictions?sport=${sport}`)
    return response.data
  },

  // User picks
  savePick: async (pick, getToken) => {
    const client = await getApiClient(getToken)
    const response = await client.post('/user/picks', pick)
    return response.data
  },

  getUserPicks: async (getToken) => {
    const client = await getApiClient(getToken)
    const response = await client.get('/user/picks')
    return response.data
  },

  // Analytics
  getAccuracyMetrics: async (predictionType = null, getToken) => {
    const client = await getApiClient(getToken)
    const url = predictionType 
      ? `/analytics/accuracy?prediction_type=${predictionType}`
      : '/analytics/accuracy'
    const response = await client.get(url)
    return response.data
  },

  // Auth
  verifyAuth: async (getToken) => {
    const client = await getApiClient(getToken)
    const response = await client.get('/auth/verify')
    return response.data
  },
}

export default api
