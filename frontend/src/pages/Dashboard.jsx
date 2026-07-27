import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import NavBar from '../components/NavBar.jsx'
import KnowledgeGraph from '../components/KnowledgeGraph.jsx'
import KnowledgeList from '../components/KnowledgeList.jsx'
import ReviewBanner from '../components/ReviewBanner.jsx'
import api from '../api/client.js'
import { theme } from '../theme.js'

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [viewMode, setViewMode] = useState('graph') // 'graph' | 'list'
  const [bannerDismissed, setBannerDismissed] = useState(false)

  useEffect(() => {
    api.get('/dashboard')
      .then(res => setData(res.data))
      .catch(err => setError(err.response?.data?.detail || 'Failed to load dashboard'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <>
        <NavBar />
        <div style={styles.loading}>Loading your knowledge map…</div>
      </>
    )
  }

  if (error) {
    return (
      <>
        <NavBar />
        <div style={styles.error}>{error}</div>
      </>
    )
  }

  const { knowledge_map, stats, recommended_next, review_enforcement, placement_completed } = data

  return (
    <>
      <NavBar />
      <div style={styles.page}>
        <div style={styles.container}>

          {/* Placement CTA (if not done) */}
          {!placement_completed && (
            <div style={styles.placementBanner}>
              <div>
                <strong style={{ fontFamily: theme.fonts.serif }}>Take the placement test</strong>
                <p style={{ margin: '4px 0 0', fontSize: '14px', color: theme.colors.textMuted }}>
                  ~5 minutes · ~12-15 questions · Identifies your algebra strengths
                </p>
              </div>
              <button
                onClick={() => navigate('/placement/intro')}
                style={styles.primaryBtn}
              >
                Start Placement Test
              </button>
            </div>
          )}

          {/* Reviews due banner — tiered escalating soft gate (14-10) */}
          <ReviewBanner
            enforcement={review_enforcement}
            dismissed={bannerDismissed}
            onDismiss={() => setBannerDismissed(true)}
          />

          {/* Stats row */}
          <div style={styles.statsRow}>
            <div style={styles.statCard}>
              <div style={{ ...styles.statNumber, color: theme.colors.primary }}>{stats.mastered_count}</div>
              <div style={styles.statLabel}>Mastered</div>
            </div>
            <div style={styles.statCard}>
              <div style={{ ...styles.statNumber, color: theme.colors.accent }}>{stats.ready_count}</div>
              <div style={styles.statLabel}>Ready to Learn</div>
            </div>
            <div style={styles.statCard}>
              <div style={{ ...styles.statNumber, color: theme.colors.textMuted }}>{stats.total_count - stats.mastered_count - stats.ready_count}</div>
              <div style={styles.statLabel}>Locked</div>
            </div>
            <div style={styles.statCard}>
              <div style={{ ...styles.statNumber, color: theme.colors.text }}>
                {Math.round(stats.overall_progress * 100)}%
              </div>
              <div style={styles.statLabel}>Overall Progress</div>
            </div>
          </div>

          {/* Main layout: map + sidebar */}
          <div style={styles.mainLayout}>
            {/* Knowledge map */}
            <div style={styles.mapArea}>
              <div style={styles.mapHeader}>
                <h2 style={styles.sectionTitle}>Knowledge Map</h2>
                <div style={styles.viewToggle}>
                  <button
                    onClick={() => setViewMode('graph')}
                    style={viewMode === 'graph' ? styles.toggleActive : styles.toggleInactive}
                  >
                    Graph
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    style={viewMode === 'list' ? styles.toggleActive : styles.toggleInactive}
                  >
                    List
                  </button>
                </div>
              </div>

              {viewMode === 'graph' ? (
                <KnowledgeGraph
                  nodes={knowledge_map.nodes}
                  edges={knowledge_map.edges}
                />
              ) : (
                <KnowledgeList nodes={knowledge_map.nodes} />
              )}
            </div>

            {/* Sidebar */}
            <div style={styles.sidebar}>
              {/* Recommended next */}
              {recommended_next && (
                <div style={styles.sideCard}>
                  <h3 style={styles.sideCardTitle}>Recommended Next</h3>
                  <div style={styles.recommendedCard}>
                    <div style={{ fontSize: '12px', color: '#8B6914', fontWeight: 600, marginBottom: 4 }}>
                      {recommended_next.topic}
                    </div>
                    <div style={{ fontFamily: theme.fonts.serif, fontSize: '16px', color: theme.colors.text, marginBottom: 12 }}>
                      {recommended_next.label}
                    </div>
                    <button
                      onClick={() => navigate(`/lesson/${recommended_next.node_id}`)}
                      style={styles.accentBtn}
                    >
                      Start Learning →
                    </button>
                  </div>
                </div>
              )}

              {/* Legend */}
              <div style={styles.sideCard}>
                <h3 style={styles.sideCardTitle}>Legend</h3>
                {[
                  { color: theme.colors.primary, bg: theme.colors.primaryLight, label: 'Mastered' },
                  { color: theme.colors.accent, bg: theme.colors.accentLight, label: 'Ready to Learn' },
                  { color: theme.colors.locked, bg: '#F5F4F2', label: 'Locked' },
                ].map(({ color, bg, label }) => (
                  <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <div style={{
                      width: 16,
                      height: 16,
                      borderRadius: 4,
                      background: bg,
                      border: `2px solid ${color}`,
                    }} />
                    <span style={{ fontFamily: theme.fonts.sans, fontSize: '13px', color: theme.colors.text }}>{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

const styles = {
  page: {
    background: theme.colors.bg,
    minHeight: 'calc(100vh - 56px)',
    padding: `${theme.spacing.xl} ${theme.spacing.lg}`,
  },
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    display: 'flex',
    flexDirection: 'column',
    gap: theme.spacing.lg,
  },
  loading: {
    padding: 60,
    textAlign: 'center',
    color: theme.colors.textMuted,
    fontFamily: theme.fonts.sans,
  },
  error: {
    padding: 60,
    textAlign: 'center',
    color: theme.colors.danger,
    fontFamily: theme.fonts.sans,
  },
  reviewBanner: {
    background: '#FFF8E7',
    border: `1px solid ${theme.colors.accent}`,
    borderRadius: theme.radius.md,
    padding: `${theme.spacing.md} ${theme.spacing.lg}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    color: '#8B6914',
  },
  reviewBtn: {
    background: theme.colors.accent,
    color: '#fff',
    border: 'none',
    borderRadius: theme.radius.md,
    padding: '8px 16px',
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  placementBanner: {
    background: theme.colors.primaryLight,
    border: `1px solid ${theme.colors.primary}`,
    borderRadius: theme.radius.md,
    padding: `${theme.spacing.lg} ${theme.spacing.xl}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: theme.spacing.lg,
  },
  primaryBtn: {
    background: theme.colors.primary,
    color: '#fff',
    border: 'none',
    borderRadius: theme.radius.md,
    padding: '12px 24px',
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    fontWeight: 600,
    cursor: 'pointer',
    whiteSpace: 'nowrap',
  },
  statsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: theme.spacing.md,
  },
  statCard: {
    background: theme.colors.card,
    border: `1px solid ${theme.colors.border}`,
    borderRadius: theme.radius.md,
    padding: theme.spacing.lg,
    textAlign: 'center',
    boxShadow: theme.shadow.sm,
  },
  statNumber: {
    fontFamily: theme.fonts.serif,
    fontSize: '32px',
    fontWeight: 700,
    lineHeight: 1,
    marginBottom: 4,
  },
  statLabel: {
    fontFamily: theme.fonts.sans,
    fontSize: '12px',
    color: theme.colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  mainLayout: {
    display: 'grid',
    gridTemplateColumns: '1fr 280px',
    gap: theme.spacing.lg,
    alignItems: 'start',
  },
  mapArea: {
    background: theme.colors.card,
    border: `1px solid ${theme.colors.border}`,
    borderRadius: theme.radius.lg,
    padding: theme.spacing.lg,
    boxShadow: theme.shadow.sm,
  },
  mapHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: theme.spacing.md,
  },
  sectionTitle: {
    fontFamily: theme.fonts.serif,
    fontSize: '18px',
    color: theme.colors.text,
    margin: 0,
  },
  viewToggle: {
    display: 'flex',
    border: `1px solid ${theme.colors.border}`,
    borderRadius: theme.radius.md,
    overflow: 'hidden',
  },
  toggleActive: {
    background: theme.colors.primary,
    color: '#fff',
    border: 'none',
    padding: '6px 16px',
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    fontWeight: 600,
    cursor: 'pointer',
  },
  toggleInactive: {
    background: 'transparent',
    color: theme.colors.textMuted,
    border: 'none',
    padding: '6px 16px',
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    cursor: 'pointer',
  },
  sidebar: {
    display: 'flex',
    flexDirection: 'column',
    gap: theme.spacing.md,
  },
  sideCard: {
    background: theme.colors.card,
    border: `1px solid ${theme.colors.border}`,
    borderRadius: theme.radius.lg,
    padding: theme.spacing.lg,
    boxShadow: theme.shadow.sm,
  },
  sideCardTitle: {
    fontFamily: theme.fonts.serif,
    fontSize: '14px',
    color: theme.colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    margin: `0 0 ${theme.spacing.md}`,
  },
  recommendedCard: {
    background: theme.colors.accentLight,
    borderRadius: theme.radius.md,
    padding: theme.spacing.md,
  },
  accentBtn: {
    background: theme.colors.accent,
    color: '#fff',
    border: 'none',
    borderRadius: theme.radius.md,
    padding: '8px 16px',
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    fontWeight: 600,
    cursor: 'pointer',
    width: '100%',
  },
}
