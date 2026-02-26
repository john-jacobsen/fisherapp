import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import NavBar from '../components/NavBar.jsx'
import api from '../api/client.js'
import { theme } from '../theme.js'

export default function PlacementResults() {
  const navigate = useNavigate()
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.get('/placement/results')
      .then(res => setResults(res.data))
      .catch(err => setError(err.response?.data?.detail || 'Failed to load results'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <>
        <NavBar />
        <div style={styles.center}>
          <p style={{ fontFamily: theme.fonts.sans, color: theme.colors.textMuted }}>
            Calculating your results…
          </p>
        </div>
      </>
    )
  }

  if (error || !results) {
    return (
      <>
        <NavBar />
        <div style={styles.center}>
          <p style={{ color: theme.colors.danger, fontFamily: theme.fonts.sans }}>{error}</p>
          <button onClick={() => navigate('/dashboard')} style={styles.primaryBtn}>Go to Dashboard</button>
        </div>
      </>
    )
  }

  const total = results.mastered_nodes.length + results.ready_nodes.length + results.locked_nodes.length
  const masteredPct = total > 0 ? Math.round((results.mastered_nodes.length / total) * 100) : 0

  return (
    <>
      <NavBar />
      <div style={styles.page}>
        <div style={styles.container}>
          {/* Header */}
          <div style={styles.header}>
            <h1 style={styles.title}>Placement Complete</h1>
            <div style={styles.statsBadges}>
              <div style={styles.badge}>
                <span style={styles.badgeNum}>{results.questions_answered}</span>
                <span style={styles.badgeLabel}>questions</span>
              </div>
              <div style={styles.badge}>
                <span style={styles.badgeNum}>{Math.round(results.accuracy * 100)}%</span>
                <span style={styles.badgeLabel}>accuracy</span>
              </div>
              <div style={styles.badge}>
                <span style={{ ...styles.badgeNum, color: theme.colors.primary }}>{masteredPct}%</span>
                <span style={styles.badgeLabel}>already mastered</span>
              </div>
            </div>
          </div>

          {/* Results grid */}
          <div style={styles.resultsGrid}>
            {/* Mastered */}
            <div style={styles.resultSection}>
              <div style={{ ...styles.sectionHeader, background: theme.colors.primaryLight, borderColor: theme.colors.primary }}>
                <span style={{ ...styles.sectionTitle, color: theme.colors.primary }}>
                  ✓ Mastered ({results.mastered_nodes.length})
                </span>
              </div>
              <div style={styles.nodeList}>
                {results.mastered_nodes.length === 0
                  ? <p style={styles.emptyMsg}>None yet — let's start learning!</p>
                  : results.mastered_nodes.map(n => (
                    <div key={n.node_id} style={styles.nodeItem}>
                      <span style={styles.nodeTopic}>{n.topic}</span>
                      <span style={styles.nodeLabel}>{n.label}</span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Ready */}
            <div style={styles.resultSection}>
              <div style={{ ...styles.sectionHeader, background: theme.colors.accentLight, borderColor: theme.colors.accent }}>
                <span style={{ ...styles.sectionTitle, color: '#8B6914' }}>
                  → Ready to Learn ({results.ready_nodes.length})
                </span>
              </div>
              <div style={styles.nodeList}>
                {results.ready_nodes.length === 0
                  ? <p style={styles.emptyMsg}>Complete prerequisites first.</p>
                  : results.ready_nodes.map(n => (
                    <div key={n.node_id} style={styles.nodeItem}>
                      <span style={styles.nodeTopic}>{n.topic}</span>
                      <span style={styles.nodeLabel}>{n.label}</span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Locked */}
            <div style={styles.resultSection}>
              <div style={{ ...styles.sectionHeader, background: '#F5F4F2', borderColor: theme.colors.locked }}>
                <span style={{ ...styles.sectionTitle, color: theme.colors.textMuted }}>
                  🔒 Locked ({results.locked_nodes.length})
                </span>
              </div>
              <div style={styles.nodeList}>
                {results.locked_nodes.length === 0
                  ? <p style={styles.emptyMsg}>Nothing locked — great work!</p>
                  : results.locked_nodes.map(n => (
                    <div key={n.node_id} style={{ ...styles.nodeItem, opacity: 0.7 }}>
                      <span style={styles.nodeTopic}>{n.topic}</span>
                      <span style={styles.nodeLabel}>{n.label}</span>
                    </div>
                  ))}
              </div>
            </div>
          </div>

          <div style={styles.cta}>
            <button onClick={() => navigate('/dashboard')} style={styles.primaryBtn}>
              Go to My Knowledge Map →
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
    padding: '40px 16px',
  },
  center: {
    minHeight: 'calc(100vh - 56px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'column',
    gap: '16px',
  },
  container: {
    maxWidth: '900px',
    margin: '0 auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '32px',
  },
  header: { textAlign: 'center' },
  title: {
    fontFamily: theme.fonts.serif,
    fontSize: '32px',
    color: theme.colors.text,
    margin: '0 0 24px',
  },
  statsBadges: {
    display: 'flex',
    justifyContent: 'center',
    gap: '32px',
  },
  badge: {
    textAlign: 'center',
    background: theme.colors.card,
    border: `1px solid ${theme.colors.border}`,
    borderRadius: '12px',
    padding: '16px 24px',
    minWidth: '100px',
  },
  badgeNum: {
    display: 'block',
    fontFamily: theme.fonts.serif,
    fontSize: '28px',
    fontWeight: 700,
    color: theme.colors.text,
    lineHeight: 1,
  },
  badgeLabel: {
    display: 'block',
    fontFamily: theme.fonts.sans,
    fontSize: '12px',
    color: theme.colors.textMuted,
    marginTop: '4px',
  },
  resultsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '16px',
  },
  resultSection: {
    background: theme.colors.card,
    border: `1px solid ${theme.colors.border}`,
    borderRadius: '12px',
    overflow: 'hidden',
  },
  sectionHeader: {
    padding: '12px 16px',
    borderBottom: '1px solid',
  },
  sectionTitle: {
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    fontWeight: 600,
  },
  nodeList: {
    padding: '8px',
    maxHeight: '320px',
    overflowY: 'auto',
  },
  nodeItem: {
    padding: '8px 8px',
    display: 'flex',
    flexDirection: 'column',
    gap: '2px',
    borderRadius: '6px',
  },
  nodeTopic: {
    fontFamily: theme.fonts.sans,
    fontSize: '10px',
    color: theme.colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  nodeLabel: {
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    color: theme.colors.text,
  },
  emptyMsg: {
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    color: theme.colors.textMuted,
    padding: '16px 8px',
    margin: 0,
  },
  cta: { textAlign: 'center' },
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
}
