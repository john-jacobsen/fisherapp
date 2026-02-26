import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MathInput from '../components/MathInput';
import { theme } from '../theme';

function ReviewCard({ review, onComplete }) {
  const [session, setSession] = useState(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [started, setStarted] = useState(false);

  const startReview = async () => {
    try {
      const r = await api.post(`/review/${review.node_id}/start`);
      setSession(r.data);
      setStarted(true);
    } catch {
      alert('Could not start review.');
    }
  };

  const submitAnswer = async () => {
    if (!answer.trim() || submitting || !session) return;
    const problem = session.problems[currentIdx];
    setSubmitting(true);
    try {
      const r = await api.post('/review/submit', {
        node_id: review.node_id,
        problem_id: problem.id,
        answer: answer.trim(),
      });
      const d = r.data;
      setFeedback({ correct: d.correct, message: d.feedback, needsPractice: d.needs_practice });
      if (d.correct) {
        setTimeout(() => {
          if (currentIdx + 1 < session.problems.length) {
            setCurrentIdx(i => i + 1);
            setAnswer('');
            setFeedback(null);
          } else {
            onComplete(review.node_id, true);
          }
        }, 1000);
      } else {
        // Incorrect — after showing feedback, mark complete with needs_practice
        setTimeout(() => {
          onComplete(review.node_id, false);
        }, 2000);
      }
    } catch {
      setFeedback({ correct: false, message: 'Submission error.' });
    } finally {
      setSubmitting(false);
    }
  };

  const daysLabel = review.days_overdue > 0
    ? `${review.days_overdue}d overdue`
    : 'Due now';

  if (!started) {
    return (
      <div style={{
        padding: '20px 24px', background: theme.colors.surface, borderRadius: theme.radius.lg,
        boxShadow: theme.shadow.sm, border: `1px solid ${theme.colors.border}`,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12,
      }}>
        <div>
          <div style={{ fontWeight: 600, fontSize: 16, color: theme.colors.text, marginBottom: 4 }}>{review.node_title}</div>
          <div style={{ fontSize: 12, color: theme.colors.textSecondary }}>
            {review.topic} · Review #{review.review_number + 1} · Streak: {review.streak}
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{
            fontSize: 12, padding: '4px 10px', borderRadius: 20,
            background: review.days_overdue > 0 ? theme.colors.errorLight : theme.colors.warningLight,
            color: review.days_overdue > 0 ? theme.colors.error : theme.colors.warning,
          }}>
            {daysLabel}
          </span>
          <button
            onClick={startReview}
            style={{
              padding: '9px 20px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
              fontSize: 13, fontWeight: 600, fontFamily: theme.fonts.sans,
            }}
          >
            Review
          </button>
        </div>
      </div>
    );
  }

  const problem = session?.problems?.[currentIdx];

  return (
    <div style={{
      padding: '24px', background: theme.colors.surface, borderRadius: theme.radius.lg,
      boxShadow: theme.shadow.md, border: `1px solid ${theme.colors.border}`,
    }}>
      <div style={{ marginBottom: 16, fontSize: 13, color: theme.colors.textSecondary }}>
        {review.node_title} · Problem {currentIdx + 1} of {session.problems.length}
      </div>
      {problem && (
        <>
          <p style={{ margin: '0 0 16px', fontSize: 15, lineHeight: 1.8, color: theme.colors.text }}>{problem.statement}</p>
          {problem.answer_type === 'multiple_choice' && problem.choices ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 16 }}>
              {problem.choices.map((ch, i) => (
                <button key={i} onClick={() => setAnswer(ch)} style={{
                  padding: '10px 14px', textAlign: 'left',
                  background: answer === ch ? theme.colors.primaryLight : theme.colors.surfaceAlt,
                  border: `2px solid ${answer === ch ? theme.colors.primary : theme.colors.border}`,
                  borderRadius: theme.radius.md, cursor: 'pointer', fontSize: 14,
                  fontFamily: theme.fonts.sans,
                }}>
                  {String.fromCharCode(65 + i)}. {ch}
                </button>
              ))}
            </div>
          ) : (
            <MathInput value={answer} onChange={setAnswer} onSubmit={submitAnswer} style={{ marginBottom: 16 }} />
          )}
          {feedback && (
            <div style={{
              padding: '10px 14px', borderRadius: theme.radius.md, marginBottom: 12,
              background: feedback.correct ? theme.colors.successLight : theme.colors.errorLight,
              color: feedback.correct ? theme.colors.success : theme.colors.error,
              fontSize: 14, border: `1px solid ${feedback.correct ? theme.colors.success : theme.colors.error}`,
            }}>
              {feedback.correct ? '✓ ' : '✗ '}{feedback.message}
            </div>
          )}
          <button
            onClick={submitAnswer}
            disabled={!answer.trim() || submitting}
            style={{
              padding: '10px 24px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md, cursor: 'pointer',
              fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
              opacity: !answer.trim() || submitting ? 0.6 : 1,
            }}
          >
            {submitting ? 'Checking…' : 'Submit'}
          </button>
        </>
      )}
    </div>
  );
}

