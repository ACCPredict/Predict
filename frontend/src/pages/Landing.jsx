import { Link } from 'react-router-dom'
import { SignInButton, SignUpButton, SignedIn, SignedOut } from '@clerk/clerk-react'
import './Landing.css'

function Landing() {
  return (
    <div className="landing">
      <div className="landing-hero">
        <h1>Predict</h1>
        <p className="subtitle">Probabilistic Predictions for Stocks & Sports Markets</p>
        <p className="description">
          Get AI-powered predictions with confidence scores for stock movements and sports betting markets.
          All predictions are informational only.
        </p>
        <div className="cta-buttons">
          <SignedOut>
            <SignUpButton mode="modal">
              <button className="btn btn-primary">Get Started</button>
            </SignUpButton>
            <SignInButton mode="modal">
              <button className="btn btn-secondary">Sign In</button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <Link to="/dashboard">
              <button className="btn btn-primary">Go to Dashboard</button>
            </Link>
          </SignedIn>
        </div>
      </div>
      <div className="features">
        <div className="feature-card">
          <h3>Stock Predictions</h3>
          <p>Machine learning models analyze price movements and technical indicators to predict stock direction.</p>
        </div>
        <div className="feature-card">
          <h3>Sports Predictions</h3>
          <p>Odds-based predictions adjusted with team ratings for sports betting markets.</p>
        </div>
        <div className="feature-card">
          <h3>Accuracy Tracking</h3>
          <p>Monitor prediction accuracy over time with detailed analytics and charts.</p>
        </div>
      </div>
    </div>
  )
}

export default Landing
