import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/client';
import NavBar from '../components/NavBar';
import MasteryMeter from '../components/MasteryMeter';
import HintPanel from '../components/HintPanel';
import ProgressSteps from '../components/ProgressSteps';
import MathInput from '../components/MathInput';
import { useAI, callAI } from '../contexts/AIContext';
import { theme } from '../theme';

export default function PracticePage() {
  const { nodeId } = useParams();
  const navigate = useNavigate();
  const { aiConfig } = useAI();
  const [sessionId, setSessionId] = useState(null);
  const [problem, setProblem] = useState(null);
  const [mastery, setMastery] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState(null); // { correct, message }
  const [hints, setHints] = useState([]);
  const [loadingHints, setLoadingHints] = useState(false);
  const [questionsAnswered, setQuestionsAnswered] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [nodeTitle, setNodeTitle] = useState('');
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    // Get node title
    api.get(`/lessons/${nodeId}`).then(r => setNodeTitle(r.data.title)).catch(() => {});

    // Start practice session
    api.post(`/practice/${nodeId}/start`).then(r => {
      const d = r.data;
      setSessionId(d.session_id);
      setProblem(d.problem);
      setMastery(d.mastery);
      setQuestionsAnswered(d.questions_answered || 0);
    }).catch(() => {
      setError('Could not start practice session.');
    }).finally(() => setLoading(false));
  }, [nodeId]);

  const fetchHints = async () => {
    if (!problem || loadingHints) return;
    setLoadingHints(true);
    try {
      const r = await api.get(`/practice/${nodeId}/hints/${problem.id}`);
      setHints(r.data);
    } catch {
      setHints([]);
    } finally {
      setLoadingHints(false);
    }
  };

  // Reset hints when problem changes
  useEffect(() => {
    setHints([]);
  }, [problem?.id]);

  const submit = async () => {
    if (!answer.trim() || submitting || !problem) return;
    setSubmitting(true);
    setFeedback(null);
    try {
      const r = await api.post(`/practice/${nodeId}/submit`, {
        session_id: sessionId,
        problem_id: problem.id,
        answer: answer.trim(),
      });
      const d = r.data;
      setMastery(d.mastery);
      setQuestionsAnswered(d.questions_answered);
      setCorrectAnswers(prev => [...prev, d.correct]);
      setFeedback({ correct: d.correct, message: d.feedback || (d.correct ? 'Correct!' : 'Incorrect, try again.') });

      if (d.is_complete) {
        setTimeout(() => navigate(`/score/${nodeId}`, { state: { mastery: d.mastery, questionsAnswered: d.questions_answered, correct: [...correctAnswers, d.correct] } }), 1500);
      } else if (d.next_problem) {
        setTimeout(() => {
          setProblem(d.next_problem);
          setAnswer('');
          setFeedback(null);
        }, 1200);
      }
    } catch {
      setFeedback({ correct: false, message: 'Submission error. Please try again.' });
    } finally {
      setSubmitting(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) submit();
  };

  const endSession = async () => {
    try {
      const r = await api.post(`/practice/${nodeId}/complete`, { session_id: sessionId });
      navigate(`/score/${nodeId}`, { state: { mastery: r.data.mastery, questionsAnswered: r.data.questions_answered, correct: correctAnswers } });
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
              {problem.statement}
            </p>

            {/* Multiple choice */}
            {problem.answer_type === 'multiple_choice' && problem.choices && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 20 }}>
                {problem.choices.map((ch, i) => (
                  <button
                    key={i}
                    onClick={() => setAnswer(ch)}
                    style={{
                      padding: '12px 16px', textAlign: 'left',
                      background: answer === ch ? theme.colors.primaryLight : theme.colors.surfaceAlt,
                      border: `2px solid ${answer === ch ? theme.colors.primary : theme.colors.border}`,
                      borderRadius: theme.radius.md, cursor: 'pointer', fontSize: 14,
                      color: theme.colors.text, fontFamily: theme.fonts.sans,
                      transition: 'all 0.15s',
                    }}
                  >
                    {String.fromCharCode(65 + i)}. {ch}
                  </button>
                ))}
              </div>
            )}

            {/* Free text / numeric / symbolic */}
            {problem.answer_type !== 'multiple_choice' && (
              <MathInput
                value={answer}
                onChange={setAnswer}
                onSubmit={submit}
                placeholder={problem.answer_type === 'numeric' ? 'Enter a number…' : 'Enter your answer…'}
                style={{ marginBottom: 16 }}
              />
            )}

            {/* Feedback banner */}
            {feedback && (
              <div style={{
                padding: '12px 16px', borderRadius: theme.radius.md, marginBottom: 16,
                background: feedback.correct ? theme.colors.successLight : theme.colors.errorLight,
                color: feedback.correct ? theme.colors.success : theme.colors.error,
                fontSize: 14, fontWeight: 500, border: `1px solid ${feedback.correct ? theme.colors.success : theme.colors.error}`,
              }}>
                {feedback.correct ? '✓ ' : '✗ '}{feedback.message}
              </div>
            )}

            <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
              <button
                onClick={submit}
                disabled={!answer.trim() || submitting}
                style={{
                  padding: '11px 28px', background: theme.colors.primary, color: '#fff',
                  border: 'none', borderRadius: theme.radius.md, cursor: !answer.trim() || submitting ? 'not-allowed' : 'pointer',
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
                  cursor: 'pointer', fontSize: 13, color: theme.colors.textSecondary, fontFamily: theme.fonts.sans,
                }}
              >
                Finish session
              </button>
            </div>
          </div>
        )}

        {/* Hints */}
        <HintPanel
          hints={hints}
          onOpen={fetchHints}
          aiConfig={aiConfig}
          onAiHint={async () => {
            if (!problem || !aiConfig) throw new Error('Not configured');
            return callAI(
              aiConfig,
              `You are a math tutor helping a student with ${nodeTitle || 'algebra'}. Give a helpful hint without giving away the final answer. Be encouraging and concise.`,
              `Problem: ${problem.statement}\nStudent's current attempt: ${answer || '(no attempt yet)'}`
            );
          }}
        />
      </div>
    </>
  );
}
