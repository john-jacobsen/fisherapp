import { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { theme } from '../theme.js'
import HIERARCHY from '../data/hierarchy.json'

const STATUS_COLORS = {
  mastered: theme.colors.primary,
  ready: theme.colors.accent,
  practicing: theme.colors.practicing,
  locked: theme.colors.locked,
  available: theme.colors.locked,
}

const NODE_W = 130
const NODE_H = 44
const TOPIC_W = 160
const TOPIC_H = 80
const PAD = 40
const TOPIC_GAP = 20
const TOPICS_PER_ROW = 4

// Static subject/topic definitions — node IDs are matched against HIERARCHY.items at runtime
const SUBJECT_DEFS = [
  {
    id: 'foundations', name: 'Foundations',
    description: 'Fractions, equations, exponents, and series fundamentals',
    hasContent: true,
    topicDefs: [
      { id: 'fractions',    name: 'Fractions',            prefix: 'frac-' },
      { id: 'order-ops',    name: 'Order of Operations',  prefix: 'order-' },
      { id: 'exponents',    name: 'Exponents',            prefix: 'exp-' },
      { id: 'equations',    name: 'Equations',            prefix: 'eq-' },
      { id: 'logarithms',   name: 'Logarithms',           prefix: 'log-' },
      { id: 'summations',   name: 'Summations',           prefix: 'sum-' },
      { id: 'combinatorics',name: 'Combinatorics',        prefix: 'comb-' },
      { id: 'geometric',    name: 'Geometric Series',     prefix: 'geo-' },
    ],
  },
  {
    id: 'algebra', name: 'Algebra',
    description: 'Linear, polynomial, and pre-calculus algebra',
    hasContent: true,
    topicDefs: [
      { id: 'alg-linear', name: 'Linear & Systems',   nodeIds: ['alg-linear-graphs','alg-slope','alg-systems-sub','alg-systems-elim','alg-inequalities'] },
      { id: 'alg-poly',   name: 'Polynomials',         nodeIds: ['alg-poly-ops','alg-factoring-gcf','alg-factoring-quad','alg-completing-square'] },
      { id: 'alg-expr',   name: 'Expressions',         nodeIds: ['alg-rational-expr','alg-radical-simplify','alg-radical-equations'] },
      { id: 'precalc',    name: 'Pre-Calculus',         prefix: 'precalc-' },
    ],
  },
  {
    id: 'calculus', name: 'Calculus',
    description: 'Limits, derivatives, integrals, and multivariable calculus',
    hasContent: true,
    topicDefs: [
      { id: 'limits',       name: 'Limits',                nodeIds: ['calc-limits','calc-limit-laws','calc-continuity'] },
      { id: 'derivatives',  name: 'Derivatives',           nodeIds: ['calc-deriv-def','calc-deriv-power','calc-deriv-product','calc-deriv-chain','calc-deriv-exp-log','calc-implicit','calc-optim'] },
      { id: 'integrals',    name: 'Integrals',             nodeIds: ['calc-antideriv','calc-riemann','calc-ftc','calc-usub','calc-byparts','calc-improper','calc-series-conv'] },
      { id: 'multivariable',name: 'Multivariable',         prefix: 'mv-' },
    ],
  },
  {
    id: 'linalg', name: 'Linear Algebra',
    description: 'Vectors, matrices, and linear transformations',
    hasContent: true,
    topicDefs: [
      { id: 'linalg-matrices', name: 'Vectors & Matrices', nodeIds: ['linalg-vectors','linalg-matrix-ops','linalg-matrix-mult','linalg-transpose','linalg-row-reduce','linalg-determinant','linalg-inverse','linalg-linear-systems'] },
      { id: 'linalg-spaces',   name: 'Vector Spaces',      nodeIds: ['linalg-span-independence','linalg-subspaces','linalg-rank-nullity'] },
      { id: 'linalg-eigen',    name: 'Eigenvalues',        nodeIds: ['linalg-linear-transforms','linalg-change-basis','linalg-eigenvalues','linalg-diagonalization','linalg-symmetric-spectral'] },
      { id: 'linalg-ortho',    name: 'Orthogonality',      nodeIds: ['linalg-orthogonality','linalg-gram-schmidt','linalg-orthogonal-projection','linalg-least-squares','linalg-svd'] },
    ],
  },
  {
    id: 'probability', name: 'Probability',
    description: 'Sample spaces, random variables, and distributions',
    hasContent: true,
    topicDefs: [
      { id: 'prob-basics',     name: 'Probability Basics',  nodeIds: ['prob-sample-space','prob-set-ops','prob-axioms','prob-inclusion-excl','prob-area-probability','prob-conditional','prob-independence','prob-total-prob','prob-bayes'] },
      { id: 'prob-discrete',   name: 'Discrete RVs',        nodeIds: ['prob-discrete-rv','prob-expected-value','prob-indicators','prob-variance','prob-bernoulli-binom','prob-hypergeometric','prob-geometric-dist','prob-poisson','prob-poisson-approx'] },
      { id: 'prob-continuous', name: 'Continuous RVs',      nodeIds: ['prob-continuous-rv','prob-normal','prob-exponential-dist','prob-memoryless','prob-gamma-dist','prob-normal-approx','prob-cdf-method','prob-transformations','prob-inverse-cdf'] },
      { id: 'prob-joint',      name: 'Joint Distributions', nodeIds: ['prob-joint-discrete','prob-joint-continuous','prob-marginal','prob-conditional-dist','prob-covariance','prob-conditional-expect','prob-bivariate-normal'] },
      { id: 'prob-limits',     name: 'Limit Theorems',      nodeIds: ['prob-mgf','prob-poisson-process','prob-order-stats','prob-lln','prob-clt'] },
    ],
  },
  {
    id: 'statistics', name: 'Statistics',
    description: 'Estimation, hypothesis testing, and regression',
    hasContent: true,
    topicDefs: [
      { id: 'stat-estimation', name: 'Estimation',          nodeIds: ['stat-sampling-dist','stat-estimator-props','stat-survey-srs','stat-mom','stat-mle-univariate','stat-mle-multiparameter','stat-mle-properties','stat-sufficiency','stat-fisher-info','stat-crlb','stat-mvue','stat-delta-method','stat-bootstrap'] },
      { id: 'stat-ci',         name: 'Confidence Intervals',nodeIds: ['stat-ci-z','stat-ci-t','stat-ci-proportion'] },
      { id: 'stat-hyp',        name: 'Hypothesis Testing',  nodeIds: ['stat-hyp-setup','stat-errors-power','stat-pvalue','stat-neyman-pearson','stat-ump','stat-glrt','stat-power-sample-size'] },
      { id: 'stat-tests',      name: 'Statistical Tests',   nodeIds: ['stat-ztest-one','stat-ttest-one','stat-ttest-two','stat-pooled-variance','stat-ttest-paired','stat-mannwhitney','stat-wilcoxon-signed','stat-permutation','stat-chi-gof','stat-chi-indep','stat-chi-homog','stat-anova-one','stat-anova-kruskal','stat-multiple-testing'] },
      { id: 'stat-regression', name: 'Regression',          nodeIds: ['stat-slr','stat-slr-matrix','stat-slr-inference','stat-mlr','stat-mlr-inference','stat-model-comparison','stat-regression-checks'] },
      { id: 'stat-advanced',   name: 'Advanced Topics',     nodeIds: ['stat-bayes-posterior','stat-order-statistics','stat-simulation','stat-confounding','stat-causal-intro'] },
    ],
  },
]

// Build the subjects array from the flat HIERARCHY.items list
function buildSubjects() {
  const itemSet = new Set(HIERARCHY.items || [])
  return SUBJECT_DEFS.map(subj => ({
    id: subj.id,
    name: subj.name,
    description: subj.description,
    hasContent: subj.hasContent,
    topics: subj.topicDefs.map((td, i) => {
      const nodeIds = td.prefix
        ? (HIERARCHY.items || []).filter(id => id.startsWith(td.prefix))
        : (td.nodeIds || []).filter(id => itemSet.has(id))
      const col = i % TOPICS_PER_ROW
      const row = Math.floor(i / TOPICS_PER_ROW)
      return {
        id: td.id,
        name: td.name,
        nodeIds,
        display_x: PAD + col * (TOPIC_W + TOPIC_GAP),
        display_y: PAD + row * (TOPIC_H + TOPIC_GAP),
      }
    }),
  }))
}

const SUBJECTS = buildSubjects()

// Compute where an inter-topic edge should start/end based on relative positions
function getTopicEdgePoints(from, to) {
  const fromCX = from.display_x + TOPIC_W / 2
  const fromCY = from.display_y + TOPIC_H / 2
  const toCX = to.display_x + TOPIC_W / 2
  const toCY = to.display_y + TOPIC_H / 2
  const dx = toCX - fromCX
  const dy = toCY - fromCY

  let x1, y1, x2, y2
  if (Math.abs(dx) >= Math.abs(dy)) {
    if (dx >= 0) {
      x1 = from.display_x + TOPIC_W; y1 = fromCY
      x2 = to.display_x; y2 = toCY
    } else {
      x1 = from.display_x; y1 = fromCY
      x2 = to.display_x + TOPIC_W; y2 = toCY
    }
  } else {
    if (dy >= 0) {
      x1 = fromCX; y1 = from.display_y + TOPIC_H
      x2 = toCX; y2 = to.display_y
    } else {
      x1 = fromCX; y1 = from.display_y
      x2 = toCX; y2 = to.display_y + TOPIC_H
    }
  }
  return { x1, y1, x2, y2 }
}

function Breadcrumb({ items }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 16, fontFamily: theme.fonts.sans, fontSize: 13 }}>
      {items.map((item, i) => (
        <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          {i > 0 && <span style={{ color: theme.colors.textMuted, userSelect: 'none' }}>›</span>}
          {item.onClick ? (
            <button
              onClick={item.onClick}
              style={{ background: 'none', border: 'none', padding: 0, cursor: 'pointer', color: theme.colors.primary, fontFamily: theme.fonts.sans, fontSize: 13, fontWeight: 500 }}
            >
              {item.label}
            </button>
          ) : (
            <span style={{ color: theme.colors.text, fontWeight: 600 }}>{item.label}</span>
          )}
        </span>
      ))}
    </div>
  )
}

