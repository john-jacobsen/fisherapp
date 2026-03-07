import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MasteryMeter from '../components/MasteryMeter';
import HintPanel from '../components/HintPanel';
import ProgressSteps from '../components/ProgressSteps';
import MathInput from '../components/MathInput';
import MathDisplay from '../components/MathDisplay';
import { useAI, callAI } from '../contexts/AIContext';
import { theme } from '../theme';

export default function PracticePage() {
  const { nodeId } = useParams();
  const navigate = useNavigate();
  const { aiConfig } = useAI();

  // Session state
  const [sessionId, setSessionId] = useState(null);
  const [problem, setProblem] = useState(null);
  const [mastery, setMastery] = useState(0);
  const [answer, setAnswer] = useState('');
  const [questionsAnswered, setQuestionsAnswered] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [nodeTitle, setNodeTitle] = useState('');

  // Mode: "learning" | "test"
  const [mode, setMode] = useState('learning');

  // Feedback state
  const [feedback, setFeedback] = useState(null); // { isCorrect, correctAnswer, studentAnswer }
  const [nextProblemData, setNextProblemData] = useState(null);
  const [sessionDone, setSessionDone] = useState(false);
  const [masteryAchieved, setMasteryAchieved] = useState(false);
  const [networkError, setNetworkError] = useState(false);

  // Hints
  const [hints, setHints] = useState([]);
  const [loadingHints, setLoadingHints] = useState(false);

  // AI Chat panel
  const [showAIChat, setShowAIChat] = useState(false);
  const [aiMessages, setAiMessages] = useState([]);
  const [aiInput, setAiInput] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const aiBottomRef = useRef(null);

  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    api.get(`/lessons/${nodeId}`)
      .then(r => setNodeTitle(r.data.node?.label || ''))
      .catch(() => {});

    api.post(`/practice/${nodeId}/start`).then(r => {
      const d = r.data;
      setSessionId(d.session_id);
      setProblem(d.problem);
      setMastery(d.mastery?.current_posterior ?? 0);
    }).catch(() => {
      setError('Could not start practice session.');
    }).finally(() => setLoading(false));
  }, [nodeId]);

  const fetchHints = async () => {
    if (!problem || loadingHints) return;
    // If hints were returned inline with the problem, use them directly
    if (problem.hints && problem.hints.length > 0) {
      setHints(problem.hints.map(h => ({ text: h.text })));
      return;
    }
    setLoadingHints(true);
    const timeoutId = setTimeout(() => setLoadingHints(false), 5000);
    try {
      const params1 = { level: 1 };
      if (sessionId) params1.session_id = sessionId;
      const r1 = await api.get(`/practice/${nodeId}/hints/${problem.id}`, { params: params1 });
      const maxLevel = r1.data.max_level || 1;
      const allHints = [{ text: r1.data.hint_text }];
      for (let l = 2; l <= maxLevel; l++) {
        const paramsL = { level: l };
        if (sessionId) paramsL.session_id = sessionId;
        const rl = await api.get(`/practice/${nodeId}/hints/${problem.id}`, { params: paramsL });
        allHints.push({ text: rl.data.hint_text });
      }
      setHints(allHints);
    } catch {
      setHints([]);
    } finally {
      clearTimeout(timeoutId);
      setLoadingHints(false);
    }
  };

  useEffect(() => {
    // If the new problem already has inline hints, pre-populate them;
    // otherwise clear so they can be fetched on demand.
    if (problem?.hints && problem.hints.length > 0) {
      setHints(problem.hints.map(h => ({ text: h.text })));
    } else {
      setHints([]);
    }
    // Clear AI chat history when moving to a new problem
    setAiMessages([]);
    setAiInput('');
  }, [problem?.id]);

  const submit = async () => {
    if (!answer.trim() || submitting || !problem || feedback) return;
    setSubmitting(true);
    setNetworkError(false);
    try {
      const r = await api.post(`/practice/${nodeId}/submit`, {
        session_id: sessionId,
        problem_id: problem.id,
        answer: answer.trim(),
        mode,
      });
      const d = r.data;

      // Handle structured error from answer checker (200 response but error:true)
      if (d.error === true) {
        setFeedback({
          isCorrect: false,
          correctAnswer: d.correct_answer ?? null,
          studentAnswer: answer.trim(),
          error: true,
          errorMessage: d.message ?? 'Could not evaluate your answer. Please try a different format.',
        });
        // Allow student to proceed to next problem but do NOT update mastery
        if (d.next_problem) {
          setNextProblemData(d.next_problem);
        } else {
          setNextProblemData(null);
        }
        return;
      }

      const newMastery = d.mastery?.current_posterior ?? mastery;
      const newQuestionsAnswered = d.mastery?.questions_answered ?? questionsAnswered + 1;
      const isCorrect = d.is_correct;
      const isMastered = d.mastery?.is_mastered ?? false;

      // Only update mastery display in test mode
      if (mode === 'test') {
        setMastery(newMastery);
        setQuestionsAnswered(newQuestionsAnswered);
      }
      setCorrectAnswers(prev => [...prev, isCorrect]);

      setFeedback({
        isCorrect,
        correctAnswer: d.correct_answer,
        studentAnswer: answer.trim(),
      });

      if (mode === 'test' && isMastered) {
        setMasteryAchieved(true);
      }
      if (mode === 'test' && (isMastered || (!d.next_problem && !isMastered))) {
        setSessionDone(true);
        setNextProblemData(null);
      } else if (d.next_problem) {
        setNextProblemData(d.next_problem);
      } else {
        // In learning mode there's always more problems available
        setNextProblemData(null);
      }
    } catch {
      setNetworkError(true);
      setSubmitting(false);
      return;
    } finally {
      setSubmitting(false);
    }
  };

  const advance = () => {
    if (sessionDone) {
      // Call /complete so mastery is recorded, review is scheduled, and fringes update
      endSession();
      return;
    }
    if (nextProblemData) {
      setProblem(nextProblemData);
    }
    // In learning mode without a next problem queued, fetch a new one
    setAnswer('');
    setFeedback(null);
    setNextProblemData(null);
  };

  const switchToTest = () => {
    setMode('test');
    setFeedback(null);
  };

  const switchToLearning = () => {
    setMode('learning');
    setFeedback(null);
  };

  const sendAIMessage = async () => {
    const text = aiInput.trim();
    if (!text || aiLoading || !aiConfig?.apiKey) return;

    const userMsg = { role: 'user', content: text };
    const nextMessages = [...aiMessages, userMsg];
    setAiMessages(nextMessages);
    setAiInput('');
    setAiLoading(true);

    try {
      const hintsText = hints.map((h, i) => `Hint ${i + 1}: ${h.text}`);
      const r = await api.post('/ai/chat', {
        api_key: aiConfig.apiKey,
        messages: nextMessages,
        context: {
          topic: nodeTitle || nodeId,
          problem_text: problem?.problem_text || '',
          hints: hintsText,
        },
      });
      setAiMessages(prev => [...prev, { role: 'assistant', content: r.data.response }]);
    } catch (err) {
      const detail = err.response?.data?.detail || 'Could not reach AI. Check your API key.';
      setAiMessages(prev => [...prev, { role: 'assistant', content: `Error: ${detail}`, error: true }]);
    } finally {
      setAiLoading(false);
      setTimeout(() => aiBottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 50);
    }
  };

  const endSession = async () => {
    try {
      const r = await api.post(`/practice/${nodeId}/complete`, { session_id: sessionId });
      navigate(`/score/${nodeId}`, {
        state: {
          mastery: r.data.summary?.mastery_posterior ?? mastery,
          questionsAnswered: r.data.summary?.questions ?? questionsAnswered,
          correct: correctAnswers,
        }
      });
    } catch {
      navigate(`/score/${nodeId}`, { state: { mastery, questionsAnswered, correct: correctAnswers } });
    }
  };

  if (loading) return (
    <>
      <NavBar />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh', fontFamily: theme.fonts.sans, color: theme.colors.textSecondary }}>
        Loading…
      </div>
    </>
  );

  if (error) return (
    <>
      <NavBar />
      <div style={{ maxWidth: 700, margin: '40px auto', padding: '0 24px', fontFamily: theme.fonts.sans }}>
        <p style={{ color: theme.colors.error }}>{error}</p>
      </div>
    </>
  );

  const hasFeedback = !!feedback;
  const isCorrect = feedback?.isCorrect;
  const isLearning = mode === 'learning';

  // Mode banner colors
  const bannerBg = isLearning ? '#EEF6FF' : '#FFF8EE';
  const bannerBorder = isLearning ? theme.colors.primary : '#E8961A';
  const bannerColor = isLearning ? theme.colors.primary : '#B86A00';

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 760, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>

        {/* Mastery celebration banner */}
        {masteryAchieved && (
          <div style={{
            padding: '16px 20px', borderRadius: theme.radius.md, marginBottom: 16,
            background: 'linear-gradient(135deg, #d4edda, #c3e6cb)',
            border: '2px solid #28a745',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: 28, marginBottom: 4 }}>🏆</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: '#155724', marginBottom: 4 }}>
              Topic Mastered!
            </div>
            <div style={{ fontSize: 14, color: '#155724' }}>
              You've demonstrated mastery of this topic. It's been added to your review schedule.
            </div>
          </div>
        )}

        {/* Mode banner */}
        <div style={{
          padding: '10px 16px', borderRadius: theme.radius.md, marginBottom: 16,
          background: bannerBg, border: `1px solid ${bannerBorder}`,
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          flexWrap: 'wrap', gap: 8,
        }}>
          <span style={{ color: bannerColor, fontSize: 13, fontWeight: 600 }}>
            {isLearning
              ? '📖 Learning Mode — hints and AI available. Problems do not count toward mastery.'
              : '🎯 Test Mode — answer without help to demonstrate mastery.'}
          </span>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            {isLearning ? (
              <>
                <button onClick={switchToTest} style={{
                  padding: '5px 14px', background: '#E8961A', color: '#fff', border: 'none',
                  borderRadius: theme.radius.sm, cursor: 'pointer', fontSize: 12, fontWeight: 600,
                  fontFamily: theme.fonts.sans,
                }}>
                  Ready to Test →
                </button>
                <button onClick={switchToTest} style={{
                  padding: '5px 12px', background: 'transparent', color: '#B86A00',
                  border: `1px solid #E8961A`, borderRadius: theme.radius.sm,
                  cursor: 'pointer', fontSize: 12, fontFamily: theme.fonts.sans,
                }}>
                  Skip to Test
                </button>
              </>
            ) : (
              <button onClick={switchToLearning} style={{
                padding: '5px 14px', background: 'transparent', color: theme.colors.primary,
                border: `1px solid ${theme.colors.primary}`, borderRadius: theme.radius.sm,
                cursor: 'pointer', fontSize: 12, fontFamily: theme.fonts.sans,
              }}>
                ← Back to Learning
              </button>
            )}
          </div>
        </div>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, flexWrap: 'wrap', gap: 16 }}>
          <div>
            <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: theme.colors.text }}>{nodeTitle || 'Practice'}</h1>
            <div style={{ marginTop: 8 }}>
              <ProgressSteps total={Math.max(questionsAnswered + 1, 5)} current={questionsAnswered} correct={correctAnswers} />
            </div>
          </div>
          <MasteryMeter mastery={mastery} size={72} />
        </div>

        {/* Problem card */}
        {problem && (
          <div style={{
            background: theme.colors.surface, borderRadius: theme.radius.lg,
            padding: '28px 32px', boxShadow: theme.shadow.md,
            border: `1px solid ${theme.colors.border}`, marginBottom: 20,
          }}>
            <p style={{ margin: '0 0 24px', fontSize: 16, lineHeight: 1.8, color: theme.colors.text }}>
              <MathDisplay content={problem.problem_text} />
            </p>

            {/* Multiple choice */}
            {problem.answer_type === 'multiple_choice' && problem.choices && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 20 }}>
                {problem.choices.map((ch, i) => (
                  <button
                    key={i}
                    onClick={() => !hasFeedback && setAnswer(ch)}
                    disabled={hasFeedback}
                    style={{
                      padding: '12px 16px', textAlign: 'left',
                      background: answer === ch ? theme.colors.primaryLight : theme.colors.surfaceAlt,
                      border: `2px solid ${answer === ch ? theme.colors.primary : theme.colors.border}`,
                      borderRadius: theme.radius.md, cursor: hasFeedback ? 'default' : 'pointer',
                      fontSize: 14, color: theme.colors.text, fontFamily: theme.fonts.sans,
                      opacity: hasFeedback ? 0.7 : 1,
                    }}
                  >
                    {String.fromCharCode(65 + i)}. {ch}
                  </button>
                ))}
              </div>
            )}

            {/* Math input */}
            {problem.answer_type !== 'multiple_choice' && (
              <MathInput
                value={answer}
                onChange={setAnswer}
                onSubmit={submit}
                placeholder={problem.answer_type === 'numeric' ? 'Enter a number…' : 'Enter your answer…'}
                disabled={hasFeedback}
              />
            )}

            {/* Feedback section */}
            {hasFeedback && !feedback.error && (
              <div style={{ marginTop: 16 }}>
                <div style={{
                  padding: '14px 16px', borderRadius: theme.radius.md, marginBottom: 12,
                  background: isCorrect ? theme.colors.successLight : theme.colors.errorLight,
                  color: isCorrect ? theme.colors.success : theme.colors.error,
                  fontSize: 15, fontWeight: 600,
                  border: `1px solid ${isCorrect ? theme.colors.success : theme.colors.error}`,
                }}>
                  {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
                </div>

                {!isCorrect && feedback.correctAnswer != null && (
                  <div style={{
                    padding: '12px 16px', borderRadius: theme.radius.md, marginBottom: 12,
                    background: theme.colors.surfaceAlt, border: `1px solid ${theme.colors.border}`,
                    fontSize: 14, color: theme.colors.text,
                  }}>
                    <div style={{ color: theme.colors.textSecondary, fontSize: 13, marginBottom: 4 }}>Your answer:</div>
                    <div style={{ fontWeight: 500, marginBottom: 10 }}>
                      <MathDisplay content={feedback.studentAnswer} />
                    </div>
                    <div style={{ color: theme.colors.textSecondary, fontSize: 13, marginBottom: 4 }}>Correct answer:</div>
                    <div style={{ fontWeight: 600, color: theme.colors.success }}>
                      <MathDisplay content={feedback.correctAnswer} />
                    </div>

                    {/* Review hint — only in learning mode */}
                    {isLearning && (
                      <button
                        onClick={fetchHints}
                        style={{
                          marginTop: 10, padding: '6px 14px', background: 'transparent',
                          border: `1px solid ${theme.colors.accent}`, borderRadius: theme.radius.sm,
                          cursor: 'pointer', fontSize: 13, color: theme.colors.accent, fontFamily: theme.fonts.sans,
                        }}
                      >
                        💡 Review Hint
                      </button>
                    )}
                  </div>
                )}

                <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap', marginTop: 8 }}>
                  <button
                    onClick={advance}
                    style={{
                      padding: '11px 28px',
                      background: sessionDone ? theme.colors.success : theme.colors.primary,
                      color: '#fff', border: 'none', borderRadius: theme.radius.md,
                      cursor: 'pointer', fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
                    }}
                  >
                    {sessionDone ? 'See Results →' : 'Next Problem →'}
                  </button>
                  {!sessionDone && (
                    <button onClick={endSession} style={{
                      padding: '11px 20px', background: 'transparent',
                      border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                      cursor: 'pointer', fontSize: 13, color: theme.colors.textSecondary, fontFamily: theme.fonts.sans,
                    }}>
                      Finish session
                    </button>
                  )}
                </div>
              </div>
            )}

            {hasFeedback && feedback.error && (
              <div style={{ marginTop: 16 }}>
                <div style={{
                  padding: '14px 16px', borderRadius: theme.radius.md, marginBottom: 12,
                  background: '#FFF8EE', color: '#B86A00',
                  fontSize: 15, fontWeight: 600,
                  border: '1px solid #E8961A',
                }}>
                  {feedback.errorMessage || 'Could not evaluate your answer. Please try a different format.'}
                </div>

                {feedback.correctAnswer != null && (
                  <div style={{
                    padding: '12px 16px', borderRadius: theme.radius.md, marginBottom: 12,
                    background: theme.colors.surfaceAlt, border: `1px solid ${theme.colors.border}`,
                    fontSize: 14, color: theme.colors.text,
                  }}>
                    <div style={{ color: theme.colors.textSecondary, fontSize: 13, marginBottom: 4 }}>Correct answer:</div>
                    <div style={{ fontWeight: 600, color: theme.colors.success }}>
                      <MathDisplay content={feedback.correctAnswer} />
                    </div>
                  </div>
                )}

                <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap', marginTop: 8 }}>
                  <button
                    onClick={advance}
                    style={{
                      padding: '11px 28px',
                      background: theme.colors.primary,
                      color: '#fff', border: 'none', borderRadius: theme.radius.md,
                      cursor: 'pointer', fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
                    }}
                  >
                    Next Problem →
                  </button>
                  <button onClick={endSession} style={{
                    padding: '11px 20px', background: 'transparent',
                    border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                    cursor: 'pointer', fontSize: 13, color: theme.colors.textSecondary, fontFamily: theme.fonts.sans,
                  }}>
                    Finish session
                  </button>
                </div>
              </div>
            )}

            {!hasFeedback && (
              <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap', marginTop: 16 }}>
                <button
                  onClick={submit}
                  disabled={!answer.trim() || submitting}
                  style={{
                    padding: '11px 28px', background: theme.colors.primary, color: '#fff',
                    border: 'none', borderRadius: theme.radius.md,
                    cursor: !answer.trim() || submitting ? 'not-allowed' : 'pointer',
                    fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
                    opacity: !answer.trim() || submitting ? 0.6 : 1,
                  }}
                >
                  {submitting ? 'Checking…' : 'Submit'}
                </button>
                <button onClick={endSession} style={{
                  padding: '11px 20px', background: 'transparent',
                  border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                  cursor: 'pointer', fontSize: 13, color: theme.colors.textSecondary, fontFamily: theme.fonts.sans,
                }}>
                  Finish session
                </button>
              </div>
            )}
          </div>
        )}

        {/* Network error — shown outside the problem card, with a Retry button */}
        {networkError && (
          <div style={{
            padding: '14px 16px', borderRadius: theme.radius.md, marginBottom: 16,
            background: '#FEF2F2', border: `1px solid ${theme.colors.error}`,
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            flexWrap: 'wrap', gap: 12,
            fontFamily: theme.fonts.sans,
          }}>
            <span style={{ color: theme.colors.error, fontSize: 14, fontWeight: 600 }}>
              Connection error — your answer could not be submitted.
            </span>
            <button
              onClick={() => setNetworkError(false)}
              style={{
                padding: '8px 20px', background: theme.colors.error, color: '#fff',
                border: 'none', borderRadius: theme.radius.sm,
                cursor: 'pointer', fontSize: 13, fontWeight: 600, fontFamily: theme.fonts.sans,
              }}
            >
              Try Again
            </button>
          </div>
        )}

        {/* Hints + AI Help — only visible in Learning Mode */}
        <HintPanel
          hints={hints}
          loading={loadingHints}
          onOpen={fetchHints}
          visible={isLearning}
          aiConfig={isLearning ? aiConfig : null}
          onAiHint={async () => {
            if (!problem || !aiConfig) throw new Error('Not configured');
            const hintsText = hints.length > 0
              ? hints.map((h, i) => `Hint ${i + 1}: ${h.text}`).join('\n')
              : 'No hints revealed yet.';
            return callAI(
              aiConfig,
              `The student is working on this problem: ${problem.problem_text}.\nThey have seen the following hints:\n${hintsText}\nHelp them think through the problem without giving the answer directly.`,
              `Student's current attempt: ${answer || '(no attempt yet)'}`
            );
          }}
        />

        {/* AI Help button and chat panel — Learning Mode only */}
        {isLearning && (
          <div style={{ marginTop: 8 }}>
            <button
              onClick={() => {
                if (!aiConfig?.apiKey) {
                  setShowAIChat('no-key');
                } else {
                  setShowAIChat(v => v === 'open' ? false : 'open');
                }
              }}
              style={{
                padding: '10px 16px', width: '100%', background: theme.colors.primaryLight,
                border: `1px solid ${theme.colors.primary}`, borderRadius: theme.radius.md,
                cursor: 'pointer', display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', fontSize: 14, color: theme.colors.primary,
                fontFamily: theme.fonts.sans, fontWeight: 600,
              }}
            >
              <span>🤖 AI Help</span>
              <span>{showAIChat === 'open' ? '▲' : '▼'}</span>
            </button>

            {showAIChat === 'no-key' && (
              <div style={{
                padding: '12px 16px', marginTop: 4,
                background: '#FFF8EE', border: '1px solid #E8961A',
                borderRadius: theme.radius.md, fontSize: 14, color: '#B86A00',
                fontFamily: theme.fonts.sans,
              }}>
                To use AI help, add your Anthropic API key in{' '}
                <Link to="/ai-setup" style={{ color: theme.colors.primary, fontWeight: 600 }}>
                  Settings → AI Hints
                </Link>
                .
              </div>
            )}

            {showAIChat === 'open' && (
              <div style={{
                marginTop: 4, border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.md, overflow: 'hidden',
              }}>
                {/* Chat messages */}
                <div style={{
                  maxHeight: 400, overflowY: 'auto', padding: 12,
                  display: 'flex', flexDirection: 'column', gap: 10,
                  background: theme.colors.surface,
                }}>
                  {aiMessages.length === 0 && (
                    <p style={{ margin: 0, fontSize: 13, color: theme.colors.textSecondary, textAlign: 'center', padding: '16px 0' }}>
                      Ask me anything about this problem!
                    </p>
                  )}
                  {aiMessages.map((m, i) => (
                    <div key={i} style={{
                      maxWidth: '85%',
                      alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
                      padding: '9px 13px', borderRadius: theme.radius.md,
                      fontSize: 13, lineHeight: 1.6,
                      background: m.role === 'user'
                        ? theme.colors.primary
                        : (m.error ? theme.colors.errorLight : '#F1F3F5'),
                      color: m.role === 'user' ? '#fff' : (m.error ? theme.colors.error : theme.colors.text),
                      fontFamily: theme.fonts.sans,
                    }}>
                      {m.role === 'assistant'
                        ? <MathDisplay content={m.content} />
                        : m.content}
                    </div>
                  ))}
                  {aiLoading && (
                    <div style={{
                      alignSelf: 'flex-start', padding: '9px 13px',
                      borderRadius: theme.radius.md, background: '#F1F3F5',
                      fontSize: 13, color: theme.colors.textSecondary,
                    }}>
                      Thinking…
                    </div>
                  )}
                  <div ref={aiBottomRef} />
                </div>

                {/* Input area */}
                <div style={{
                  padding: '10px 12px',
                  borderTop: `1px solid ${theme.colors.border}`,
                  display: 'flex', gap: 8,
                  background: theme.colors.surfaceAlt,
                }}>
                  <input
                    value={aiInput}
                    onChange={e => setAiInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendAIMessage(); } }}
                    placeholder="Ask a question…"
                    style={{
                      flex: 1, padding: '8px 12px', fontSize: 13,
                      border: `1px solid ${theme.colors.border}`,
                      borderRadius: theme.radius.sm,
                      background: theme.colors.surface,
                      color: theme.colors.text,
                      fontFamily: theme.fonts.sans, outline: 'none',
                    }}
                  />
                  <button
                    onClick={sendAIMessage}
                    disabled={!aiInput.trim() || aiLoading}
                    style={{
                      padding: '8px 16px', background: theme.colors.primary,
                      color: '#fff', border: 'none', borderRadius: theme.radius.sm,
                      cursor: !aiInput.trim() || aiLoading ? 'not-allowed' : 'pointer',
                      fontSize: 13, fontFamily: theme.fonts.sans,
                      opacity: !aiInput.trim() || aiLoading ? 0.6 : 1,
                    }}
                  >
                    Send
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}
