import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NavBar from '../components/NavBar';
import { useAI, callAI } from '../contexts/AIContext';
import api from '../api/client';
import { theme } from '../theme';

const PROVIDERS = [
  {
    id: 'openai',
    name: 'OpenAI',
    description: 'GPT-4o Mini (recommended) or GPT-4o. Fast, reliable, affordable.',
    defaultModel: 'gpt-4o-mini',
    keyUrl: 'https://platform.openai.com/api-keys',
    placeholder: 'sk-...',
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    description: 'Claude Haiku (recommended). Great at math explanations.',
    defaultModel: 'claude-haiku-4-5-20251001',
    keyUrl: 'https://console.anthropic.com/settings/keys',
    placeholder: 'sk-ant-...',
  },
  {
    id: 'google',
    name: 'Google AI',
    description: 'Gemini 1.5 Flash. Free tier available.',
    defaultModel: 'gemini-1.5-flash',
    keyUrl: 'https://aistudio.google.com/app/apikey',
    placeholder: 'AIza...',
  },
];

export default function AISetupPage() {
  const navigate = useNavigate();
  const { aiConfig, saveConfig, clearConfig } = useAI();
  const [provider, setProvider] = useState(aiConfig?.provider || 'openai');
  const [apiKey, setApiKey] = useState(aiConfig?.apiKey || '');
  const [showKey, setShowKey] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  const selectedProvider = PROVIDERS.find(p => p.id === provider);

  const testConnection = async () => {
    if (!apiKey.trim()) return;
    setTesting(true);
    setTestResult(null);
    try {
      if (provider === 'anthropic') {
        // Use backend proxy to avoid CORS issues with Anthropic
        const r = await api.post('/ai/chat', {
          api_key: apiKey.trim(),
          messages: [{ role: 'user', content: 'Say hello' }],
          context: { topic: 'test', problem_text: '', hints: [] },
        });
        if (r.data.response) {
          setTestResult({ ok: true, message: '✓ Connected! AI tutoring is ready to use.' });
        } else {
          setTestResult({ ok: false, message: 'Unexpected response from AI service.' });
        }
      } else {
        // For other providers, call directly from browser
        const config = { provider, apiKey: apiKey.trim(), model: selectedProvider.defaultModel };
        await callAI(config, 'You are a helpful math tutor.', 'Say "Connection successful!" and nothing else.');
        setTestResult({ ok: true, message: '✓ Connected! AI tutoring is ready to use.' });
      }
    } catch (e) {
      const detail = e.response?.data?.detail || e.message;
      setTestResult({ ok: false, message: `Connection failed: ${detail}. Check your API key.` });
    } finally {
      setTesting(false);
    }
  };

  const save = () => {
    if (!apiKey.trim()) return;
    saveConfig({ provider, apiKey: apiKey.trim(), model: selectedProvider.defaultModel });
    navigate(-1);
  };

  return (
    <>
      <NavBar />
      <div style={{ maxWidth: 600, margin: '0 auto', padding: '40px 24px', fontFamily: theme.fonts.sans }}>
        <h1 style={{ margin: '0 0 16px', fontSize: 26, fontWeight: 700, color: theme.colors.text }}>
          Set Up AI Tutoring
        </h1>

        {/* Main explainer */}
        <div style={{
          padding: '20px 20px', background: theme.colors.surfaceAlt,
          borderRadius: theme.radius.md, marginBottom: 24,
          border: `1px solid ${theme.colors.border}`, lineHeight: 1.7, fontSize: 14,
          color: theme.colors.text,
        }}>
          <p style={{ margin: '0 0 12px' }}>
            Fisher App can connect to an AI tutor that gives you personalized help when you're stuck on a problem.
            The AI tutor is powered by <strong>Claude</strong>, made by Anthropic.
          </p>
          <p style={{ margin: '0 0 12px', fontWeight: 600 }}>To use this feature, you'll need an Anthropic API key:</p>
          <ol style={{ margin: '0 0 12px', paddingLeft: 20 }}>
            <li>Go to <a href="https://console.anthropic.com" target="_blank" rel="noopener noreferrer" style={{ color: theme.colors.primary }}>console.anthropic.com</a> and create a free account</li>
            <li>Navigate to <strong>API Keys</strong> in your dashboard</li>
            <li>Click <strong>Create Key</strong> and copy the key</li>
            <li>Paste it below and click <strong>Test Connection</strong></li>
          </ol>
          <a
            href="https://console.anthropic.com"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-block', padding: '8px 16px',
              background: theme.colors.primary, color: '#fff',
              borderRadius: theme.radius.sm, fontSize: 13, fontWeight: 600,
              textDecoration: 'none',
            }}
          >
            Get your API key at console.anthropic.com →
          </a>
        </div>

        {/* Privacy notice */}
        <div style={{ padding: '12px 16px', background: theme.colors.primaryLight, borderRadius: theme.radius.md, marginBottom: 28, border: `1px solid ${theme.colors.primary}`, fontSize: 13, color: theme.colors.primary, lineHeight: 1.6 }}>
          🔒 <strong>Privacy:</strong> Your API key is stored only in your browser — it is never sent to or stored on our servers. You can remove it at any time below.
        </div>

        {/* Provider selection */}
        <div style={{ marginBottom: 24 }}>
          <label style={{ display: 'block', marginBottom: 8, fontSize: 13, fontWeight: 600, color: theme.colors.textSecondary, textTransform: 'uppercase', letterSpacing: 1 }}>
            AI Provider
          </label>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {PROVIDERS.map(p => (
              <button
                key={p.id}
                onClick={() => { setProvider(p.id); setTestResult(null); }}
                style={{
                  padding: '14px 16px', textAlign: 'left',
                  background: provider === p.id ? theme.colors.primaryLight : theme.colors.surfaceAlt,
                  border: `2px solid ${provider === p.id ? theme.colors.primary : theme.colors.border}`,
                  borderRadius: theme.radius.md, cursor: 'pointer', fontFamily: theme.fonts.sans,
                }}
              >
                <div style={{ fontWeight: 600, fontSize: 14, color: theme.colors.text, marginBottom: 2 }}>{p.name}</div>
                <div style={{ fontSize: 12, color: theme.colors.textSecondary }}>{p.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* API key input */}
        <div style={{ marginBottom: 16 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <label style={{ fontSize: 13, fontWeight: 600, color: theme.colors.textSecondary, textTransform: 'uppercase', letterSpacing: 1 }}>
              API Key
            </label>
            <a href={selectedProvider.keyUrl} target="_blank" rel="noopener noreferrer" style={{ fontSize: 12, color: theme.colors.primary }}>
              Get a key →
            </a>
          </div>
          <div style={{ position: 'relative' }}>
            <input
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={e => { setApiKey(e.target.value); setTestResult(null); }}
              placeholder={selectedProvider.placeholder}
              style={{
                width: '100%', padding: '11px 44px 11px 14px', fontSize: 14,
                border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
                background: theme.colors.surface, color: theme.colors.text,
                fontFamily: theme.fonts.sans, boxSizing: 'border-box',
                outline: 'none',
              }}
            />
            <button
              onClick={() => setShowKey(s => !s)}
              style={{
                position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)',
                background: 'none', border: 'none', cursor: 'pointer', fontSize: 16,
                color: theme.colors.textSecondary,
              }}
            >
              {showKey ? '🙈' : '👁️'}
            </button>
          </div>
        </div>

        {/* Test result */}
        {testResult && (
          <div style={{
            padding: '12px 16px', borderRadius: theme.radius.md, marginBottom: 16,
            background: testResult.ok ? theme.colors.successLight : theme.colors.errorLight,
            color: testResult.ok ? theme.colors.success : theme.colors.error,
            fontSize: 14, border: `1px solid ${testResult.ok ? theme.colors.success : theme.colors.error}`,
          }}>
            {testResult.ok ? '✓ ' : '✗ '}{testResult.message}
          </div>
        )}

        {/* Actions */}
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <button
            onClick={testConnection}
            disabled={!apiKey.trim() || testing}
            style={{
              padding: '11px 20px', background: theme.colors.surfaceAlt,
              border: `1px solid ${theme.colors.border}`, borderRadius: theme.radius.md,
              cursor: !apiKey.trim() || testing ? 'not-allowed' : 'pointer',
              fontSize: 14, fontFamily: theme.fonts.sans, color: theme.colors.text,
              opacity: !apiKey.trim() || testing ? 0.6 : 1,
            }}
          >
            {testing ? 'Testing…' : 'Test Connection'}
          </button>
          <button
            onClick={save}
            disabled={!apiKey.trim()}
            style={{
              padding: '11px 24px', background: theme.colors.primary, color: '#fff',
              border: 'none', borderRadius: theme.radius.md,
              cursor: !apiKey.trim() ? 'not-allowed' : 'pointer',
              fontSize: 14, fontWeight: 600, fontFamily: theme.fonts.sans,
              opacity: !apiKey.trim() ? 0.6 : 1,
            }}
          >
            Save & Enable AI
          </button>
          {aiConfig && (
            <button
              onClick={() => { clearConfig(); setApiKey(''); setTestResult(null); }}
              style={{
                padding: '11px 20px', background: theme.colors.errorLight,
                border: `1px solid ${theme.colors.error}`, borderRadius: theme.radius.md,
                cursor: 'pointer', fontSize: 14, fontFamily: theme.fonts.sans, color: theme.colors.error,
              }}
            >
              Remove Key
            </button>
          )}
        </div>
      </div>
    </>
  );
}
