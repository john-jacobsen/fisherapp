import { useNavigate } from 'react-router-dom'
import { theme } from '../theme.js'

const STATUS_LABEL = {
  mastered: 'Mastered',
  ready: 'Ready',
  practicing: 'In Progress',
  locked: 'Locked',
}

const STATUS_STYLE = {
  mastered: { background: theme.colors.primaryLight, color: theme.colors.primary, border: `1px solid ${theme.colors.primary}` },
  ready: { background: theme.colors.accentLight, color: '#8B6914', border: `1px solid ${theme.colors.accent}` },
  practicing: { background: '#E8F2FC', color: theme.colors.practicing, border: `1px solid ${theme.colors.practicing}` },
  locked: { background: '#F5F4F2', color: theme.colors.locked, border: `1px solid ${theme.colors.locked}` },
}

export default function KnowledgeList({ nodes }) {
  const navigate = useNavigate()

  // Group by topic
  const byTopic = {}
  nodes.forEach(node => {
    if (!byTopic[node.topic]) byTopic[node.topic] = []
    byTopic[node.topic].push(node)
  })

  const handleClick = (node) => {
    if (node.status !== 'locked') navigate(`/lesson/${node.id}`)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: theme.spacing.lg }}>
      {Object.entries(byTopic).map(([topic, topicNodes]) => (
        <div key={topic}>
          <h3 style={{
            fontFamily: theme.fonts.serif,
            fontSize: '16px',
            color: theme.colors.text,
            margin: `0 0 ${theme.spacing.sm}`,
            paddingBottom: theme.spacing.xs,
            borderBottom: `1px solid ${theme.colors.border}`,
          }}>
            {topic}
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {topicNodes.map(node => (
              <div
                key={node.id}
                onClick={() => handleClick(node)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: `${theme.spacing.sm} ${theme.spacing.md}`,
                  background: theme.colors.card,
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: theme.radius.md,
                  cursor: node.status !== 'locked' ? 'pointer' : 'default',
                  opacity: node.status === 'locked' ? 0.7 : 1,
                }}
              >
                <span style={{
                  fontFamily: theme.fonts.sans,
                  fontSize: '14px',
                  color: theme.colors.text,
                }}>
                  {node.label}
                </span>
                <span style={{
                  fontFamily: theme.fonts.sans,
                  fontSize: '12px',
                  fontWeight: 600,
                  padding: '3px 10px',
                  borderRadius: '20px',
                  ...STATUS_STYLE[node.status],
                }}>
                  {STATUS_LABEL[node.status] || node.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
