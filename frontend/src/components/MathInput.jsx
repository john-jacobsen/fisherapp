import { useEffect, useRef } from 'react';
import 'mathlive';
import { theme } from '../theme.js';

/**
 * MathInput wraps the MathLive <math-field> web component.
 * Exposes a value (LaTeX string) via onChange, and calls onSubmit on Enter.
 */
export default function MathInput({ value, onChange, onSubmit, placeholder = 'Enter your answer', disabled = false }) {
  const mathFieldRef = useRef(null);

  useEffect(() => {
    const mf = mathFieldRef.current;
    if (!mf) return;

    // Configure MathLive options
    mf.smartFence = true;
    mf.virtualKeyboardMode = 'onfocus';
    if (placeholder) mf.placeholder = placeholder;

    const handleInput = () => {
      if (onChange) onChange(mf.value);
    };

    const handleKeyDown = (evt) => {
      if (evt.key === 'Enter' && !evt.shiftKey && onSubmit) {
        evt.preventDefault();
        onSubmit();
      }
    };

    mf.addEventListener('input', handleInput);
    mf.addEventListener('keydown', handleKeyDown);

    return () => {
      mf.removeEventListener('input', handleInput);
      mf.removeEventListener('keydown', handleKeyDown);
    };
  }, [onChange, onSubmit, placeholder]);

  // Sync disabled state
  useEffect(() => {
    const mf = mathFieldRef.current;
    if (mf) mf.disabled = disabled;
  }, [disabled]);

  // Clear the field when value is reset to empty
  useEffect(() => {
    const mf = mathFieldRef.current;
    if (mf && value === '') {
      mf.value = '';
    }
  }, [value]);

  return (
    <div>
      <math-field
        ref={mathFieldRef}
        style={{
          display: 'block',
          width: '100%',
          padding: '8px 12px',
          border: `2px solid ${theme.colors.border}`,
          borderRadius: theme.radius.md,
          fontSize: '20px',
          minHeight: '52px',
          background: disabled ? '#F5F4F2' : theme.colors.card,
          boxSizing: 'border-box',
        }}
      />
      <div style={{
        marginTop: '4px',
        fontSize: '12px',
        color: theme.colors.textMuted,
        fontFamily: theme.fonts.sans,
      }}>
        Click to enter math. Press Enter to submit.
      </div>
    </div>
  );
}
