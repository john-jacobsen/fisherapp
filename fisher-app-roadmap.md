Here are the next round of fixes and improvements. Work through them one at a time.

1. PRACTICE SESSION BUG - "ALL CAUGHT UP": When a user selects topics and starts a practice session, it immediately shows "All caught up! All topics mastered and none are due for review." This is wrong — practice mode should always serve problems. If no problems are due for spaced repetition review, it should generate new problems at the user's current difficulty level for the selected topics. The "all caught up" message should only appear if the user has truly mastered everything AND there's nothing new to practice, which should be very rare. Fix the problem selection logic to fall back to fresh problem generation.

2. API KEY HELP TEXT: On the AI settings page (both in registration and settings), add a brief 1-2 sentence helper note under each provider explaining where users can find their API key. For example:
   - Anthropic Claude: "Get your API key at console.anthropic.com under API Keys."
   - OpenAI: "Get your API key at platform.openai.com under API Keys."
   - Google Gemini: "Get your API key at aistudio.google.com under API Keys."
   - DeepSeek: "Get your API key at platform.deepseek.com under API Keys."

3. DASHBOARD-BASED PRACTICE FLOW REDESIGN: Replace the separate topic selection screen with an integrated dashboard flow:
   - Make each topic card on the dashboard selectable with a highlighted state when clicked/tapped
   - Add two buttons: "Practice" (begins a session with the manually selected/highlighted topics) and "Smart Practice" (app automatically picks the topics where the user has lowest accuracy or most overdue reviews and starts immediately — no need to visually highlight the cards first)
   - Remove the old separate topic selection screen