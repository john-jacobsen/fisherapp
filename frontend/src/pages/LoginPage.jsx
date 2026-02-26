import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import { theme } from '../theme.js'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(form.email, form.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Fisher App</h1>
        <p style={styles.subtitle}>Adaptive algebra for statistics students</p>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>Email</label>
          <input
            style={styles.input}
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
            autoFocus
          />
          <label style={styles.label}>Password</label>
          <input
            style={styles.input}
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
          {error && <p style={styles.error}>{error}</p>}
          <button
            style={loading ? { ...styles.button, background: theme.colors.locked, cursor: 'not-allowed' } : styles.button}
            disabled={loading}
            type="submit"
          >
            {loading ? 'Signing in\u2026' : 'Sign In'}
          </button>
        </form>
        <p style={styles.link}>
          No account?{' '}
          <Link to="/register" style={{ color: theme.colors.primary }}>
            Create one
          </Link>
        </p>
      </div>
    </div>
  )
}

const styles = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: theme.colors.bg,
    padding: theme.spacing.md,
  },
  card: {
    background: theme.colors.card,
    borderRadius: theme.radius.lg,
    boxShadow: theme.shadow.md,
    padding: '48px 40px',
    width: '100%',
    maxWidth: '420px',
  },
  title: {
    fontFamily: theme.fonts.serif,
    fontSize: '28px',
    color: theme.colors.primary,
    margin: '0 0 4px',
    textAlign: 'center',
  },
  subtitle: {
    color: theme.colors.textMuted,
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    textAlign: 'center',
    margin: '0 0 32px',
  },
  form: { display: 'flex', flexDirection: 'column', gap: '8px' },
  label: { fontFamily: theme.fonts.sans, fontSize: '14px', fontWeight: 500, color: theme.colors.text },
  input: {
    padding: '10px 12px',
    border: `1px solid ${theme.colors.border}`,
    borderRadius: theme.radius.md,
    fontFamily: theme.fonts.sans,
    fontSize: '15px',
    marginBottom: '8px',
    outline: 'none',
    width: '100%',
    boxSizing: 'border-box',
  },
  button: {
    marginTop: '8px',
    padding: '12px',
    background: theme.colors.primary,
    color: '#fff',
    border: 'none',
    borderRadius: theme.radius.md,
    fontFamily: theme.fonts.sans,
    fontSize: '15px',
    fontWeight: 600,
    cursor: 'pointer',
    width: '100%',
  },
  error: { color: theme.colors.danger, fontSize: '14px', margin: '4px 0' },
  link: {
    textAlign: 'center',
    marginTop: '20px',
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    color: theme.colors.textMuted,
  },
}
