import { useState } from 'react';
import { theme } from '../theme';
import MathDisplay from './MathDisplay';

export default function HintPanel({
  hints = [],
  loading = false,
  onOpen = null,
  aiConfig = null,
  onAiHint = null,
  visible = true,
}) {
  const [revealed, setRevealed] = useState(0);
  const [aiHint, setAiHint] = useState(null);
  const [loadingAi, setLoadingAi] = useState(false);
  const [open, setOpen] = useState(false);
  const [opened, setOpened] = useState(false);

  if (!visible) return null;

  const toggleOpen = () => {
    const next = !open;
    setOpen(next);
    if (next && !opened) {
      setOpened(true);
      if (onOpen) onOpen();
    }
  };

  const revealNext = () => setRevealed(r => Math.min(r + 1, hints.length));

  const requestAiHint = async () => {
    if (!aiConfig || !onAiHint) return;
    setLoadingAi(true);
    try {
      const result = await onAiHint();
      setAiHint(result);
    } catch {
      setAiHint('Could not load AI hint. Check your API key in Settings.');
    } finally {
      setLoadingAi(false);
    }
  };

  const totalHints = hints.length;
  const hasMore = revealed < totalHints;

  // Determine status message when panel is open and no hints revealed
  let emptyMessage = null;
  if (totalHints === 0) {
    if (loading) {
      emptyMessage = 'Loading hints…';
    } else {
      emptyMessage = 'No hints available for this problem.';
    }
  }

  return (
    <div style={{ border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md, overflow: 'hidden', marginTop: 16 }}>
      <button
        onClick={toggleOpen}
        style={{
          width: '100%', padding: '10px 16px', background: theme.colors.surfaceAlt,
          border: 'none', cursor: 'pointer', display: 'flex', justifyContent: 'space-between',
          alignItems: 'center', fontSize: 14, color: theme.colors.text, fontFamily: theme.fonts.sans,
        }}
      >
        <span>💡 Hints {totalHints > 0 ? `(${Math.min(revealed, totalHints)}/${totalHints})` : ''}</span>
        <span>{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div style={{ padding: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
          {hints.slice(0, revealed).map((h, i) => (
            <div key={i} style={{
              padding: '10px 14px', background: theme.colors.accentLight,
              borderRadius: theme.radius.sm, fontSize: 14, color: theme.colors.text,
              borderLeft: `3px solid ${theme.colors.accent}`,
              fontFamily: theme.fonts.sans, lineHeight: 1.6,
            }}>
              <strong>Hint {i + 1}:</strong>{' '}
              <MathDisplay content={h.text || (typeof h === 'string' ? h : '')} />
            </div>
          ))}

          {emptyMessage && (
            <p style={{ margin: 0, fontSize: 13, color: theme.colors.textSecondary }}>
              {emptyMessage}
            </p>
          )}

          {totalHints > 0 && hints.slice(0, revealed).length === 0 && (
            <button onClick={revealNext} style={{
              padding: '8px 16px', background: theme.colors.surface,
              border: `1px solid ${theme.colors.accent}`, borderRadius: theme.radius.sm,
              cursor: 'pointer', color: theme.colors.accent, fontSize: 13, fontFamily: theme.fonts.sans,
            }}>
              Show first hint (1/{totalHints})
            </button>
          )}

          {totalHints > 0 && revealed > 0 && hasMore && (
            <button onClick={revealNext} style={{
              padding: '8px 16px', background: theme.colors.surface,
              border: `1px solid ${theme.colors.accent}`, borderRadius: theme.radius.sm,
              cursor: 'pointer', color: theme.colors.accent, fontSize: 13, fontFamily: theme.fonts.sans,
            }}>
              Show next hint ({revealed + 1}/{totalHints})
            </button>
          )}

          {aiConfig && (
            <div style={{ borderTop: `1px solid ${theme.colors.border}`, paddingTop: 12, marginTop: 4 }}>
              {aiHint ? (
                <div style={{
                  padding: '10px 14px', background: theme.colors.primaryLight,
                  borderRadius: theme.radius.sm, fontSize: 14, color: theme.colors.text,
                  borderLeft: `3px solid ${theme.colors.primary}`,
                  fontFamily: theme.fonts.sans, lineHeight: 1.6,
                }}>
                  <strong>AI Hint:</strong> {aiHint}
                </div>
              ) : (
                <button onClick={requestAiHint} disabled={loadingAi} style={{
                  padding: '8px 16px', background: theme.colors.primaryLight,
                  border: `1px solid ${theme.colors.primary}`, borderRadius: theme.radius.sm,
                  cursor: loadingAi ? 'not-allowed' : 'pointer', color: theme.colors.primary,
                  fontSize: 13, fontFamily: theme.fonts.sans, opacity: loadingAi ? 0.7 : 1,
                }}>
                  {loadingAi ? 'Asking AI…' : 'Ask AI for a hint'}
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