export default function KnowledgeGraph({ nodes, edges, onNodeClick }) {
  const navigate = useNavigate()
  const [level, setLevel] = useState('subject')
  const [activeSubject, setActiveSubject] = useState(null)
  const [activeTopic, setActiveTopic] = useState(null)

  // Build id → node lookup (with status from API)
  const nodeMap = useMemo(() => {
    const m = {}
    if (nodes) nodes.forEach(n => { m[n.id] = n })
    return m
  }, [nodes])

  // Build nodeId → topicId lookup from hierarchy
  const nodeTopicMap = useMemo(() => {
    const m = {}
    SUBJECTS.forEach(subj => {
      subj.topics.forEach(topic => {
        topic.nodeIds.forEach(nid => { m[nid] = topic.id })
      })
    })
    return m
  }, [])

  // Topic stats: mastered, ready, total, progress
  const topicStats = useMemo(() => {
    const stats = {}
    SUBJECTS.forEach(subj => {
      subj.topics.forEach(topic => {
        let mastered = 0, ready = 0, total = 0
        topic.nodeIds.forEach(nid => {
          const n = nodeMap[nid]
          if (n) {
            total++
            if (n.status === 'mastered') mastered++
            else if (n.status === 'ready') ready++
          }
        })
        stats[topic.id] = { mastered, ready, total, progress: total > 0 ? mastered / total : 0 }
      })
    })
    return stats
  }, [nodeMap])

  // Subject stats: aggregate from topics
  const subjectStats = useMemo(() => {
    const stats = {}
    SUBJECTS.forEach(subj => {
      let mastered = 0, ready = 0, total = 0
      subj.topics.forEach(t => {
        const s = topicStats[t.id] || {}
        mastered += s.mastered || 0
        ready += s.ready || 0
        total += s.total || 0
      })
      stats[subj.id] = { mastered, ready, total, progress: total > 0 ? mastered / total : 0 }
    })
    return stats
  }, [topicStats])

  // Derive unique inter-topic edges from node-level edges for a given subject
  const topicEdges = useMemo(() => {
    if (!edges || !activeSubject) return []
    const subjectTopicIds = new Set(activeSubject.topics.map(t => t.id))
    const seen = new Set()
    const result = []
    edges.forEach(e => {
      const fromTopic = nodeTopicMap[e.from_node_id]
      const toTopic = nodeTopicMap[e.to_node_id]
      if (!fromTopic || !toTopic || fromTopic === toTopic) return
      if (!subjectTopicIds.has(fromTopic) || !subjectTopicIds.has(toTopic)) return
      const key = `${fromTopic}→${toTopic}`
      if (!seen.has(key)) {
        seen.add(key)
        result.push({ from: fromTopic, to: toTopic })
      }
    })
    return result
  }, [edges, activeSubject, nodeTopicMap])

  if (!nodes || nodes.length === 0) {
    return <div style={{ padding: 40, color: theme.colors.textMuted, fontFamily: theme.fonts.sans }}>Loading knowledge map…</div>
  }

  // ── LEVEL 1: SUBJECT VIEW ─────────────────────────────────────────────────
  if (level === 'subject') {
    return (
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16 }}>
        {SUBJECTS.map(subj => {
          const stats = subjectStats[subj.id] || {}
          const active = subj.hasContent
          const allMastered = active && stats.mastered > 0 && stats.mastered === stats.total
          const hasReady = active && stats.ready > 0
          const subjBg = !active ? '#F5F4F2'
            : allMastered ? theme.colors.primaryLight
            : hasReady ? theme.colors.accentLight
            : theme.colors.primaryLight
          const subjBorder = !active ? theme.colors.border
            : allMastered ? theme.colors.primary
            : hasReady ? theme.colors.accent
            : theme.colors.primary
          const subjTitleColor = !active ? theme.colors.textMuted
            : hasReady && !allMastered ? '#7A5C00'
            : theme.colors.primary
          return (
            <div
              key={subj.id}
              onClick={() => active && (setActiveSubject(subj), setLevel('topic'))}
              style={{
                width: 200, padding: '20px 24px', boxSizing: 'border-box',
                background: subjBg,
                border: `2px solid ${subjBorder}`,
                borderRadius: theme.radius.lg,
                cursor: active ? 'pointer' : 'default',
                opacity: active ? 1 : 0.55,
                transition: 'all 0.15s',
                boxShadow: active ? theme.shadow.sm : 'none',
              }}
            >
              <div style={{ fontFamily: theme.fonts.serif, fontSize: 18, fontWeight: 700, color: subjTitleColor, marginBottom: 6 }}>
                {subj.name}
              </div>
              <div style={{ fontFamily: theme.fonts.sans, fontSize: 12, color: theme.colors.textMuted, marginBottom: 10, lineHeight: 1.4 }}>
                {subj.description}
              </div>
              {active ? (
                <>
                  <div style={{ fontFamily: theme.fonts.sans, fontSize: 12, color: theme.colors.textMuted, marginBottom: 6 }}>
                    {stats.mastered || 0} / {stats.total || 0} skills mastered
                  </div>
                  <div style={{ height: 4, background: theme.colors.border, borderRadius: 2, marginBottom: 12 }}>
                    <div style={{ height: '100%', width: `${(stats.progress || 0) * 100}%`, background: theme.colors.primary, borderRadius: 2, transition: 'width 0.4s' }} />
                  </div>
                  <div style={{ fontFamily: theme.fonts.sans, fontSize: 12, color: subjTitleColor, fontWeight: 600 }}>
                    {hasReady && !allMastered ? `${stats.ready} ready to learn →` : 'Explore topics →'}
                  </div>
                </>
              ) : (
                <div style={{ fontFamily: theme.fonts.sans, fontSize: 12, color: theme.colors.textMuted, fontStyle: 'italic' }}>
                  Coming soon
                </div>
              )}
            </div>
          )
        })}
      </div>
    )
  }

  // ── LEVEL 2: TOPIC VIEW ───────────────────────────────────────────────────
  if (level === 'topic') {
    const topics = activeSubject.topics
    const topicById = {}
    topics.forEach(t => { topicById[t.id] = t })
    const maxX = Math.max(...topics.map(t => t.display_x + TOPIC_W)) + PAD
    const maxY = Math.max(...topics.map(t => t.display_y + TOPIC_H)) + PAD

    return (
      <div>
        <Breadcrumb items={[
          { label: 'All Subjects', onClick: () => { setLevel('subject'); setActiveSubject(null) } },
          { label: activeSubject.name },
        ]} />
        <div style={{ overflowX: 'auto', overflowY: 'auto', maxHeight: 520, border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.lg, background: theme.colors.bg }}>
          <div style={{ position: 'relative', width: maxX, height: maxY, minWidth: '100%' }}>
            <svg style={{ position: 'absolute', top: 0, left: 0, width: maxX, height: maxY, pointerEvents: 'none' }} viewBox={`0 0 ${maxX} ${maxY}`}>
              <defs>
                <marker id="topic-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                  <polygon points="0 0, 8 3, 0 6" fill={theme.colors.border} />
                </marker>
              </defs>
              {topicEdges.map((edge, i) => {
                const from = topicById[edge.from]
                const to = topicById[edge.to]
                if (!from || !to) return null
                const { x1, y1, x2, y2 } = getTopicEdgePoints(from, to)
                const cx1 = x1 + (x2 - x1) * 0.4
                const cy1 = y1
                const cx2 = x1 + (x2 - x1) * 0.6
                const cy2 = y2
                return (
                  <path key={i}
                    d={`M ${x1} ${y1} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${x2} ${y2}`}
                    fill="none" stroke={theme.colors.border} strokeWidth={1.5}
                    markerEnd="url(#topic-arrow)" opacity={0.7}
                  />
                )
              })}
            </svg>

            {topics.map(topic => {
              const stats = topicStats[topic.id] || {}
              const allMastered = stats.mastered > 0 && stats.mastered === stats.total
              const hasProgress = stats.mastered > 0 || stats.ready > 0
              const borderColor = allMastered ? theme.colors.primary : hasProgress ? theme.colors.accent : theme.colors.border
              const bgColor = allMastered ? theme.colors.primaryLight : hasProgress ? theme.colors.accentLight : '#F5F4F2'

              return (
                <div
                  key={topic.id}
                  onClick={() => { setActiveTopic(topic); setLevel('skill') }}
                  style={{
                    position: 'absolute',
                    left: topic.display_x,
                    top: topic.display_y,
                    width: TOPIC_W,
                    height: TOPIC_H,
                    background: bgColor,
                    border: `2px solid ${borderColor}`,
                    borderRadius: theme.radius.md,
                    cursor: 'pointer',
                    padding: '10px 12px',
                    boxSizing: 'border-box',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    transition: 'all 0.15s',
                    boxShadow: theme.shadow.sm,
                  }}
                >
                  <div style={{ fontFamily: theme.fonts.sans, fontSize: 12, fontWeight: 600, color: theme.colors.text, lineHeight: 1.3 }}>
                    {topic.name}
                  </div>
                  <div>
                    <div style={{ fontFamily: theme.fonts.sans, fontSize: 10, color: theme.colors.textMuted, marginBottom: 4 }}>
                      {stats.mastered || 0} / {stats.total || 0} mastered
                    </div>
                    <div style={{ height: 3, background: theme.colors.border, borderRadius: 2 }}>
                      <div style={{ height: '100%', width: `${(stats.progress || 0) * 100}%`, background: theme.colors.primary, borderRadius: 2 }} />
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  // ── LEVEL 3: SUB-SKILL VIEW ───────────────────────────────────────────────
  if (level === 'skill') {
    const topicNodeIds = new Set(activeTopic.nodeIds)
    const topicNodes = nodes.filter(n => topicNodeIds.has(n.id))
    const topicEdgeList = (edges || []).filter(e => topicNodeIds.has(e.from_node_id) && topicNodeIds.has(e.to_node_id))

    const nodeMapL3 = {}
    topicNodes.forEach(n => { nodeMapL3[n.id] = n })

    const xs = topicNodes.map(n => n.display_x || 0)
    const ys = topicNodes.map(n => n.display_y || 0)
    const minX = Math.min(...xs)
    const minY = Math.min(...ys)
    const norm = (v, min) => (v || 0) - min + PAD

    const canvasW = Math.max(...topicNodes.map(n => norm(n.display_x, minX) + NODE_W)) + PAD
    const canvasH = Math.max(...topicNodes.map(n => norm(n.display_y, minY) + NODE_H)) + PAD

    return (
      <div>
        <Breadcrumb items={[
          { label: 'All Subjects', onClick: () => { setLevel('subject'); setActiveSubject(null); setActiveTopic(null) } },
          { label: activeSubject.name, onClick: () => { setLevel('topic'); setActiveTopic(null) } },
          { label: activeTopic.name },
        ]} />
        <div style={{ overflowX: 'auto', overflowY: 'auto', maxHeight: 540, border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.lg, background: theme.colors.bg }}>
          <div style={{ position: 'relative', width: Math.max(canvasW, 400), height: Math.max(canvasH, 180), minWidth: '100%' }}>
            <svg
              style={{ position: 'absolute', top: 0, left: 0, width: Math.max(canvasW, 400), height: Math.max(canvasH, 180), pointerEvents: 'none' }}
              viewBox={`0 0 ${Math.max(canvasW, 400)} ${Math.max(canvasH, 180)}`}
            >
              <defs>
                <marker id="skill-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                  <polygon points="0 0, 8 3, 0 6" fill={theme.colors.border} />
                </marker>
              </defs>
              {topicEdgeList.map((edge, i) => {
                const from = nodeMapL3[edge.from_node_id]
                const to = nodeMapL3[edge.to_node_id]
                if (!from || !to) return null
                const x1 = norm(from.display_x, minX) + NODE_W
                const y1 = norm(from.display_y, minY) + NODE_H / 2
                const x2 = norm(to.display_x, minX)
                const y2 = norm(to.display_y, minY) + NODE_H / 2
                return (
                  <path key={i}
                    d={`M ${x1} ${y1} C ${x1 + 30} ${y1}, ${x2 - 30} ${y2}, ${x2} ${y2}`}
                    fill="none" stroke={theme.colors.border} strokeWidth={1.5}
                    markerEnd="url(#skill-arrow)" opacity={0.65}
                  />
                )
              })}
            </svg>

            {topicNodes.map(node => {
              const x = norm(node.display_x, minX)
              const y = norm(node.display_y, minY)
              const statusColor = STATUS_COLORS[node.status] || STATUS_COLORS.available
              const isAvailable = node.status === 'available' || node.status === 'locked'

              return (
                <div
                  key={node.id}
                  onClick={() => {
                    if (onNodeClick) onNodeClick(node)
                    else navigate(`/lesson/${node.id}`)
                  }}
                  title={isAvailable ? `${node.label} — prerequisites not yet met` : node.label}
                  style={{
                    position: 'absolute', left: x, top: y,
                    width: NODE_W, height: NODE_H,
                    background: node.status === 'mastered' ? theme.colors.primaryLight
                      : node.status === 'ready' ? theme.colors.accentLight : '#F5F4F2',
                    border: `2px ${isAvailable ? 'dashed' : 'solid'} ${statusColor}`,
                    borderRadius: theme.radius.md,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    cursor: 'pointer',
                    padding: '4px 8px', boxSizing: 'border-box',
                    opacity: isAvailable ? 0.7 : 1,
                    transition: 'all 0.15s',
                    boxShadow: theme.shadow.sm,
                  }}
                >
                  <span style={{
                    fontFamily: theme.fonts.sans, fontSize: '11px',
                    fontWeight: node.status === 'mastered' || node.status === 'ready' ? 600 : 400,
                    color: node.status === 'mastered' ? theme.colors.primary
                      : node.status === 'ready' ? '#8B6914' : theme.colors.textMuted,
                    textAlign: 'center', lineHeight: '1.3',
                    overflow: 'hidden', display: '-webkit-box',
                    WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
                  }}>
                    {node.label}
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  return null
}
