import { theme } from '../theme';

export default function MasteryMeter({ mastery = 0, size = 80, label = 'Mastery' }) {
  const r = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(100, Math.max(0, Math.round(mastery * 100)));
  const offset = circ - (pct / 100) * circ;
  const color = pct >= 85 ? theme.colors.success : pct >= 50 ? theme.colors.accent : theme.colors.locked;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
      <svg width={size} height={size}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={theme.colors.border} strokeWidth={8} />
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none"
          stroke={color}
          strokeWidth={8}
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          style={{ transition: 'stroke-dashoffset 0.5s ease' }}
        />
        <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={theme.colors.text}
          style={{ fontSize: 14, fontWeight: 700, fontFamily: theme.fonts.sans }}>
          {pct}%
        </text>
      </svg>
      <span style={{ fontSize: 11, color: theme.colors.textSecondary, fontFamily: theme.fonts.sans }}>{label}</span>
    </div>
  );
}
