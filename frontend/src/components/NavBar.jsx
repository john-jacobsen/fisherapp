import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import { theme } from '../theme.js'

export default function NavBar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav style={styles.nav}>
      <div style={styles.inner}>
        <Link to="/dashboard" style={styles.brand}>
          Fisher App
        </Link>
        <div style={styles.links}>
          {user && (
            <>
              <Link to="/dashboard" style={styles.link}>Dashboard</Link>
              <Link to="/reviews" style={styles.link}>Reviews</Link>
              <Link to="/settings" style={styles.link}>Settings</Link>
              <button onClick={handleLogout} style={styles.logoutBtn}>
                Sign Out
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

const styles = {
  nav: {
    background: theme.colors.card,
    borderBottom: `1px solid ${theme.colors.border}`,
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  inner: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: `0 ${theme.spacing.lg}`,
    height: '56px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  brand: {
    fontFamily: theme.fonts.serif,
    fontSize: '20px',
    fontWeight: 700,
    color: theme.colors.primary,
    textDecoration: 'none',
  },
  links: {
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing.lg,
  },
  link: {
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    color: theme.colors.textMuted,
    textDecoration: 'none',
  },
  logoutBtn: {
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    color: theme.colors.textMuted,
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: 0,
  },
}
