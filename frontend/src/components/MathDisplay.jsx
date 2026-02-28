import { useEffect, useRef } from 'react';

/**
 * Wraps detected LaTeX sequences in \( ... \) so MathJax will render them.
 * Strategy: find the first backslash-command and wrap from there to end of string,
 * while keeping any plain-text prefix as-is.
 */
function addMathDelimiters(text) {
  if (!text) return '';
  // Check for LaTeX: backslash followed by a letter or opening brace
  const idx = text.search(/\\[a-zA-Z{]/);
  if (idx === -1) return text;
  const plain = text.slice(0, idx);
  const math = text.slice(idx);
  return plain + '\\(' + math + '\\)';
}

/**
 * MathDisplay renders a string that may contain LaTeX.
 * Uses MathJax (loaded via CDN in index.html) for rendering.
 *
 * Props:
 *   content  - string with plain text and/or LaTeX (e.g. "Evaluate: \sum_{i=1}^{4} i")
 *   block    - if true, renders as a block element; defaults to inline span
 *   style    - optional additional CSS
 */
export default function MathDisplay({ content, block = false, style }) {
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current) return;
    if (window.MathJax?.typesetPromise) {
      // Clear any previous typesetting first to avoid stale state
      if (window.MathJax.typesetClear) {
        window.MathJax.typesetClear([ref.current]);
      }
      window.MathJax.typesetPromise([ref.current]).catch(() => {});
    }
  }, [content]);

  const processed = addMathDelimiters(content || '');
  const Tag = block ? 'div' : 'span';

  return (
    <Tag
      ref={ref}
      dangerouslySetInnerHTML={{ __html: processed }}
      style={style}
    />
  );
}
