import { useNavigate } from 'react-router-dom'
import { theme } from '../theme.js'
import NavBar from '../components/NavBar.jsx'

export default function PlacementIntro() {
  const navigate = useNavigate()

  return (
    <>
      <NavBar />
      <div style={styles.page}>
        <div style={styles.card}>
          <div style={styles.iconRow}>
            <div style={styles.icon}>📐</div>
          </div>
          <h1 style={styles.title}>Algebra Placement Test</h1>
          <p style={styles.lead}>
            This short adaptive test helps us understand your algebra background so we can
            recommend the right starting points for you.
          </p>

          <div style={styles.infoGrid}>
            <div style={styles.infoItem}>
              <div style={styles.infoNumber}>~5</div>
              <div style={styles.infoLabel}>minutes</div>
            </div>
            <div style={styles.infoItem}>
              <div style={styles.infoNumber}>12–15</div>
              <div style={styles.infoLabel}>questions</div>
            </div>
            <div style={styles.infoItem}>
              <div style={styles.infoNumber}>8</div>
              <div style={styles.infoLabel}>topics</div>
            </div>
          </div>

          <div style={styles.detailBox}>
            <p style={styles.detailText}>
              The test adapts to your answers — it won't ask questions that are too easy or too hard.
              There are no hints during the placement test. Answer as best you can; it's okay if you're unsure.
            </p>
            <p style={styles.detailText}>
              Topics covered: Fractions, Exponents, Order of Operations, Equations, Logarithms,
              Summation, Combinatorics, and Geometric Series.
            </p>
          </div>

          <div style={styles.buttonRow}>
            <button
              onClick={() => navigate('/placement/start')}
              style={styles.primaryBtn}
            >
              Start Placement Test
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              style={styles.secondaryBtn}
            >
              Skip — start from the beginning
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

const styles = {
  page: {
    minHeight: 'calc(100vh - 56px)',
    background: theme.colors.bg,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px 16px',
  },
  card: {
    background: theme.colors.card,
    borderRadius: '16px',
    boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
    padding: '56px 48px',
    maxWidth: '560px',
    width: '100%',
    textAlign: 'center',
  },
  iconRow: { marginBottom: '16px' },
  icon: { fontSize: '48px' },
  title: {
    fontFamily: theme.fonts.serif,
    fontSize: '28px',
    color: theme.colors.text,
    margin: '0 0 16px',
  },
  lead: {
    fontFamily: theme.fonts.sans,
    fontSize: '16px',
    color: theme.colors.textMuted,
    lineHeight: 1.6,
    margin: '0 0 32px',
  },
  infoGrid: {
    display: 'flex',
    justifyContent: 'center',
    gap: '40px',
    margin: '0 0 32px',
  },
  infoItem: { textAlign: 'center' },
  infoNumber: {
    fontFamily: theme.fonts.serif,
    fontSize: '32px',
    fontWeight: 700,
    color: theme.colors.primary,
    lineHeight: 1,
  },
  infoLabel: {
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    color: theme.colors.textMuted,
    marginTop: '4px',
  },
  detailBox: {
    background: theme.colors.bg,
    borderRadius: '8px',
    padding: '16px 20px',
    margin: '0 0 32px',
    textAlign: 'left',
  },
  detailText: {
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    color: theme.colors.textMuted,
    lineHeight: 1.6,
    margin: '0 0 8px',
  },
  buttonRow: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  primaryBtn: {
    background: theme.colors.primary,
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    padding: '14px 32px',
    fontFamily: theme.fonts.sans,
    fontSize: '15px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  secondaryBtn: {
    background: 'transparent',
    color: theme.colors.textMuted,
    border: `1px solid ${theme.colors.border}`,
    borderRadius: '8px',
    padding: '12px 32px',
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    cursor: 'pointer',
  },
}
