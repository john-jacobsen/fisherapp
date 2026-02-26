import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import { theme } from '../theme.js'

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', name: '', password: '', courseCode: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await register(form.email, form.name, form.password, form.courseCode || null)
      navigate('/placement/intro')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Create Account</h1>
        <p style={styles.subtitle}>Fisher App 3.0</p>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>Full Name</label>
          <input
            style={styles.input}
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
            autoFocus
          />
          <label style={styles.label}>Email</label>
          <input
            style={styles.input}
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
          <label style={styles.label}>Password</label>
          <input
            style={styles.input}
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
            minLength={8}
          />
          <label style={styles.label}>
            Course Code{' '}
            <span style={{ color: theme.colors.textMuted, fontWeight: 400 }}>(optional)</span>
          </label>
          <input
            style={styles.input}
            type="text"
            value={form.courseCode}
            onChange={(e) => setForm({ ...form, courseCode: e.target.value })}
            placeholder="e.g. STAT-20-FA26"
          />
          {error && <p style={styles.error}>{error}</p>}
          <button
            style={loading ? { ...styles.button, background: theme.colors.locked, cursor: 'not-allowed' } : styles.button}
            disabled={loading}
            type="submit"
          >
            {loading ? 'Creating account\u2026' : 'Create Account'}
          </button>
        </form>
        <p style={styles.link}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: theme.colors.primary }}>
            Sign in
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
