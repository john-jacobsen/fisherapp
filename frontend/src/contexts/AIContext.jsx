import { createContext, useContext, useState } from 'react';

const AI_STORAGE_KEY = 'fisher_ai_config';

const AIContext = createContext(null);

export function AIProvider({ children }) {
  const [aiConfig, setAiConfig] = useState(() => {
    try {
      const stored = localStorage.getItem(AI_STORAGE_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch { return null; }
  });

  const saveConfig = (config) => {
    if (!config) {
      localStorage.removeItem(AI_STORAGE_KEY);
      setAiConfig(null);
    } else {
      localStorage.setItem(AI_STORAGE_KEY, JSON.stringify(config));
      setAiConfig(config);
    }
  };

  const clearConfig = () => saveConfig(null);

  return (
    <AIContext.Provider value={{ aiConfig, saveConfig, clearConfig }}>
      {children}
    </AIContext.Provider>
  );
}

export function useAI() {
  return useContext(AIContext);
}

// Call AI provider directly from frontend (BYOK — key never sent to backend)
export async function callAI(aiConfig, systemPrompt, userMessage) {
  if (!aiConfig?.provider || !aiConfig?.apiKey) throw new Error('No AI configured');

  const { provider, apiKey, model } = aiConfig;

  if (provider === 'openai') {
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
      body: JSON.stringify({
        model: model || 'gpt-4o-mini',
        messages: [{ role: 'system', content: systemPrompt }, { role: 'user', content: userMessage }],
        max_tokens: 300,
      }),
    });
    if (!res.ok) throw new Error('OpenAI API error');
    const data = await res.json();
    return data.choices[0].message.content;
  }

  if (provider === 'anthropic') {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model: model || 'claude-haiku-4-5-20251001',
        max_tokens: 300,
        system: systemPrompt,
        messages: [{ role: 'user', content: userMessage }],
      }),
    });
    if (!res.ok) throw new Error('Anthropic API error');
    const data = await res.json();
    return data.content[0].text;
  }

  if (provider === 'google') {
    const modelName = model || 'gemini-1.5-flash';
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system_instruction: { parts: [{ text: systemPrompt }] },
          contents: [{ role: 'user', parts: [{ text: userMessage }] }],
          generationConfig: { maxOutputTokens: 300 },
        }),
      }
    );
    if (!res.ok) throw new Error('Google AI API error');
    const data = await res.json();
    return data.candidates[0].content.parts[0].text;
  }

  throw new Error(`Unknown provider: ${provider}`);
}
