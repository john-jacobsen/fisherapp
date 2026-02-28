import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MathDisplay from '../components/MathDisplay';
import { theme } from '../theme';

export default function WorkedExamplesPage() {
  const { nodeId } = useParams();
  const navigate = useNavigate();
  const [examples, setExamples] = useState([]);
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [openIdx, setOpenIdx] = useState(0);

  useEffect(() => {
    Promise.all([
      api.get(`/lessons/${nodeId}`),
      api.get(`/lessons/${nodeId}/examples`),
    ]).then(([lessonRes, exRes]) => {
      // lessonRes.data has { node, lesson, worked_examples, ... }
      setTitle(lessonRes.data.node?.label || '');
      // exRes.data has { worked_examples: [...] }
      const exList = exRes.data.worked_examples || exRes.data || [];
      setExamples(exList);
    }).catch(() => {}).finally(() => setLoading(false));
  }, [nodeId]);

  if (loading) return (
    <>
      <NavBar />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh', fontFamily: theme.fonts.sans, color: theme.colors.textSecondary }}>
        Loading…
      </div>
    </>
  );

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
        <div style={{ marginBottom: 24, fontSize: 13, color: theme.colors.textSecondary }}>
          <Link to="/dashboard" style={{ color: theme.colors.primary, textDecoration: 'none' }}>Dashboard</Link>
          {' › '}
          <Link to={`/lesson/${nodeId}`} style={{ color: theme.colors.primary, textDecoration: 'none' }}>{title}</Link>
          {' › Worked Examples'}
        </div>

        <h1 style={{ margin: '0 0 8px', fontSize: 26, fontWeight: 700, color: theme.colors.text }}>
          Worked Examples
        </h1>
        <p style={{ margin: '0 0 28px', color: theme.colors.textSecondary, fontSize: 14 }}>
          {examples.length} example{examples.length !== 1 ? 's' : ''} for {title}
        </p>

        {examples.length === 0 && (
          <div style={{ padding: '40px', textAlign: 'center', color: theme.colors.textSecondary, background: theme.colors.surfaceAlt, borderRadius: theme.radius.lg }}>
            No worked examples yet.
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {examples.map((ex, i) => {
            // API returns { id, problem_text, steps }
            // steps is a list (could be strings or objects)
            const steps = Array.isArray(ex.steps) ? ex.steps : [];
            return (
              <div key={ex.id || i} style={{ border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.lg, overflow: 'hidden', boxShadow: theme.shadow.sm }}>
                <button
                  onClick={() => setOpenIdx(openIdx === i ? -1 : i)}
                  style={{
                    width: '100%', padding: '16px 20px', background: openIdx === i ? theme.colors.primaryLight : theme.colors.surface,
                    border: 'none', cursor: 'pointer', display: 'flex', justifyContent: 'space-between',
                    alignItems: 'center', fontFamily: theme.fonts.sans,
                  }}
                >
                  <span style={{ fontWeight: 600, fontSize: 15, color: theme.colors.text }}>
                    Example {i + 1}
                  </span>
                  <span style={{ color: theme.colors.textSecondary }}>{openIdx === i ? '▲' : '▼'}</span>
                </button>

                {openIdx === i && (
                  <div style={{ padding: '20px 24px', borderTop: `1px solid ${theme.colors.border}` }}>
                    <div style={{ marginBottom: 16 }}>
                      <h4 style={{ margin: '0 0 8px', color: theme.colors.textSecondary, fontSize: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Problem</h4>
                      <p style={{ margin: 0, fontSize: 15, lineHeight: 1.7, color: theme.colors.text }}>
                        <MathDisplay content={ex.problem_text || ''} />
                      </p>
                    </div>

                    {steps.length > 0 && (
                      <div>
                        <h4 style={{ margin: '0 0 8px', color: theme.colors.textSecondary, fontSize: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Steps</h4>
                        <ol style={{ margin: 0, paddingLeft: 20, display: 'flex', flexDirection: 'column', gap: 8 }}>
                          {steps.map((step, j) => {
                            const stepText = typeof step === 'string' ? step : (step.text || step.explanation || JSON.stringify(step));
                            const stepResult = typeof step === 'object' ? (step.result || '') : '';
                            return (
                              <li key={j} style={{ fontSize: 14, lineHeight: 1.7, color: theme.colors.text, marginBottom: 4 }}>
                                <MathDisplay content={stepText} />
                                {stepResult && (
                                  <div style={{
                                    marginTop: 4, paddingLeft: 12,
                                    borderLeft: `2px solid ${theme.colors.accent}`,
                                    color: theme.colors.textSecondary, fontSize: 13,
                                  }}>
                                    <MathDisplay content={stepResult} />
                                  </div>
                                )}
                              </li>
                            );
                          })}
                        </ol>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div style={{ marginTop: 32, display: 'flex', gap: 12 }}>
          <button
            onClick={() => navigate(`/lesson/${nodeId}`)}
            style={{
              padding: '11px 20px', background: theme.colors.surface,
              border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
              cursor: 'pointer', fontSize: 14, fontFamily: theme.fonts.sans, color: theme.colors.text,
            }}
          >
            ← Back to Lesson
          </button>
          <button
            onClick={() => navigate(`/practice/${nodeId}`)}
            style={{
              padding: '11px 24px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
              fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
            }}
          >
            Start Practice →
          </button>
        </div>
      </div>
    </>
  );
}
