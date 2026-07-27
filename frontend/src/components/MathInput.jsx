import { useEffect, useRef, useState } from 'react';
import 'mathlive';
import { theme } from '../theme.js';

/**
 * MathInput wraps the MathLive <math-field> web component.
 * Exposes a value (LaTeX string) via onChange, and calls onSubmit on Enter.
 *
 * Virtual keyboard (MathLive 0.100 API):
 *   - `mathVirtualKeyboardPolicy = 'auto'` shows the keyboard on focus for
 *     touch devices and leaves desktop alone (no forced-open keyboard).
 *   - The keyboard is a single global singleton (`window.mathVirtualKeyboard`);
 *     its `layouts` are configured once below and shared by every MathInput.
 *   - Desktop users get a small toggle button to open/close it manually.
 */

// A calculus/functions layer (single-layer custom layout via the `rows`
// shortcut). `#?` marks an editable placeholder the caret lands on.
const CALCULUS_LAYOUT = {
  label: '∫∑',
  tooltip: 'Calculus & functions',
  rows: [
    [
      { latex: '\\frac{d}{dx}' }, { latex: '\\frac{\\partial}{\\partial x}' },
      { latex: '\\int' }, { latex: '\\int_{#?}^{#?}' },
      { latex: '\\sum_{#?}^{#?}' }, { latex: '\\prod_{#?}^{#?}' },
      { latex: '\\lim_{#?\\to#?}' }, { latex: '\\infty' },
    ],
    [
      { latex: '\\sin' }, { latex: '\\cos' }, { latex: '\\tan' },
      { latex: '\\csc' }, { latex: '\\sec' }, { latex: '\\cot' },
      { latex: '\\ln' }, { latex: '\\log_{#?}' },
    ],
    [
      { latex: '\\sqrt{#?}' }, { latex: '\\sqrt[#?]{#?}' }, { latex: 'e^{#?}' },
      { latex: '\\to' }, { latex: '\\partial' }, { latex: '\\nabla' },
      { latex: '\\vec{#?}' }, { latex: '\\bar{#?}' },
    ],
  ],
};

// Configure the shared keyboard exactly once. Layers/tabs cover:
// numeric/basic, algebra (frac, sqrt, exponents — in 'numeric'), comparison
// & set operators ('symbols'), Greek ('greek'), and the calculus layer above.
let _keyboardConfigured = false;
function configureVirtualKeyboard() {
  if (_keyboardConfigured) return;
  const kbd = typeof window !== 'undefined' ? window.mathVirtualKeyboard : undefined;
  if (!kbd) return;
  try {
    kbd.layouts = ['numeric', 'symbols', 'greek', CALCULUS_LAYOUT];
    _keyboardConfigured = true;
  } catch {
    // Older/newer API mismatch — fail soft; the default keyboard still works.
  }
}

export default function MathInput({ value, onChange, onSubmit, placeholder = 'Enter your answer', disabled = false }) {
  const mathFieldRef = useRef(null);
  const [kbdOpen, setKbdOpen] = useState(false);

  useEffect(() => {
    const mf = mathFieldRef.current;
    if (!mf) return;

    configureVirtualKeyboard();

    // Configure MathLive options
    mf.smartFence = true;
    // Disable smartSuperscript so multi-digit exponents stay in the superscript.
    // With smartSuperscript=true (default), typing x^12 produces (x^1)2 because
    // MathLive exits the superscript after the first digit.
    mf.smartSuperscript = false;
    // 'auto': keyboard appears on focus for touch devices; desktop stays closed
    // until the user clicks the toggle button below.
    mf.mathVirtualKeyboardPolicy = 'auto';
    if (placeholder) mf.placeholder = placeholder;

    // Add shortcut: type "logb" to insert \log_{#?}(#?) template
    mf.inlineShortcuts = {
      ...mf.inlineShortcuts,
      'logb': '\\log_{#?}\\left(#?\\right)',
    };

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

  // Desktop toggle: focus the field, then show/hide the shared keyboard.
  const toggleKeyboard = () => {
    const mf = mathFieldRef.current;
    const kbd = typeof window !== 'undefined' ? window.mathVirtualKeyboard : undefined;
    if (!mf || !kbd) return;
    if (kbd.visible) {
      kbd.hide();
      setKbdOpen(false);
    } else {
      mf.focus();
      kbd.show();
      setKbdOpen(true);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'stretch', gap: 6 }}>
        <math-field
          ref={mathFieldRef}
          style={{
            display: 'block',
            flex: 1,
            padding: '8px 12px',
            border: `2px solid ${theme.colors.border}`,
            borderRadius: theme.radius.md,
            fontSize: '20px',
            minHeight: '52px',
            background: disabled ? '#F5F4F2' : theme.colors.card,
            boxSizing: 'border-box',
          }}
        />
        <button
          type="button"
          onClick={toggleKeyboard}
          disabled={disabled}
          title={kbdOpen ? 'Hide math keyboard' : 'Show math keyboard'}
          aria-label={kbdOpen ? 'Hide math keyboard' : 'Show math keyboard'}
          style={{
            flexShrink: 0,
            padding: '0 12px',
            border: `2px solid ${theme.colors.border}`,
            borderRadius: theme.radius.md,
            background: kbdOpen ? theme.colors.primaryLight : theme.colors.card,
            cursor: disabled ? 'not-allowed' : 'pointer',
            fontSize: '20px',
            color: theme.colors.text,
          }}
        >
          ⌨
        </button>
      </div>
      <div style={{
        marginTop: '4px',
        fontSize: '12px',
        color: theme.colors.textMuted,
        fontFamily: theme.fonts.sans,
      }}>
        Click to enter math, or use the ⌨ keyboard (numeric, symbols, Greek, calculus). Press Enter to submit. For exponents, type all digits then press → to exit. For log base: type "logb", or "log" then "_".
      </div>
    </div>
  );
}
