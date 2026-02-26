import { theme } from '../theme.js'

export default function MathInput({ value, onChange, onSubmit, placeholder = "Type your answer", disabled = false }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && onSubmit) {
      e.preventDefault()
      onSubmit()
    }
  }

  return (
    <div style={{ position: 'relative' }}>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        style={{
          width: '100%',
          padding: '12px 16px',
          border: `2px solid ${theme.colors.border}`,
          borderRadius: theme.radius.md,
          fontFamily: theme.fonts.sans,
          fontSize: '18px',
          background: disabled ? '#F5F4F2' : theme.colors.card,
          color: theme.colors.text,
          outline: 'none',
          boxSizing: 'border-box',
          transition: 'border-color 0.15s ease',
        }}
        onFocus={(e) => { e.target.style.borderColor = theme.colors.primary }}
        onBlur={(e) => { e.target.style.borderColor = theme.colors.border }}
        autoComplete="off"
        autoCorrect="off"
        spellCheck="false"
      />
      <div style={{
        marginTop: '4px',
        fontSize: '12px',
        color: theme.colors.textMuted,
        fontFamily: theme.fonts.sans,
      }}>
        Enter your answer (e.g. "3/4", "x**2", "12"). Press Enter to submit.
      </div>
    </div>
  )
}
