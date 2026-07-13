import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MasteryMeter from '../components/MasteryMeter';
import AIChat from '../components/AIChat';
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
  const [curatedVideos, setCuratedVideos] = useState(null); // null = loading, [] = no videos
  const [activeVideoIndex, setActiveVideoIndex] = useState(0);

  useEffect(() => {
    api.get(`/lessons/${nodeId}`)
      .then(r => setLessonData(r.data))
      .catch(() => setError('Could not load lesson.'))
      .finally(() => setLoading(false));

    api.get(`/lessons/${nodeId}/videos`)
      .then(r => setCuratedVideos(r.data.videos || []))
      .catch(() => setCuratedVideos([])); // fallback to Tier 2 if endpoint unavailable
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
  const contentMarkdown = lesson?.content_markdown || '';

  // Tier 1: curated video from lesson_videos.json (via backend endpoint)
  const activeVideo = curatedVideos && curatedVideos.length > 0 ? curatedVideos[activeVideoIndex] : null;
  const activeVideoId = activeVideo ? extractYouTubeId(activeVideo.url) : null;
  const activeEmbedUrl = activeVideoId ? `https://www.youtube.com/embed/${activeVideoId}` : null;


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

        {/* Tier 1: curated video player */}
        {activeEmbedUrl && !videoFailed ? (
          <div style={{ marginBottom: 32 }}>
            <div style={{ borderRadius: theme.radius.lg, overflow: 'hidden', boxShadow: theme.shadow.md }}>
              <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0 }}>
                <iframe
                  src={activeEmbedUrl}
                  title={activeVideo?.title || title}
                  frameBorder="0"
                  allowFullScreen
                  onError={() => setVideoFailed(true)}
                  style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
                />
              </div>
            </div>
            {activeVideo?.source && (
              <div style={{ marginTop: 6, fontSize: 12, color: theme.colors.textSecondary }}>
                Source: {activeVideo.source}
              </div>
            )}
            {/* Video selector when multiple videos exist */}
            {curatedVideos.length > 1 && (
              <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 6 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: theme.colors.textSecondary }}>More videos:</div>
                {curatedVideos.map((v, i) => (
                  <button
                    key={i}
                    onClick={() => { setActiveVideoIndex(i); setVideoFailed(false); }}
                    style={{
                      padding: '8px 14px', textAlign: 'left',
                      background: i === activeVideoIndex ? theme.colors.primaryLight : theme.colors.surfaceAlt,
                      border: `1px solid ${i === activeVideoIndex ? theme.colors.primary : theme.colors.border}`,
                      borderRadius: theme.radius.sm, cursor: 'pointer',
                      fontSize: 13, color: theme.colors.text, fontFamily: theme.fonts.sans,
                    }}
                  >
                    {v.title || `Video ${i + 1}`}
                    {v.source && <span style={{ color: theme.colors.textSecondary }}> — {v.source}</span>}
                  </button>
                ))}
              </div>
            )}
          </div>
        ) : (
          /* No video available */
          <div style={{
            marginBottom: 32, borderRadius: theme.radius.lg, boxShadow: theme.shadow.sm,
            background: theme.colors.surfaceAlt, border: `1px solid ${theme.colors.border}`,
            padding: '28px', textAlign: 'center',
          }}>
            <div style={{ fontSize: 28, marginBottom: 8, color: theme.colors.textMuted }}>▶</div>
            <p style={{ margin: 0, color: theme.colors.textMuted, fontSize: 14 }}>
              No video available for this topic yet.
            </p>
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
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[[rehypeKatex, { throwOnError: false, strict: false }]]}
                components={{
                  p: ({ children }) => (
                    <p style={{ margin: '0 0 12px' }}>{children}</p>
                  ),
                  li: ({ children }) => (
                    <li style={{ marginBottom: 6 }}>{children}</li>
                  ),
                  code: ({ inline, children }) => inline
                    ? <code style={{ background: theme.colors.surfaceAlt, padding: '1px 5px', borderRadius: 4, fontSize: '0.92em' }}>{children}</code>
                    : <pre style={{ background: theme.colors.surfaceAlt, padding: '12px 16px', borderRadius: theme.radius.sm, overflow: 'auto' }}><code>{children}</code></pre>,
                  table: ({ children }) => (
                    <div style={{ overflowX: 'auto', marginBottom: 12 }}>
                      <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 14 }}>{children}</table>
                    </div>
                  ),
                  th: ({ children }) => (
                    <th style={{ border: `1px solid ${theme.colors.border}`, padding: '8px 12px', background: theme.colors.surfaceAlt, fontWeight: 600, textAlign: 'left' }}>{children}</th>
                  ),
                  td: ({ children }) => (
                    <td style={{ border: `1px solid ${theme.colors.border}`, padding: '8px 12px' }}>{children}</td>
                  ),
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

// Extract YouTube video ID from watch, youtu.be, or embed URLs.
// Returns null if the URL is null/empty/placeholder (no valid 11-char ID).
function extractYouTubeId(url) {
  if (!url) return null;
  // youtu.be/VIDEO_ID
  let m = url.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
  if (m) return m[1];
  // youtube.com/watch?v=VIDEO_ID or youtube.com/embed/VIDEO_ID
  m = url.match(/[?&/](?:v=|embed\/)([a-zA-Z0-9_-]{11})/);
  if (m) return m[1];
  return null;
}
