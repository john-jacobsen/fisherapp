import { useLocation, useNavigate, useParams } from 'react-router-dom';
import NavBar from '../components/NavBar';
import MasteryMeter from '../components/MasteryMeter';
import { theme } from '../theme';

export default function ScoreReport() {
  const { nodeId } = useParams();
  const navigate = useNavigate();
  const { state } = useLocation();

  const mastery = state?.mastery ?? 0;
  const questionsAnswered = state?.questionsAnswered ?? 0;
  const correct = state?.correct ?? [];
  const correctCount = correct.filter(Boolean).length;
  const accuracy = questionsAnswered > 0 ? correctCount / questionsAnswered : 0;
  const mastered = mastery >= 0.85;

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 600, margin: '0 auto', padding: '48px 24px', fontFamily: theme.fonts.sans, textAlign: 'center' }}>
        {/* Result badge */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ fontSize: 56, marginBottom: 12 }}>
            {mastered ? '🎉' : '📚'}
          </div>
          <h1 style={{ margin: '0 0 8px', fontSize: 30, fontWeight: 700, color: theme.colors.text }}>
            {mastered ? 'Node Mastered!' : 'Practice Complete'}
          </h1>
          <p style={{ margin: 0, color: theme.colors.textSecondary, fontSize: 15 }}>
            {mastered
              ? 'Great work! This skill is now in your mastered set.'
              : 'Keep practicing to reach mastery (85%).'}
          </p>
        </div>

        {/* Stats grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
          <div style={{ padding: '20px 16px', background: theme.colors.surface, borderRadius: theme.radius.lg, boxShadow: theme.shadow.sm, border: `1px solid ${theme.colors.border}` }}>
            <div style={{ fontSize: 28, fontWeight: 700, color: theme.colors.text, marginBottom: 4 }}>{questionsAnswered}</div>
            <div style={{ fontSize: 12, color: theme.colors.textSecondary }}>Questions</div>
          </div>
          <div style={{ padding: '20px 16px', background: theme.colors.surface, borderRadius: theme.radius.lg, boxShadow: theme.shadow.sm, border: `1px solid ${theme.colors.border}` }}>
            <div style={{ fontSize: 28, fontWeight: 700, color: theme.colors.text, marginBottom: 4 }}>{Math.round(accuracy * 100)}%</div>
            <div style={{ fontSize: 12, color: theme.colors.textSecondary }}>Accuracy</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '12px 16px', background: theme.colors.surface, borderRadius: theme.radius.lg, boxShadow: theme.shadow.sm, border: `1px solid ${theme.colors.border}` }}>
            <MasteryMeter mastery={mastery} size={64} label="" />
          </div>
        </div>

        {/* Mastery badge */}
        {mastered && (
          <div style={{ padding: '16px 24px', background: theme.colors.successLight, borderRadius: theme.radius.lg, marginBottom: 32, border: `1px solid ${theme.colors.success}` }}>
            <p style={{ margin: 0, color: theme.colors.success, fontWeight: 600, fontSize: 15 }}>
              ✓ This node is now part of your mastered set. New nodes may be unlocked on your knowledge map.
            </p>
          </div>
        )}

        {/* Action buttons */}
        <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
          <button
            onClick={() => navigate(`/practice/${nodeId}`)}
            style={{
              padding: '12px 24px', background: theme.colors.surfaceAlt,
              border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
              cursor: 'pointer', fontSize: 14, fontFamily: theme.fonts.sans, color: theme.colors.text,
            }}
          >
            Practice Again
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            style={{
              padding: '12px 28px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
              fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
            }}
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </>
  );
}