export default function ReviewQueue() {
  const [dueReviews, setDueReviews] = useState([]);
  const [upcomingReviews, setUpcomingReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [completed, setCompleted] = useState(new Set());
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      api.get('/review/due'),
      api.get('/review/upcoming'),
    ]).then(([dueRes, upcomRes]) => {
      setDueReviews(dueRes.data);
      setUpcomingReviews(upcomRes.data);
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const handleComplete = (nodeId, passed) => {
    setCompleted(prev => new Set([...prev, nodeId]));
  };

  const pendingDue = dueReviews.filter(r => !completed.has(r.node_id));

  if (loading) return (
    <>
      <NavBar />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh', fontFamily: theme.fonts.sans, color: theme.colors.textSecondary }}>
        Loading reviews…
      </div>
    </>
  );

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 700, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
        <h1 style={{ margin: '0 0 8px', fontSize: 26, fontWeight: 700, color: theme.colors.text }}>Review Queue</h1>
        <p style={{ margin: '0 0 28px', color: theme.colors.textSecondary, fontSize: 14 }}>
          Spaced repetition keeps mastered skills fresh.
        </p>

        {/* Due reviews */}
        <h2 style={{ margin: '0 0 16px', fontSize: 18, fontWeight: 600, color: theme.colors.text }}>
          Due Now ({pendingDue.length})
        </h2>

        {pendingDue.length === 0 && dueReviews.length === 0 && (
          <div style={{ padding: '32px', textAlign: 'center', background: theme.colors.surfaceAlt, borderRadius: theme.radius.lg, marginBottom: 24 }}>
            <div style={{ fontSize: 32, marginBottom: 8 }}>✅</div>
            <p style={{ margin: 0, color: theme.colors.textSecondary }}>No reviews due. You're all caught up!</p>
          </div>
        )}

        {completed.size > 0 && pendingDue.length === 0 && dueReviews.length > 0 && (
          <div style={{ padding: '20px', textAlign: 'center', background: theme.colors.successLight, borderRadius: theme.radius.lg, marginBottom: 24, border: `1px solid ${theme.colors.success}` }}>
            <p style={{ margin: 0, color: theme.colors.success, fontWeight: 600 }}>
              ✓ All {completed.size} review{completed.size !== 1 ? 's' : ''} completed!
            </p>
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 32 }}>
          {pendingDue.map(r => (
            <ReviewCard key={r.node_id} review={r} onComplete={handleComplete} />
          ))}
        </div>

        {/* Upcoming */}
        {upcomingReviews.length > 0 && (
          <>
            <h2 style={{ margin: '0 0 16px', fontSize: 18, fontWeight: 600, color: theme.colors.text }}>
              Coming Up ({upcomingReviews.length})
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {upcomingReviews.map(r => (
                <div key={r.node_id} style={{
                  padding: '14px 20px', background: theme.colors.surface, borderRadius: theme.radius.md,
                  border: `1px solid ${theme.colors.border}`, display: 'flex',
                  justifyContent: 'space-between', alignItems: 'center',
                }}>
                  <div>
                    <div style={{ fontWeight: 500, fontSize: 14, color: theme.colors.text }}>{r.node_title}</div>
                    <div style={{ fontSize: 12, color: theme.colors.textSecondary }}>{r.topic} · in {r.days_until} day{r.days_until !== 1 ? 's' : ''}</div>
                  </div>
                  <span style={{ fontSize: 12, color: theme.colors.textMuted }}>Streak: {r.streak}</span>
                </div>
              ))}
            </div>
          </>
        )}

        <div style={{ marginTop: 32 }}>
          <Link to="/dashboard" style={{ color: theme.colors.primary, textDecoration: 'none', fontSize: 14 }}>← Back to Dashboard</Link>
        </div>
      </div>
    </>
  );
}
