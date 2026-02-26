import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import api from '../api/client';
import NavBar from '../components/NavBar';
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
      setTitle(lessonRes.data.title);
      setExamples(exRes.data);
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
          {examples.map((ex, i) => (
            <div key={ex.id} style={{ border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.lg, overflow: 'hidden', boxShadow: theme.shadow.sm }}>
              <button
                onClick={() => setOpenIdx(openIdx === i ? -1 : i)}
                style={{
                  width: '100%', padding: '16px 20px', background: openIdx === i ? theme.colors.primaryLight : theme.colors.surface,
                  border: 'none', cursor: 'pointer', display: 'flex', justifyContent: 'space-between',
                  alignItems: 'center', fontFamily: theme.fonts.sans,
                }}
              >
                <span style={{ fontWeight: 600, fontSize: 15, color: theme.colors.text }}>
                  Example {i + 1}: {ex.title}
                </span>
                <span style={{ color: theme.colors.textSecondary }}>{openIdx === i ? '▲' : '▼'}</span>
              </button>

              {openIdx === i && (
                <div style={{ padding: '20px 24px', borderTop: `1px solid ${theme.colors.border}` }}>
                  <div style={{ marginBottom: 16 }}>
                    <h4 style={{ margin: '0 0 8px', color: theme.colors.textSecondary, fontSize: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Problem</h4>
                    <p style={{ margin: 0, fontSize: 15, lineHeight: 1.7, color: theme.colors.text }}>{ex.problem_statement}</p>
                  </div>

                  {ex.solution_steps && ex.solution_steps.length > 0 && (
                    <div style={{ marginBottom: 16 }}>
                      <h4 style={{ margin: '0 0 8px', color: theme.colors.textSecondary, fontSize: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Steps</h4>
                      <ol style={{ margin: 0, paddingLeft: 20, display: 'flex', flexDirection: 'column', gap: 8 }}>
                        {ex.solution_steps.map((step, j) => (
                          <li key={j} style={{ fontSize: 14, lineHeight: 1.7, color: theme.colors.text }}>{step}</li>
                        ))}
                      </ol>
                    </div>
                  )}

                  {ex.explanation && (
                    <div style={{ padding: '12px 16px', background: theme.colors.accentLight, borderRadius: theme.radius.sm, borderLeft: `3px solid ${theme.colors.accent}` }}>
                      <h4 style={{ margin: '0 0 6px', fontSize: 12, color: theme.colors.textSecondary, textTransform: 'uppercase', letterSpacing: 1 }}>Key Insight</h4>
                      <p style={{ margin: 0, fontSize: 14, lineHeight: 1.7, color: theme.colors.text }}>{ex.explanation}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
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
