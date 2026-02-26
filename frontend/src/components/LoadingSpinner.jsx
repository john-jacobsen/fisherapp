import { theme } from '../theme';

export default function LoadingSpinner({ message = 'Loading\u2026', fullPage = false }) {
  const content = (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16,
      color: theme.colors.textSecondary, fontFamily: theme.fonts.sans,
    }}>
      <div style={{
        width: 36, height: 36, borderRadius: '50%',
        border: `3px solid ${theme.colors.border}`,
        borderTopColor: theme.colors.primary,
        animation: 'spin 0.8s linear infinite',
      }} />
      <span style={{ fontSize: 14 }}>{message}</span>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  if (fullPage) {
    return (
      <div style={{
        display: 'flex', justifyContent: 'center', alignItems: 'center',
        minHeight: '60vh',
      }}>
        {content}
      </div>
    );
  }

  return content;
}
