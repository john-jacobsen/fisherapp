import katex from "katex";
import { useMemo } from "react";

interface MathRendererProps {
  text: string;
  display?: boolean;
  className?: string;
}

/**
 * Renders a string that may contain LaTeX math.
 *
 * Handles three formats:
 * 1. Pure LaTeX (no delimiters) — rendered as math if it contains LaTeX commands
 * 2. Inline math delimiters: $...$ or \(...\)
 * 3. Display math delimiters: $$...$$ or \[...\]
 * 4. Plain text — rendered as-is
 */
export default function MathRenderer({ text, display = false, className = "" }: MathRendererProps) {
  const html = useMemo(() => renderMathText(text, display), [text, display]);

  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

function renderMathText(text: string, displayMode: boolean): string {
  if (!text) return "";

  // Check if the entire string looks like LaTeX (contains backslash commands)
  const hasLatexCommands = /\\[a-zA-Z]+/.test(text);

  // If it has LaTeX commands and no delimiters, render the whole thing as math
  if (hasLatexCommands && !text.includes("$") && !text.includes("\\(") && !text.includes("\\[")) {
    return renderKatex(text, displayMode);
  }

  // Split on math delimiters and render segments
  // Handle $$...$$ (display), $...$ (inline), \[...\] (display), \(...\) (inline)
  const parts: string[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    // Display math: $$...$$
    const ddMatch = remaining.match(/^\$\$([\s\S]*?)\$\$/);
    if (ddMatch) {
      parts.push(renderKatex(ddMatch[1], true));
      remaining = remaining.slice(ddMatch[0].length);
      continue;
    }

    // Display math: \[...\]
    const dbMatch = remaining.match(/^\\\[([\s\S]*?)\\\]/);
    if (dbMatch) {
      parts.push(renderKatex(dbMatch[1], true));
      remaining = remaining.slice(dbMatch[0].length);
      continue;
    }

    // Inline math: $...$
    const sMatch = remaining.match(/^\$([\s\S]*?)\$/);
    if (sMatch) {
      parts.push(renderKatex(sMatch[1], false));
      remaining = remaining.slice(sMatch[0].length);
      continue;
    }

    // Inline math: \(...\)
    const pMatch = remaining.match(/^\\\(([\s\S]*?)\\\)/);
    if (pMatch) {
      parts.push(renderKatex(pMatch[1], false));
      remaining = remaining.slice(pMatch[0].length);
      continue;
    }

    // Plain text until next delimiter
    const nextDelim = remaining.search(/\$|\\\(|\\\[/);
    if (nextDelim === -1) {
      parts.push(escapeHtml(remaining));
      break;
    } else {
      parts.push(escapeHtml(remaining.slice(0, nextDelim)));
      remaining = remaining.slice(nextDelim);
    }
  }

  return parts.join("");
}

function renderKatex(latex: string, displayMode: boolean): string {
  try {
    return katex.renderToString(latex, {
      displayMode,
      throwOnError: false,
      trust: true,
    });
  } catch {
    return `<code>${escapeHtml(latex)}</code>`;
  }
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
