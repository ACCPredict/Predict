import { Link, useLocation } from 'react-router-dom'
import { UserButton, useUser } from '@clerk/clerk-react'
import './Layout.css'

function Layout({ children }) {
  const location = useLocation()
  const { user } = useUser()

  const isActive = (path) => location.pathname === path

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/dashboard" className="nav-logo">
            Predict
          </Link>
          <div className="nav-links">
            <Link 
              to="/dashboard" 
              className={isActive('/dashboard') ? 'active' : ''}
            >
              Dashboard
            </Link>
            <Link 
              to="/stocks" 
              className={isActive('/stocks') ? 'active' : ''}
            >
              Stocks
            </Link>
            <Link 
              to="/sports" 
              className={isActive('/sports') ? 'active' : ''}
            >
              Sports
            </Link>
            <Link 
              to="/profile" 
              className={isActive('/profile') ? 'active' : ''}
            >
              Profile
            </Link>
          </div>
          <div className="nav-user">
            <UserButton />
          </div>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout
