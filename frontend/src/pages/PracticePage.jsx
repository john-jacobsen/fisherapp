import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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

  // Feedback state — set after submit, cleared when advancing
  const [feedback, setFeedback] = useState(null); // { isCorrect, correctAnswer, studentAnswer }
  const [nextProblemData, setNextProblemData] = useState(null); // pending next problem
  const [sessionDone, setSessionDone] = useState(false); // mastered or ended

  // Hints state
  const [hints, setHints] = useState([]);
  const [loadingHints, setLoadingHints] = useState(false);
  const [hintsOpen, setHintsOpen] = useState(false); // controlled from "Review Hint" button

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
      setQuestionsAnswered(0);
    }).catch(() => {
      setError('Could not start practice session.');
    }).finally(() => setLoading(false));
  }, [nodeId]);

  const fetchHints = async () => {
    if (!problem || loadingHints) return;
    setLoadingHints(true);

    const timeoutId = setTimeout(() => {
      setLoadingHints(false);
    }, 5000);

    try {
      const r1 = await api.get(`/practice/${nodeId}/hints/${problem.id}`, { params: { level: 1 } });
      const maxLevel = r1.data.max_level || 1;
      const allHints = [{ text: r1.data.hint_text }];
      for (let l = 2; l <= maxLevel; l++) {
        const rl = await api.get(`/practice/${nodeId}/hints/${problem.id}`, { params: { level: l } });
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

  // Reset hints when problem changes
  useEffect(() => {
    setHints([]);
    setHintsOpen(false);
  }, [problem?.id]);

  const submit = async () => {
    if (!answer.trim() || submitting || !problem || feedback) return;
    setSubmitting(true);
    try {
      const r = await api.post(`/practice/${nodeId}/submit`, {
        session_id: sessionId,
        problem_id: problem.id,
        answer: answer.trim(),
      });
      const d = r.data;
      const newMastery = d.mastery?.current_posterior ?? mastery;
      const newQuestionsAnswered = d.mastery?.questions_answered ?? questionsAnswered + 1;
      const isCorrect = d.is_correct;
      const isMastered = d.mastery?.is_mastered ?? false;

      setMastery(newMastery);
      setQuestionsAnswered(newQuestionsAnswered);
      setCorrectAnswers(prev => [...prev, isCorrect]);

      // Show feedback — student stays on problem until they click "Next Problem"
      setFeedback({
        isCorrect,
        correctAnswer: d.correct_answer,
        studentAnswer: answer.trim(),
      });

      // Store what comes next (or that session is done)
      if (isMastered || (!d.next_problem && !isMastered)) {
        setSessionDone(true);
        setNextProblemData(null);
      } else if (d.next_problem) {
        setNextProblemData(d.next_problem);
      } else {
        setSessionDone(true);
      }
    } catch {
      setFeedback({ isCorrect: false, correctAnswer: null, studentAnswer: answer.trim(), error: true });
    } finally {
      setSubmitting(false);
    }
  };

  const advance = () => {
    if (sessionDone) {
      navigate(`/score/${nodeId}`, {
        state: { mastery, questionsAnswered, correct: correctAnswers }
      });
      return;
    }
    if (nextProblemData) {
      setProblem(nextProblemData);
      setAnswer('');
      setFeedback(null);
      setNextProblemData(null);
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

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 760, margin: '0 auto', padding: '32px 24px', fontFamily: theme.fonts.sans }}>
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
                      transition: 'all 0.15s', opacity: hasFeedback ? 0.7 : 1,
                    }}
                  >
                    {String.fromCharCode(65 + i)}. {ch}
                  </button>
                ))}
              </div>
            )}

            {/* Free-entry math input */}
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
                {/* Correct / Incorrect banner */}
                <div style={{
                  padding: '14px 16px', borderRadius: theme.radius.md, marginBottom: 12,
                  background: isCorrect ? theme.colors.successLight : theme.colors.errorLight,
                  color: isCorrect ? theme.colors.success : theme.colors.error,
                  fontSize: 15, fontWeight: 600,
                  border: `1px solid ${isCorrect ? theme.colors.success : theme.colors.error}`,
                }}>
                  {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
                </div>

                {/* Show correct answer if wrong */}
                {!isCorrect && feedback.correctAnswer != null && (
                  <div style={{
                    padding: '12px 16px', borderRadius: theme.radius.md, marginBottom: 12,
                    background: theme.colors.surfaceAlt,
                    border: `1px solid ${theme.colors.border}`,
                    fontSize: 14, color: theme.colors.text,
                  }}>
                    <div style={{ marginBottom: 6, color: theme.colors.textSecondary, fontSize: 13 }}>
                      Your answer:
                    </div>
                    <div style={{ fontWeight: 500 }}>
                      <MathDisplay content={feedback.studentAnswer} />
                    </div>
                    <div style={{ marginTop: 10, marginBottom: 6, color: theme.colors.textSecondary, fontSize: 13 }}>
                      Correct answer:
                    </div>
                    <div style={{ fontWeight: 600, color: theme.colors.success }}>
                      <MathDisplay content={feedback.correctAnswer} />
                    </div>
                    {/* Review Hint button */}
                    <button
                      onClick={() => {
                        setHintsOpen(true);
                        fetchHints();
                      }}
                      style={{
                        marginTop: 10, padding: '6px 14px',
                        background: 'transparent',
                        border: `1px solid ${theme.colors.accent}`,
                        borderRadius: theme.radius.sm, cursor: 'pointer',
                        fontSize: 13, color: theme.colors.accent, fontFamily: theme.fonts.sans,
                      }}
                    >
                      💡 Review Hint
                    </button>
                  </div>
                )}

                {/* Next Problem / End buttons */}
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
                    <button
                      onClick={endSession}
                      style={{
                        padding: '11px 20px', background: 'transparent',
                        border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                        cursor: 'pointer', fontSize: 13, color: theme.colors.textSecondary,
                        fontFamily: theme.fonts.sans,
                      }}
                    >
                      Finish session
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Error feedback */}
            {hasFeedback && feedback.error && (
              <div style={{
                padding: '12px 16px', borderRadius: theme.radius.md, marginTop: 12,
                background: theme.colors.errorLight, color: theme.colors.error,
                fontSize: 14, border: `1px solid ${theme.colors.error}`,
              }}>
                Submission error. Please try again.
              </div>
            )}

            {/* Submit / End buttons (only when no feedback shown) */}
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
                <button
                  onClick={endSession}
                  style={{
                    padding: '11px 20px', background: 'transparent',
                    border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                    cursor: 'pointer', fontSize: 13, color: theme.colors.textSecondary,
                    fontFamily: theme.fonts.sans,
                  }}
                >
                  Finish session
                </button>
              </div>
            )}
          </div>
        )}

        {/* Hints panel */}
        <HintPanel
          hints={hints}
          loading={loadingHints}
          onOpen={fetchHints}
          aiConfig={aiConfig}
          onAiHint={async () => {
            if (!problem || !aiConfig) throw new Error('Not configured');
            const hintsText = hints.length > 0
              ? hints.map((h, i) => `Hint ${i + 1}: ${h.text}`).join('\n')
              : 'No hints revealed yet.';
            return callAI(
              aiConfig,
              `The student is working on this problem: ${problem.problem_text}.\nThey have seen the following hints:\n${hintsText}\nHelp them think through the problem without giving the answer directly. Use clear mathematical reasoning and guide them step by step.`,
              `Student's current attempt: ${answer || '(no attempt yet)'}`
            );
          }}
        />
      </div>
    </>
  );
}
