import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { theme } from '../theme.js'

const STATUS_COLORS = {
  mastered: theme.colors.primary,
  ready: theme.colors.accent,
  practicing: theme.colors.practicing,
  locked: theme.colors.locked,
}

const TOPIC_COLORS = {
  'Fractions': '#6B8E6B',
  'Exponents': '#8E6B6B',
  'Order of Operations': '#6B7A8E',
  'Equations': '#8E7B6B',
  'Logarithms': '#6B8E82',
  'Summation': '#7B6B8E',
  'Combinatorics': '#8E876B',
  'Geometric Series': '#6B858E',
}

const NODE_WIDTH = 120
const NODE_HEIGHT = 44
const CANVAS_PADDING = 40

export default function KnowledgeGraph({ nodes, edges, onNodeClick }) {
  const [hoveredNode, setHoveredNode] = useState(null)
  const navigate = useNavigate()

  if (!nodes || nodes.length === 0) {
    return <div style={{ padding: 40, color: theme.colors.textMuted }}>Loading knowledge map…</div>
  }

  // Compute canvas bounds
  const maxX = Math.max(...nodes.map(n => (n.display_x || 0) + NODE_WIDTH)) + CANVAS_PADDING
  const maxY = Math.max(...nodes.map(n => (n.display_y || 0) + NODE_HEIGHT)) + CANVAS_PADDING

  const handleClick = (node) => {
    if (node.status === 'locked') return
    if (onNodeClick) onNodeClick(node)
    else navigate(`/lesson/${node.id}`)
  }

  // Build node lookup for edge rendering
  const nodeMap = {}
  nodes.forEach(n => { nodeMap[n.id] = n })

  return (
    <div style={{ overflowX: 'auto', overflowY: 'auto', maxHeight: '600px', border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.lg, background: theme.colors.bg }}>
      <div style={{ position: 'relative', width: maxX, height: maxY, minWidth: '100%' }}>
        {/* SVG edges layer */}
        <svg
          style={{ position: 'absolute', top: 0, left: 0, width: maxX, height: maxY, pointerEvents: 'none' }}
          viewBox={`0 0 ${maxX} ${maxY}`}
        >
          <defs>
            <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" fill={theme.colors.border} />
            </marker>
          </defs>
          {edges.map((edge, i) => {
            const from = nodeMap[edge.from_node_id]
            const to = nodeMap[edge.to_node_id]
            if (!from || !to) return null

            const x1 = (from.display_x || 0) + NODE_WIDTH
            const y1 = (from.display_y || 0) + NODE_HEIGHT / 2
            const x2 = to.display_x || 0
            const y2 = (to.display_y || 0) + NODE_HEIGHT / 2
            const cx1 = x1 + 30
            const cx2 = x2 - 30

            const isHighlighted = hoveredNode &&
              (edge.from_node_id === hoveredNode || edge.to_node_id === hoveredNode)

            return (
              <path
                key={i}
                d={`M ${x1} ${y1} C ${cx1} ${y1}, ${cx2} ${y2}, ${x2} ${y2}`}
                fill="none"
                stroke={isHighlighted ? theme.colors.primary : theme.colors.border}
                strokeWidth={isHighlighted ? 2 : 1.5}
                markerEnd="url(#arrowhead)"
                opacity={isHighlighted ? 1 : 0.6}
              />
            )
          })}
        </svg>

        {/* Node boxes */}
        {nodes.map(node => {
          const x = node.display_x || 0
          const y = node.display_y || 0
          const statusColor = STATUS_COLORS[node.status] || theme.colors.locked
          const isHovered = hoveredNode === node.id
          const isClickable = node.status !== 'locked'

          return (
            <div
              key={node.id}
              onClick={() => handleClick(node)}
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              title={node.status === 'locked' ? `${node.label} — prerequisites not met` : node.label}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: NODE_WIDTH,
                height: NODE_HEIGHT,
                background: node.status === 'mastered' ? theme.colors.primaryLight
                  : node.status === 'ready' ? theme.colors.accentLight
                  : '#F5F4F2',
                border: `2px solid ${statusColor}`,
                borderRadius: theme.radius.md,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: isClickable ? 'pointer' : 'not-allowed',
                padding: '4px 8px',
                boxShadow: isHovered && isClickable ? theme.shadow.md : theme.shadow.sm,
                transform: isHovered && isClickable ? 'scale(1.03)' : 'scale(1)',
                transition: 'all 0.15s ease',
                zIndex: isHovered ? 10 : 1,
                opacity: node.status === 'locked' ? 0.6 : 1,
              }}
            >
              <span style={{
                fontFamily: theme.fonts.sans,
                fontSize: '11px',
                fontWeight: node.status === 'mastered' || node.status === 'ready' ? 600 : 400,
                color: node.status === 'mastered' ? theme.colors.primary
                  : node.status === 'ready' ? '#8B6914'
                  : theme.colors.textMuted,
                textAlign: 'center',
                lineHeight: '1.3',
                overflow: 'hidden',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
              }}>
                {node.label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
