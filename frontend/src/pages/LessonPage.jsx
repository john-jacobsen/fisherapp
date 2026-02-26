import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MasteryMeter from '../components/MasteryMeter';
import { theme } from '../theme';

export default function LessonPage() {
  const { nodeId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get(`/lessons/${nodeId}`)
      .then(r => setLesson(r.data))
      .catch(() => setError('Could not load lesson.'))
      .finally(() => setLoading(false));
  }, [nodeId]);

  if (loading) return (
    <>
      <NavBar />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh', fontFamily: theme.fonts.sans, color: theme.colors.textSecondary }}>
        Loading lesson…
      </div>
    </>
  );

  if (error) return (
    <>
      <NavBar />
      <div style={{ maxWidth: 700, margin: '40px auto', padding: '0 24px', fontFamily: theme.fonts.sans }}>
        <p style={{ color: theme.colors.error }}>{error}</p>
        <Link to="/dashboard" style={{ color: theme.colors.primary }}>← Back to dashboard</Link>
      </div>
    </>
  );

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
        {/* Breadcrumb */}
        <div style={{ marginBottom: 24, fontSize: 13, color: theme.colors.textSecondary }}>
          <Link to="/dashboard" style={{ color: theme.colors.primary, textDecoration: 'none' }}>Dashboard</Link>
          {' › '}
          <span style={{ color: theme.colors.text }}>{lesson.title}</span>
        </div>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 32, flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ fontSize: 12, color: theme.colors.textSecondary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6 }}>
              {lesson.topic}
            </div>
            <h1 style={{ margin: 0, fontSize: 28, fontWeight: 700, color: theme.colors.text }}>{lesson.title}</h1>
          </div>
          <MasteryMeter mastery={lesson.mastery} size={80} />
        </div>

        {/* YouTube embed */}
        {lesson.youtube_url && (
          <div style={{ marginBottom: 32, borderRadius: theme.radius.lg, overflow: 'hidden', boxShadow: theme.shadow.md }}>
            <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0 }}>
              <iframe
                src={lesson.youtube_url.replace('watch?v=', 'embed/')}
                title={lesson.title}
                frameBorder="0"
                allowFullScreen
                style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
              />
            </div>
          </div>
        )}

        {/* Lesson content */}
        <div style={{
          background: theme.colors.surface, borderRadius: theme.radius.lg,
          padding: '28px 32px', boxShadow: theme.shadow.sm, marginBottom: 32,
          border: `1px solid ${theme.colors.border}`,
        }}>
          <h2 style={{ margin: '0 0 16px', fontSize: 18, color: theme.colors.text }}>Lesson Notes</h2>
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8, color: theme.colors.text, fontSize: 15 }}>
            {lesson.content_md}
          </div>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {lesson.worked_examples_count > 0 && (
            <button
              onClick={() => navigate(`/lesson/${nodeId}/examples`)}
              style={{
                padding: '12px 24px', background: theme.colors.surfaceAlt,
                border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                cursor: 'pointer', fontSize: 15, fontFamily: theme.fonts.sans, color: theme.colors.text,
              }}
            >
              📖 Worked Examples ({lesson.worked_examples_count})
            </button>
          )}
          <button
            onClick={() => navigate(`/practice/${nodeId}`)}
            style={{
              padding: '12px 28px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
              fontSize: 15, fontWeight: 600, fontFamily: theme.fonts.sans,
            }}
          >
            Start Practice →
          </button>
        </div>
      </div>
    </>
  );
}
