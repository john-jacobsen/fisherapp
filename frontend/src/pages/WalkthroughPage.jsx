import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MathDisplay from '../components/MathDisplay';
import MathInput from '../components/MathInput';
import { theme } from '../theme';

// ── Helper: wrap markdown string children in MathDisplay ─────────────────────
function processMarkdownChildren(children) {
  if (typeof children === 'string') {
    return <MathDisplay content={children} />;
  }
  if (Array.isArray(children)) {
    return children.map((child, i) =>
      typeof child === 'string' ? <MathDisplay key={i} content={child} /> : child
    );
  }
  return children;
}

// ── Per-step input renderer ───────────────────────────────────────────────────
function StepInput({ step, answer, setAnswer, onSubmit, disabled }) {
  const { input_type, options } = step;

  if (input_type === 'multiple_choice') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {(options || []).map((opt, i) => (
          <label
            key={i}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 10,
              padding: '10px 14px',
              borderRadius: theme.radius.md,
              border: `1px solid ${answer === String(i) ? theme.colors.practicing : theme.colors.border}`,
              background: answer === String(i) ? '#E8F2FC' : theme.colors.card,
              cursor: disabled ? 'not-allowed' : 'pointer',
              fontSize: 14,
              color: theme.colors.text,
            }}
          >
            <input
              type="radio"
              name="mc-answer"
              value={String(i)}
              checked={answer === String(i)}
              onChange={e => !disabled && setAnswer(e.target.value)}
              disabled={disabled}
              style={{ marginTop: 3, flexShrink: 0 }}
            />
            <span style={{ lineHeight: 1.5 }}>
              <strong style={{ marginRight: 6 }}>{String.fromCharCode(65 + i)}.</strong>
              <MathDisplay content={opt} />
            </span>
          </label>
        ))}
      </div>
    );
  }

  if (input_type === 'numeric') {
    return (
      <input
        type="number"
        value={answer}
        onChange={e => !disabled && setAnswer(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && !disabled && onSubmit()}
        disabled={disabled}
        placeholder="Enter a number"
        style={{
          width: '100%',
          padding: '10px 14px',
          fontSize: 16,
          border: `2px solid ${theme.colors.border}`,
          borderRadius: theme.radius.md,
          fontFamily: theme.fonts.sans,
          boxSizing: 'border-box',
          background: disabled ? '#F5F4F2' : theme.colors.card,
        }}
      />
    );
  }

  if (input_type === 'expression') {
    return (
      <MathInput
        value={answer}
        onChange={setAnswer}
        onSubmit={onSubmit}
        placeholder="Enter your answer"
        disabled={disabled}
      />
    );
  }

  if (input_type === 'dropdown') {
    return (
      <select
        value={answer}
        onChange={e => !disabled && setAnswer(e.target.value)}
        disabled={disabled}
        style={{
          width: '100%',
          padding: '10px 14px',
          fontSize: 15,
          border: `2px solid ${theme.colors.border}`,
          borderRadius: theme.radius.md,
          fontFamily: theme.fonts.sans,
          background: disabled ? '#F5F4F2' : theme.colors.card,
        }}
      >
        <option value="">Select an answer…</option>
        {(step.options || []).map((opt, i) => (
          <option key={i} value={String(i)}>{opt}</option>
        ))}
      </select>
    );
  }

  return null;
}

