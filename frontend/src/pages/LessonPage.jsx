import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MasteryMeter from '../components/MasteryMeter';
import AIChat from '../components/AIChat';
import MathDisplay from '../components/MathDisplay';
import { useAI } from '../contexts/AIContext';
import { theme } from '../theme';

export default function LessonPage() {
  const { nodeId } = useParams();
  const navigate = useNavigate();
  const { aiConfig } = useAI();
  const [lessonData, setLessonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [videoFailed, setVideoFailed] = useState(false);

  useEffect(() => {
    api.get(`/lessons/${nodeId}`)
      .then(r => setLessonData(r.data))
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

  // API returns { node, lesson, worked_examples, is_prerequisites_met, mastery }
  const node = lessonData.node || {};
  const lesson = lessonData.lesson || null;
  const workedExamples = lessonData.worked_examples || [];
  const mastery = lessonData.mastery ?? 0;
  const title = node.label || '';
  const topic = node.topic || '';
  const videoUrl = lesson?.video_url || null;
  const contentMarkdown = lesson?.content_markdown || '';

  // Convert YouTube watch URL to embed URL
  const embedUrl = videoUrl
    ? videoUrl.replace('watch?v=', 'embed/').replace('youtu.be/', 'youtube.com/embed/')
    : null;

  const searchQuery = encodeURIComponent(`how to ${title.toLowerCase()} algebra`);
  const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${searchQuery}`;

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
        {/* Breadcrumb */}
        <div style={{ marginBottom: 24, fontSize: 13, color: theme.colors.textSecondary }}>
          <Link to="/dashboard" style={{ color: theme.colors.primary, textDecoration: 'none' }}>Dashboard</Link>
          {' › '}
          <span style={{ color: theme.colors.text }}>{title}</span>
        </div>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 32, flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ fontSize: 12, color: theme.colors.textSecondary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6 }}>
              {topic}
            </div>
            <h1 style={{ margin: 0, fontSize: 28, fontWeight: 700, color: theme.colors.text }}>{title}</h1>
          </div>
          <MasteryMeter mastery={mastery} size={80} />
        </div>

        {/* YouTube embed or fallback */}
        {embedUrl && !videoFailed ? (
          <div style={{ marginBottom: 32, borderRadius: theme.radius.lg, overflow: 'hidden', boxShadow: theme.shadow.md }}>
            <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0 }}>
              <iframe
                src={embedUrl}
                title={title}
                frameBorder="0"
                allowFullScreen
                onError={() => setVideoFailed(true)}
                style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
              />
            </div>
          </div>
        ) : (
          <div style={{
            marginBottom: 32, borderRadius: theme.radius.lg, boxShadow: theme.shadow.sm,
            background: theme.colors.surfaceAlt, border: `1px solid ${theme.colors.border}`,
            padding: '40px 32px', textAlign: 'center',
          }}>
            <div style={{ fontSize: 36, marginBottom: 12 }}>▶</div>
            <p style={{ margin: '0 0 16px', color: theme.colors.textSecondary, fontSize: 15 }}>
              No video available for this topic yet.
            </p>
            <a
              href={youtubeSearchUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-block', padding: '10px 20px',
                background: '#FF0000', color: '#fff', borderRadius: theme.radius.md,
                textDecoration: 'none', fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
              }}
            >
              Search YouTube →
            </a>
          </div>
        )}

        {/* Lesson content */}
        <div style={{
          background: theme.colors.surface, borderRadius: theme.radius.lg,
          padding: '28px 32px', boxShadow: theme.shadow.sm, marginBottom: 32,
          border: `1px solid ${theme.colors.border}`,
        }}>
          <h2 style={{ margin: '0 0 16px', fontSize: 18, color: theme.colors.text }}>Lesson Notes</h2>
          {contentMarkdown ? (
            <div style={{ lineHeight: 1.8, color: theme.colors.text, fontSize: 15 }}>
              <ReactMarkdown
                components={{
                  p: ({ children }) => (
                    <p style={{ margin: '0 0 12px' }}>
                      {processMarkdownChildren(children)}
                    </p>
                  ),
                  li: ({ children }) => (
                    <li style={{ marginBottom: 6 }}>
                      {processMarkdownChildren(children)}
                    </li>
                  ),
                  code: ({ inline, children }) => inline
                    ? <MathDisplay content={String(children)} />
                    : <pre style={{ background: theme.colors.surfaceAlt, padding: '12px 16px', borderRadius: theme.radius.sm, overflow: 'auto' }}><code>{children}</code></pre>,
                }}
              >
                {contentMarkdown}
              </ReactMarkdown>
            </div>
          ) : (
            <p style={{ color: theme.colors.textSecondary }}>No lesson notes available yet.</p>
          )}
        </div>

        {/* AI Chat */}
        {aiConfig && (
          <AIChat
            aiConfig={aiConfig}
            systemPrompt={`You are a math tutor. The student is reading a lesson about "${title}" (${topic}). Here is the lesson content:\n\n${contentMarkdown}\n\nAnswer their question helpfully. Be encouraging. Do not give away answers to problems directly.`}
            placeholder={`Ask about ${title}…`}
          />
        )}
        {!aiConfig && (
          <div style={{ padding: '12px 16px', background: theme.colors.surfaceAlt, borderRadius: theme.radius.md, fontSize: 13, color: theme.colors.textSecondary, marginTop: 16 }}>
            💡 <Link to="/ai-setup" style={{ color: theme.colors.primary }}>Set up AI hints</Link> to ask questions about this lesson.
          </div>
        )}

        {/* Actions */}
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginTop: 24 }}>
          {workedExamples.length > 0 && (
            <button
              onClick={() => navigate(`/lesson/${nodeId}/examples`)}
              style={{
                padding: '12px 24px', background: theme.colors.surfaceAlt,
                border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                cursor: 'pointer', fontSize: 15, fontFamily: theme.fonts.sans, color: theme.colors.text,
              }}
            >
              📖 Worked Examples ({workedExamples.length})
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

// Helper: if a child is a string containing LaTeX, wrap it in MathDisplay
function processMarkdownChildren(children) {
  if (typeof children === 'string') {
    return <MathDisplay content={children} />;
  }
  if (Array.isArray(children)) {
    return children.map((child, i) =>
      typeof child === 'string'
        ? <MathDisplay key={i} content={child} />
        : child
    );
  }
  return children;
}
