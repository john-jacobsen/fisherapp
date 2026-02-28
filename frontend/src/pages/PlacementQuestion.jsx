import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import NavBar from '../components/NavBar.jsx'
import MathInput from '../components/MathInput.jsx'
import MathDisplay from '../components/MathDisplay.jsx'
import api from '../api/client.js'
import { theme } from '../theme.js'

export default function PlacementQuestion() {
  const navigate = useNavigate()
  const [session, setSession] = useState(null)       // { session_id }
  const [question, setQuestion] = useState(null)      // { problem_id, node_id, problem_text, topic }
  const [answer, setAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)      // { is_correct, correct_answer }
  const [nextQuestion, setNextQuestion] = useState(null) // stored next question, advance on button click
  const [isComplete, setIsComplete] = useState(false)   // placement test finished
  const [errorMessage, setErrorMessage] = useState(null) // structured error from answer checker
  const [errorNextQuestion, setErrorNextQuestion] = useState(null) // next_question when error occurred
  const [progress, setProgress] = useState({ questions_answered: 0, estimated_remaining: 15 })
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const started = useRef(false)

  useEffect(() => {
    if (started.current) return
    started.current = true

    api.post('/placement/start')
      .then(res => {
        setSession({ session_id: res.data.session_id })
        setQuestion(res.data.first_question)
        setLoading(false)
      })
      .catch(err => {
        setError(err.response?.data?.detail || 'Failed to start placement test')
        setLoading(false)
      })
  }, [])

  const handleSubmit = async () => {
    if (!answer.trim() || submitting || !question || !session) return

    setSubmitting(true)
    setFeedback(null)
    setErrorMessage(null)
    setErrorNextQuestion(null)

    try {
      const res = await api.post('/placement/submit', {
        session_id: session.session_id,
        problem_id: question.problem_id,
        answer: answer.trim(),
      })

      const data = res.data

      // Handle structured error from answer checker (200 response but error: true)
      if (data.error) {
        setErrorMessage('Could not evaluate your answer — please continue to the next question.')
        setErrorNextQuestion(data.next_question || null)
        if (data.progress) setProgress(data.progress)
        setSubmitting(false)
        return
      }

      setFeedback({ is_correct: data.is_correct, correct_answer: data.correct_answer })
      setProgress(data.progress)
      setNextQuestion(data.next_question || null)
      setIsComplete(!!data.is_complete)
      setSubmitting(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Submission failed')
      setSubmitting(false)
    }
  }

  const handleAdvance = () => {
    if (isComplete) {
      navigate('/placement/results')
      return
    }
    setQuestion(nextQuestion)
    setAnswer('')
    setFeedback(null)
    setNextQuestion(null)
    setIsComplete(false)
    setSubmitting(false)
  }

  const handleErrorAdvance = () => {
    if (errorNextQuestion) {
      setQuestion(errorNextQuestion)
    }
    setAnswer('')
    setErrorMessage(null)
    setErrorNextQuestion(null)
    setSubmitting(false)
  }

  const totalEstimated = progress.questions_answered + progress.estimated_remaining
  const progressPct = totalEstimated > 0
    ? Math.round((progress.questions_answered / totalEstimated) * 100)
    : 0

  if (loading) {
    return (
      <>
        <NavBar />
        <div style={styles.center}>
          <p style={{ fontFamily: theme.fonts.sans, color: theme.colors.textMuted }}>
            Setting up your test…
          </p>
        </div>
      </>
    )
  }

  if (error) {
    return (
      <>
        <NavBar />
        <div style={styles.center}>
          <p style={{ color: theme.colors.danger, fontFamily: theme.fonts.sans }}>{error}</p>
          <button onClick={() => navigate('/placement/intro')} style={styles.backBtn}>
            Back
          </button>
        </div>
      </>
    )
  }

  return (
    <>
      <NavBar />
      <div style={styles.page}>
        <div style={styles.card}>
          {/* Progress bar */}
          <div style={styles.progressSection}>
            <div style={styles.progressMeta}>
              <span style={styles.progressLabel}>
                Question {progress.questions_answered + 1} of ~{totalEstimated}
              </span>
              <span style={styles.topicChip}>{question?.topic}</span>
            </div>
            <div style={styles.progressTrack}>
              <div style={{ ...styles.progressFill, width: `${progressPct}%` }} />
            </div>
          </div>

          {/* Problem */}
          <div style={styles.problemBox}>
            <p style={styles.problemText}><MathDisplay content={question?.problem_text || ''} /></p>
          </div>

          {/* Feedback */}
          {feedback && (
            <div style={{
              ...styles.feedbackBox,
              background: feedback.is_correct ? theme.colors.primaryLight : '#FEF2F2',
              border: `1px solid ${feedback.is_correct ? theme.colors.primary : theme.colors.danger}`,
            }}>
              <span style={{
                fontFamily: theme.fonts.sans,
                fontSize: '15px',
                fontWeight: 600,
                color: feedback.is_correct ? theme.colors.primary : theme.colors.danger,
                display: 'block',
                marginBottom: '12px',
              }}>
                {feedback.is_correct ? '✓ Correct' : '✗ Incorrect'}
              </span>
              <button
                onClick={handleAdvance}
                style={{
                  ...styles.submitBtn,
                  background: theme.colors.primary,
                  width: 'auto',
                  padding: '10px 24px',
                  cursor: 'pointer',
                }}
              >
                {isComplete ? 'See Results →' : 'Next Question →'}
              </button>
            </div>
          )}

          {/* Answer checker error — warning without revealing correct answer */}
          {errorMessage && (
            <div style={{
              ...styles.feedbackBox,
              background: '#FFFBEB',
              border: '1px solid #F59E0B',
            }}>
              <span style={{
                fontFamily: theme.fonts.sans,
                fontSize: '15px',
                fontWeight: 600,
                color: '#92400E',
                display: 'block',
                marginBottom: '12px',
              }}>
                {errorMessage}
              </span>
              <button
                onClick={handleErrorAdvance}
                style={{
                  ...styles.submitBtn,
                  background: '#F59E0B',
                  width: 'auto',
                  padding: '10px 24px',
                }}
              >
                Next Question →
              </button>
            </div>
          )}

          {/* Input */}
          {!feedback && !errorMessage && (
            <div style={styles.inputSection}>
              <MathInput
                value={answer}
                onChange={setAnswer}
                onSubmit={handleSubmit}
                disabled={submitting}
                placeholder="Type your answer…"
              />
              <button
                onClick={handleSubmit}
                disabled={!answer.trim() || submitting}
                style={{
                  ...styles.submitBtn,
                  opacity: !answer.trim() || submitting ? 0.5 : 1,
                  cursor: !answer.trim() || submitting ? 'not-allowed' : 'pointer',
                }}
              >
                {submitting ? 'Checking…' : 'Submit Answer'}
              </button>
            </div>
          )}

          <p style={styles.disclaimer}>
            No hints during placement — answer as best you can.
          </p>
        </div>
      </div>
    </>
  )
}

const styles = {
  page: {
    minHeight: 'calc(100vh - 56px)',
    background: theme.colors.bg,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px 16px',
  },
  center: {
    minHeight: 'calc(100vh - 56px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'column',
    gap: '16px',
  },
  card: {
    background: theme.colors.card,
    borderRadius: '16px',
    boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
    padding: '40px 48px',
    maxWidth: '600px',
    width: '100%',
  },
  progressSection: { marginBottom: '32px' },
  progressMeta: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px',
  },
  progressLabel: {
    fontFamily: theme.fonts.sans,
    fontSize: '13px',
    color: theme.colors.textMuted,
  },
  topicChip: {
    fontFamily: theme.fonts.sans,
    fontSize: '12px',
    fontWeight: 600,
    color: theme.colors.primary,
    background: theme.colors.primaryLight,
    padding: '3px 10px',
    borderRadius: '20px',
  },
  progressTrack: {
    height: '6px',
    background: theme.colors.border,
    borderRadius: '3px',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    background: theme.colors.primary,
    borderRadius: '3px',
    transition: 'width 0.3s ease',
  },
  problemBox: {
    background: theme.colors.bg,
    borderRadius: '8px',
    padding: '24px',
    marginBottom: '24px',
    minHeight: '80px',
    display: 'flex',
    alignItems: 'center',
  },
  problemText: {
    fontFamily: theme.fonts.serif,
    fontSize: '20px',
    color: theme.colors.text,
    margin: 0,
    lineHeight: 1.5,
  },
  feedbackBox: {
    borderRadius: '8px',
    padding: '16px 20px',
    marginBottom: '16px',
  },
  inputSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  submitBtn: {
    background: theme.colors.primary,
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    padding: '12px',
    fontFamily: theme.fonts.sans,
    fontSize: '15px',
    fontWeight: 600,
    width: '100%',
  },
  disclaimer: {
    fontFamily: theme.fonts.sans,
    fontSize: '12px',
    color: theme.colors.textMuted,
    textAlign: 'center',
    marginTop: '20px',
    marginBottom: 0,
  },
  backBtn: {
    background: 'transparent',
    border: `1px solid ${theme.colors.border}`,
    borderRadius: '8px',
    padding: '10px 24px',
    fontFamily: theme.fonts.sans,
    fontSize: '14px',
    cursor: 'pointer',
    color: theme.colors.textMuted,
  },
}
