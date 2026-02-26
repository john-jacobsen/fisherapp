import { theme } from '../theme';

export default function ReviewBanner({ count, onDismiss }) {
  if (!count || count === 0) return null;

  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '14px 20px', background: theme.colors.warningLight,
      border: `1px solid ${theme.colors.warning}`, borderRadius: theme.radius.md,
      marginBottom: 20, flexWrap: 'wrap', gap: 10,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{ fontSize: 18 }}>🔔</span>
        <span style={{ fontSize: 14, color: theme.colors.text, fontFamily: theme.fonts.sans }}>
          <strong>{count} skill{count !== 1 ? 's' : ''}</strong> due for review
        </span>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <button
          onClick={onDismiss}
          style={{
            padding: '6px 12px', background: 'transparent',
            border: `1px solid ${theme.colors.warning}`, borderRadius: theme.radius.sm,
            cursor: 'pointer', fontSize: 12, color: theme.colors.textSecondary,
            fontFamily: theme.fonts.sans,
          }}
        >
          Later
        </button>
        <a
          href="/reviews"
          style={{
            padding: '6px 14px', background: theme.colors.warning, color: '#fff',
            borderRadius: theme.radius.sm, textDecoration: 'none',
            fontSize: 13, fontWeight: 600, fontFamily: theme.fonts.sans,
          }}
        >
          Review Now →
        </a>
      </div>
    </div>
  );
}
