import { useEffect, useRef } from 'react';

/**
 * Preprocess a string that may contain math in various formats.
 *
 * Handles:
 *   - Already-delimited \( ... \) and \[ ... \] — passed through as-is
 *   - $$ ... $$ — converted to \[ ... \]
 *   - $ ... $ — converted to \( ... \)
 *   - "Label: raw_latex" — splits on ": " and wraps the math portion
 *   - Strings starting with only brackets/parens before LaTeX — wrap whole string
 *   - Raw LaTeX starting at first \cmd or ^ — wraps from that point to end
 *
 * After this function MathJax will find \( ... \) and \[ ... \] and render them.
 */
function preprocessMath(text) {
  if (!text) return '';

  // If the string already has \( or \[ delimiters, MathJax can handle it directly.
  if (/\\\(|\\\[/.test(text)) {
    return text;
  }

  // Convert $$ ... $$ → \[ ... \]  (do before single $ to avoid conflict)
  let s = text.replace(/\$\$([^$]+)\$\$/gs, '\\[$1\\]');

  // Convert $ ... $ → \( ... \)
  s = s.replace(/\$([^$\n]+)\$/g, '\\($1\\)');

  // If conversion added delimiters, we're done.
  if (/\\\(|\\\[/.test(s)) {
    return s;
  }

  // Check whether the string has any LaTeX content (backslash-command or caret).
  const hasLatex = /\\[a-zA-Z{]/.test(s);
  const hasCaret = /\^/.test(s);
  if (!hasLatex && !hasCaret) {
    return s; // Plain text — no math to process.
  }

  // Try to split "Label: math_expression" pattern.
  // The label must contain at least one letter (not just brackets/spaces).
  const colonIdx = s.search(/:\s/);
  if (colonIdx !== -1) {
    const label = s.slice(0, colonIdx + 2);
    const math = s.slice(colonIdx + 2).trim();
    // Only use colon split if label has actual word characters (not just symbols)
    if (/[a-zA-Z]/.test(label) && math) {
      return label + '\\(' + math + '\\)';
    }
  }

  // No "label: " pattern. Find first LaTeX character.
  const idx = s.search(/\\[a-zA-Z{]|\^/);
  if (idx === -1) return s;

  const plain = s.slice(0, idx);
  const math = s.slice(idx);

  // If the prefix is only whitespace, parentheses, or brackets,
  // treat the whole string as math (handles CommonMark-escaped \( → ()
  if (/^[\s()\[\]{]*$/.test(plain)) {
    return '\\(' + s + '\\)';
  }

  return plain + '\\(' + math + '\\)';
}

/**
 * MathDisplay renders a string that may contain LaTeX math.
 * Uses MathJax (loaded via CDN in index.html) for rendering.
 *
 * Props:
 *   content  — string with plain text and/or LaTeX
 *   block    — if true, renders as a block <div>; defaults to inline <span>
 *   style    — optional additional CSS
 */
export default function MathDisplay({ content, block = false, style }) {
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current) return;
    if (window.MathJax?.typesetPromise) {
      if (window.MathJax.typesetClear) {
        window.MathJax.typesetClear([ref.current]);
      }
      window.MathJax.typesetPromise([ref.current]).catch(() => {});
    }
  }, [content]);

  const processed = preprocessMath(content || '');
  const Tag = block ? 'div' : 'span';

  return (
    <Tag
      ref={ref}
      dangerouslySetInnerHTML={{ __html: processed }}
      style={style}
    />
  );
}
