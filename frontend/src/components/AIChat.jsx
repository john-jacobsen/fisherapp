import { useState, useRef, useEffect } from 'react';
import { callAI } from '../contexts/AIContext';
import { theme } from '../theme';

export default function AIChat({ aiConfig, systemPrompt, placeholder = 'Ask a question about this topic…' }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    if (open && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, open]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    const userMsg = { role: 'user', text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const response = await callAI(aiConfig, systemPrompt, text);
      setMessages(prev => [...prev, { role: 'assistant', text: response }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', text: `Error: ${e.message}`, error: true }]);
    } finally {
      setLoading(false);
    }
  };

  if (!aiConfig) return null;

  return (
    <div style={{ border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.lg, overflow: 'hidden', marginTop: 24 }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: '100%', padding: '12px 16px', background: theme.colors.primaryLight,
          border: 'none', cursor: 'pointer', display: 'flex', justifyContent: 'space-between',
          alignItems: 'center', fontFamily: theme.fonts.sans,
        }}
      >
        <span style={{ fontSize: 14, fontWeight: 600, color: theme.colors.primary }}>🤖 Ask AI about this lesson</span>
        <span style={{ color: theme.colors.primary }}>{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div style={{ display: 'flex', flexDirection: 'column', height: 320 }}>
          {/* Messages */}
          <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
            {messages.length === 0 && (
              <p style={{ margin: 0, color: theme.colors.textMuted, fontSize: 13, textAlign: 'center', marginTop: 40 }}>
                Ask anything about this lesson!
              </p>
            )}
            {messages.map((m, i) => (
              <div key={i} style={{
                maxWidth: '80%', alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
                padding: '10px 14px', borderRadius: theme.radius.md, fontSize: 13, lineHeight: 1.6,
                background: m.role === 'user' ? theme.colors.primary : (m.error ? theme.colors.errorLight : theme.colors.surfaceAlt),
                color: m.role === 'user' ? '#fff' : (m.error ? theme.colors.error : theme.colors.text),
                fontFamily: theme.fonts.sans,
              }}>
                {m.text}
              </div>
            ))}
            {loading && (
              <div style={{
                alignSelf: 'flex-start', padding: '10px 14px', borderRadius: theme.radius.md,
                background: theme.colors.surfaceAlt, fontSize: 13, color: theme.colors.textSecondary,
              }}>
                Thinking…
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div style={{ padding: '10px 12px', borderTop: `1px solid ${theme.colors.border}`, display: 'flex', gap: 8 }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }}
              placeholder={placeholder}
              style={{
                flex: 1, padding: '9px 12px', fontSize: 13, border: `1px solid ${theme.colors.border}`,
                borderRadius: theme.radius.sm, background: theme.colors.surface, color: theme.colors.text,
                fontFamily: theme.fonts.sans, outline: 'none',
              }}
            />
            <button
              onClick={send}
              disabled={!input.trim() || loading}
              style={{
                padding: '9px 16px', background: theme.colors.primary, color: '#fff',
                border: 'none', borderRadius: theme.radius.sm, cursor: !input.trim() || loading ? 'not-allowed' : 'pointer',
                fontSize: 13, fontFamily: theme.fonts.sans, opacity: !input.trim() || loading ? 0.6 : 1,
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
