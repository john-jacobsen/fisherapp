import { Link } from 'react-router-dom';
import { theme } from '../theme';

/**
 * Tiered, autonomy-supportive review banner (14-10):
 *   reminder   (0-2 days overdue) — dismissible, gentle nudge
 *   persistent (3-5 days overdue) — non-dismissible, firmer
 *   limit      (6+ days overdue)  — non-dismissible, explains the daily cap
 *
 * Copy stays transparent and non-punitive across every tier.
 */
export default function ReviewBanner({ enforcement, dismissed, onDismiss }) {
  if (!enforcement) return null;
  const { tier, overdue_count, daily_limit } = enforcement;
  if (tier === 'none' || !overdue_count) return null;
  if (tier === 'reminder' && dismissed) return null;

  const n = overdue_count;
  const plural = n !== 1 ? 's' : '';
  const dismissible = tier === 'reminder';

  const palette = tier === 'limit'
    ? { bg: '#FDECEC', border: '#E57373', text: '#B23B3B', icon: '⏳' }
    : tier === 'persistent'
    ? { bg: '#FFF3E0', border: '#E8961A', text: '#B86A00', icon: '🔔' }
    : { bg: theme.colors.warningLight, border: theme.colors.warning, text: theme.colors.text, icon: '🔔' };

  const message = tier === 'limit'
    ? `${n} review${plural} are more than 6 days overdue. New practice is capped at ${daily_limit}/day until you clear them — your reviews are always available and lift the cap right away.`
    : tier === 'persistent'
    ? `${n} review${plural} are a few days overdue. A quick review keeps these skills fresh before they slip.`
    : `${n} skill${plural} due for review.`;

  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '14px 20px', background: palette.bg,
      border: `1px solid ${palette.border}`, borderRadius: theme.radius.md,
      marginBottom: 20, flexWrap: 'wrap', gap: 10,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{ fontSize: 18 }}>{palette.icon}</span>
        <span style={{ fontSize: 14, color: palette.text, fontFamily: theme.fonts.sans, lineHeight: 1.5 }}>
          {message}
        </span>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        {dismissible && (
          <button
            onClick={onDismiss}
            style={{
              padding: '6px 12px', background: 'transparent',
              border: `1px solid ${palette.border}`, borderRadius: theme.radius.sm,
              cursor: 'pointer', fontSize: 12, color: theme.colors.textSecondary,
              fontFamily: theme.fonts.sans,
            }}
          >
            Later
          </button>
        )}
        <Link
          to="/reviews"
          style={{
            padding: '6px 14px', background: palette.border, color: '#fff',
            borderRadius: theme.radius.sm, textDecoration: 'none',
            fontSize: 13, fontWeight: 600, fontFamily: theme.fonts.sans,
          }}
        >
          {tier === 'limit' ? 'Do reviews →' : 'Review now →'}
        </Link>
      </div>
    </div>
  );
}