// ── Main component ────────────────────────────────────────────────────────────
export default function WalkthroughPage() {
  const { nodeId } = useParams();
  const navigate = useNavigate();

  const [walkthrough, setWalkthrough] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 'intro' | 'steps' | 'completion'
  const [screen, setScreen] = useState('intro');
  const [currentStepIdx, setCurrentStepIdx] = useState(0);
  const [completedSteps, setCompletedSteps] = useState(new Set());

  const [answer, setAnswer] = useState('');
  const [completedAnswers, setCompletedAnswers] = useState({}); // step_number → student answer
  const [feedback, setFeedback] = useState(null);
  const [feedbackType, setFeedbackType] = useState(null); // 'correct' | 'wrong'
  const [showHint, setShowHint] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const fetchWalkthrough = useCallback(() => {
    setLoading(true);
    setError(null);
    api.get(`/walkthrough/${nodeId}`)
      .then(r => {
        setWalkthrough(r.data);
        setScreen('intro');
        setCurrentStepIdx(0);
        setCompletedSteps(new Set());
        setCompletedAnswers({});
        setAnswer('');
        setFeedback(null);
        setFeedbackType(null);
        setShowHint(false);
      })
      .catch(err => {
        if (err.response?.status === 404) {
          // No walkthrough template for this node — fall back to the static lesson
          navigate(`/lesson/${nodeId}`, { replace: true });
        } else {
          setError('Could not load walkthrough.');
        }
      })
      .finally(() => setLoading(false));
  }, [nodeId, navigate]);

  useEffect(() => {
    fetchWalkthrough();
  }, [fetchWalkthrough]);

  const handleSubmit = async () => {
    if (!answer.trim() || submitting || feedbackType === 'correct') return;

    const steps = walkthrough.steps;
    const step = steps[currentStepIdx];

    setSubmitting(true);
    try {
      const res = await api.post(`/walkthrough/${nodeId}/check-step`, {
        step_number: step.step_number,
        answer: answer,
        variables: walkthrough.variables,
      });

      if (res.data.correct) {
        setFeedbackType('correct');
        setFeedback('Correct!');
        // Auto-advance after 1 second
        setTimeout(() => {
          const nextIdx = currentStepIdx + 1;
          setCompletedSteps(prev => new Set([...prev, step.step_number]));
          setCompletedAnswers(prev => ({ ...prev, [step.step_number]: answer }));
          if (nextIdx >= steps.length) {
            setScreen('completion');
          } else {
            setCurrentStepIdx(nextIdx);
            setAnswer('');
            setFeedback(null);
            setFeedbackType(null);
            setShowHint(false);
          }
        }, 1000);
      } else {
        setFeedbackType('wrong');
        setFeedback(res.data.feedback || 'Not quite. Try again.');
        setAnswer('');
      }
    } catch {
      setFeedback('Error checking answer. Please try again.');
      setFeedbackType('wrong');
    } finally {
      setSubmitting(false);
    }
  };

  // ── Render a student's completed answer for review ───────────────────────────
  function renderCompletedAnswer(step, studentAnswer) {
    if (!studentAnswer && studentAnswer !== '0') return null;
    const { input_type, options } = step;
    if (input_type === 'multiple_choice' || input_type === 'dropdown') {
      const idx = parseInt(studentAnswer, 10);
      const text = (options && !isNaN(idx)) ? options[idx] : studentAnswer;
      return <MathDisplay content={text} />;
    }
    if (input_type === 'expression') {
      return <MathDisplay content={studentAnswer} />;
    }
    return <span>{studentAnswer}</span>;
  }

  // ── Loading / error ──────────────────────────────────────────────────────────
  if (loading) {
    return (
      <>
        <NavBar />
        <div style={{
          display: 'flex', justifyContent: 'center', alignItems: 'center',
          minHeight: '60vh', fontFamily: theme.fonts.sans, color: theme.colors.textMuted,
        }}>
          Loading walkthrough…
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <NavBar />
        <div style={{ maxWidth: 700, margin: '40px auto', padding: '0 24px', fontFamily: theme.fonts.sans }}>
          <p style={{ color: theme.colors.danger }}>{error}</p>
          <Link to="/dashboard" style={{ color: theme.colors.primary }}>← Back to dashboard</Link>
        </div>
      </>
    );
  }

  const steps = walkthrough.steps;

  // ── Intro screen ─────────────────────────────────────────────────────────────
  if (screen === 'intro') {
    return (
      <>
        <NavBar />
        <div style={{ maxWidth: 720, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
            <Link to="/dashboard" style={{ color: theme.colors.textMuted, fontSize: 13, textDecoration: 'none' }}>
              ← Dashboard
            </Link>
            <Link
              to={`/practice/${nodeId}`}
              style={{ color: theme.colors.primary, fontSize: 14, fontWeight: 600, textDecoration: 'none' }}
            >
              Skip to Practice →
            </Link>
          </div>

          <h1 style={{ fontSize: 28, fontWeight: 700, color: theme.colors.text, margin: '0 0 24px' }}>
            {walkthrough.title}
          </h1>

          {/* Intro body — markdown with LaTeX */}
          <div style={{
            background: theme.colors.card,
            borderRadius: theme.radius.lg,
            padding: '24px 28px',
            border: `1px solid ${theme.colors.border}`,
            boxShadow: theme.shadow.sm,
            marginBottom: 24,
            lineHeight: 1.8,
            color: theme.colors.text,
            fontSize: 15,
          }}>
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                p: ({ children }) => (
                  <p style={{ margin: '0 0 12px' }}>{processMarkdownChildren(children)}</p>
                ),
                li: ({ children }) => (
                  <li style={{ marginBottom: 6 }}>{processMarkdownChildren(children)}</li>
                ),
                code: ({ inline, children }) => inline
                  ? <MathDisplay content={String(children)} />
                  : <pre style={{ background: '#F5F4F2', padding: '12px 16px', borderRadius: theme.radius.sm, overflow: 'auto' }}><code>{children}</code></pre>,
              }}
            >
              {walkthrough.intro.body}
            </ReactMarkdown>
          </div>

          {/* Key formula */}
          {walkthrough.intro.key_formula && (
            <div style={{
              background: theme.colors.primaryLight,
              border: `1px solid ${theme.colors.primary}`,
              borderRadius: theme.radius.md,
              padding: '16px 20px',
              marginBottom: 32,
              textAlign: 'center',
            }}>
              <MathDisplay content={walkthrough.intro.key_formula} block={true} />
            </div>
          )}

          <div style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={() => setScreen('steps')}
              style={{
                padding: '12px 32px',
                background: theme.colors.primary,
                color: '#fff',
                border: 'none',
                borderRadius: theme.radius.md,
                cursor: 'pointer',
                fontSize: 15,
                fontWeight: 600,
                fontFamily: theme.fonts.sans,
              }}
            >
              Begin Walkthrough →
            </button>
            <Link to={`/practice/${nodeId}`} style={{ color: theme.colors.textMuted, fontSize: 14, textDecoration: 'none' }}>
              Skip to Practice →
            </Link>
          </div>
        </div>
      </>
    );
  }

  // ── Completion screen ─────────────────────────────────────────────────────────
  if (screen === 'completion') {
    return (
      <>
        <NavBar />
        <div style={{ maxWidth: 720, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
          <div style={{ textAlign: 'center', marginBottom: 40 }}>
            <div style={{ fontSize: 52, marginBottom: 12 }}>✓</div>
            <h2 style={{ fontSize: 22, fontWeight: 700, color: theme.colors.text, margin: '0 0 24px' }}>
              Walkthrough Complete!
            </h2>
            <div style={{
              fontSize: 16,
              lineHeight: 1.7,
              color: theme.colors.text,
              background: theme.colors.primaryLight,
              borderRadius: theme.radius.lg,
              padding: '20px 28px',
              border: `1px solid ${theme.colors.primary}`,
              display: 'inline-block',
              maxWidth: 560,
              textAlign: 'left',
            }}>
              <MathDisplay content={walkthrough.completion_message} />
            </div>
          </div>
          <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={() => navigate(`/practice/${nodeId}`)}
              style={{
                padding: '12px 28px',
                background: theme.colors.primary,
                color: '#fff',
                border: 'none',
                borderRadius: theme.radius.md,
                cursor: 'pointer',
                fontSize: 15,
                fontWeight: 600,
                fontFamily: theme.fonts.sans,
              }}
            >
              Start Practice →
            </button>
            <button
              onClick={fetchWalkthrough}
              style={{
                padding: '12px 28px',
                background: theme.colors.card,
                color: theme.colors.text,
                border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.md,
                cursor: 'pointer',
                fontSize: 15,
                fontFamily: theme.fonts.sans,
              }}
            >
              Try Another Example
            </button>
          </div>
        </div>
      </>
    );
  }

  // ── Steps screen ─────────────────────────────────────────────────────────────
  const inputDisabled = submitting || feedbackType === 'correct';

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 720, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <Link to="/dashboard" style={{ color: theme.colors.textMuted, fontSize: 13, textDecoration: 'none' }}>
            ← Dashboard
          </Link>
          <Link
            to={`/practice/${nodeId}`}
            style={{ color: theme.colors.primary, fontSize: 14, fontWeight: 600, textDecoration: 'none' }}
          >
            Skip to Practice →
          </Link>
        </div>

        {/* Pinned problem statement */}
        <div style={{
          background: theme.colors.primaryLight,
          border: `1px solid ${theme.colors.primary}`,
          borderRadius: theme.radius.lg,
          padding: '16px 24px',
          marginBottom: 28,
          fontSize: 18,
          fontWeight: 500,
          color: theme.colors.text,
        }}>
          <MathDisplay content={walkthrough.problem_generator.display_problem} />
        </div>

        {/* Steps list */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {steps.map((step, idx) => {
            const isCompleted = completedSteps.has(step.step_number);
            const isActive = idx === currentStepIdx;
            const isFuture = !isCompleted && !isActive;

            const leftBorderColor = isCompleted
              ? theme.colors.primary
              : isActive
              ? theme.colors.practicing
              : '#D0CFC9';

            return (
              <div
                key={step.step_number}
                style={{
                  borderRadius: theme.radius.lg,
                  border: `1px solid ${isFuture ? theme.colors.border : leftBorderColor}`,
                  borderLeft: `4px solid ${leftBorderColor}`,
                  background: theme.colors.card,
                  opacity: isFuture ? 0.55 : 1,
                  overflow: 'hidden',
                  boxShadow: isActive ? theme.shadow.sm : 'none',
                }}
              >
                {/* Step header */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  padding: '12px 16px',
                  gap: 10,
                }}>
                  <span style={{
                    width: 26, height: 26,
                    borderRadius: '50%',
                    background: isCompleted
                      ? theme.colors.primary
                      : isActive
                      ? theme.colors.practicing
                      : theme.colors.border,
                    color: '#fff',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 12, fontWeight: 700, flexShrink: 0,
                  }}>
                    {isCompleted ? '✓' : step.step_number}
                  </span>
                  <span style={{
                    fontWeight: 600,
                    fontSize: 15,
                    color: isCompleted
                      ? theme.colors.primary
                      : isActive
                      ? theme.colors.text
                      : theme.colors.textMuted,
                    flex: 1,
                  }}>
                    {step.title}
                  </span>
                  {isCompleted && (
                    <span style={{ fontSize: 12, color: theme.colors.primary, fontWeight: 600 }}>
                      Done
                    </span>
                  )}
                </div>

                {/* Completed step body */}
                {isCompleted && (
                  <div style={{ padding: '0 16px 16px' }}>
                    <div style={{ fontSize: 15, color: theme.colors.text, marginBottom: 12, lineHeight: 1.6 }}>
                      <MathDisplay content={step.prompt} />
                    </div>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 10,
                      padding: '10px 14px',
                      background: '#E8F5E9',
                      border: '1px solid #4CAF50',
                      borderRadius: theme.radius.md,
                      fontSize: 15,
                      color: '#2E7D32',
                      fontWeight: 500,
                    }}>
                      <span style={{ fontWeight: 700, fontSize: 18, flexShrink: 0 }}>✓</span>
                      <span>{renderCompletedAnswer(step, completedAnswers[step.step_number])}</span>
                    </div>
                  </div>
                )}

                {/* Active step body */}
                {isActive && (
                  <div style={{ padding: '0 16px 16px' }}>
                    {/* Prompt */}
                    <div style={{ fontSize: 15, color: theme.colors.text, marginBottom: 16, lineHeight: 1.6 }}>
                      <MathDisplay content={step.prompt} />
                    </div>

                    {/* Input */}
                    <div style={{ marginBottom: 12 }}>
                      <StepInput
                        step={step}
                        answer={answer}
                        setAnswer={setAnswer}
                        onSubmit={handleSubmit}
                        disabled={inputDisabled}
                      />
                    </div>

                    {/* Feedback */}
                    {feedback && (
                      <div style={{
                        padding: '10px 14px',
                        borderRadius: theme.radius.md,
                        background: feedbackType === 'correct' ? '#E8F5E9' : '#FFF3E0',
                        border: `1px solid ${feedbackType === 'correct' ? '#4CAF50' : '#FF9800'}`,
                        color: feedbackType === 'correct' ? '#2E7D32' : '#E65100',
                        fontSize: 14,
                        marginBottom: 12,
                      }}>
                        <MathDisplay content={feedback} />
                      </div>
                    )}

                    {/* Submit + Hint buttons */}
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
                      <button
                        onClick={handleSubmit}
                        disabled={!answer.trim() || inputDisabled}
                        style={{
                          padding: '8px 20px',
                          background: (!answer.trim() || inputDisabled)
                            ? theme.colors.border
                            : theme.colors.primary,
                          color: '#fff',
                          border: 'none',
                          borderRadius: theme.radius.md,
                          cursor: (!answer.trim() || inputDisabled) ? 'not-allowed' : 'pointer',
                          fontSize: 14,
                          fontWeight: 600,
                          fontFamily: theme.fonts.sans,
                        }}
                      >
                        {submitting ? 'Checking…' : 'Submit'}
                      </button>
                      {step.hint && (
                        <button
                          onClick={() => setShowHint(h => !h)}
                          style={{
                            padding: '8px 16px',
                            background: 'transparent',
                            color: theme.colors.textMuted,
                            border: `1px solid ${theme.colors.border}`,
                            borderRadius: theme.radius.md,
                            cursor: 'pointer',
                            fontSize: 14,
                            fontFamily: theme.fonts.sans,
                          }}
                        >
                          {showHint ? 'Hide Hint' : '💡 Hint'}
                        </button>
                      )}
                    </div>

                    {/* Hint text */}
                    {showHint && step.hint && (
                      <div style={{
                        marginTop: 12,
                        padding: '10px 14px',
                        background: theme.colors.accentLight,
                        border: `1px solid ${theme.colors.accent}`,
                        borderRadius: theme.radius.md,
                        fontSize: 14,
                        color: '#6B4C0A',
                      }}>
                        <MathDisplay content={step.hint} />
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}
