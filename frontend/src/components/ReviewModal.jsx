import { useState } from 'react';
import { theme } from '../theme';

export default function ReviewModal({ count, onClose, onReviewNow }) {
  const [step, setStep] = useState(1);

  if (!count || count === 0) return null;

  const overlayStyle = {
    position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.4)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    zIndex: 1000, padding: 20,
  };

  const modalStyle = {
    background: theme.colors.surface, borderRadius: theme.radius.xl,
    padding: '32px', maxWidth: 420, width: '100%',
    boxShadow: theme.shadow.lg, fontFamily: theme.fonts.sans,
  };

  if (step === 1) {
    return (
      <div style={overlayStyle} onClick={e => { if (e.target === e.currentTarget) onClose(); }}>
        <div style={modalStyle}>
          <div style={{ fontSize: 36, marginBottom: 12, textAlign: 'center' }}>🔔</div>
          <h2 style={{ margin: '0 0 12px', fontSize: 20, fontWeight: 700, textAlign: 'center', color: theme.colors.text }}>
            {count} Skill{count !== 1 ? 's' : ''} Due for Review
          </h2>
          <p style={{ margin: '0 0 24px', color: theme.colors.textSecondary, lineHeight: 1.6, textAlign: 'center', fontSize: 14 }}>
            Reviewing now takes ~{Math.ceil(count * 1.5)} minutes and keeps your progress solid.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <button
              onClick={onReviewNow}
              style={{
                padding: '12px', background: theme.colors.primary, color: '#fff',
                border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
                fontSize: 14, fontWeight: 600,
              }}
            >
              Review Now (~{Math.ceil(count * 1.5)} min)
            </button>
            <button
              onClick={() => setStep(2)}
              style={{
                padding: '12px', background: theme.colors.surfaceAlt,
                border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                cursor: 'pointer', fontSize: 14, color: theme.colors.text,
              }}
            >
              Remind Me Later
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={overlayStyle}>
      <div style={modalStyle}>
        <div style={{ fontSize: 36, marginBottom: 12, textAlign: 'center' }}>⚠️</div>
        <h2 style={{ margin: '0 0 12px', fontSize: 20, fontWeight: 700, textAlign: 'center', color: theme.colors.text }}>
          Skipping Reviews Has Consequences
        </h2>
        <p style={{ margin: '0 0 24px', color: theme.colors.textSecondary, lineHeight: 1.6, textAlign: 'center', fontSize: 14 }}>
          If a review is overdue by more than 7 days, the skill may drop back to "needs practice." Skills you skip reviewing can fade.
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <button
            onClick={onReviewNow}
            style={{
              padding: '12px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
              fontSize: 14, fontWeight: 600,
            }}
          >
            OK, I'll Review Now
          </button>
          <button
            onClick={onClose}
            style={{
              padding: '12px', background: theme.colors.surfaceAlt,
              border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
              cursor: 'pointer', fontSize: 14, color: theme.colors.textSecondary,
            }}
          >
            Skip for Now
          </button>
        </div>
      </div>
    </div>
  );
}
