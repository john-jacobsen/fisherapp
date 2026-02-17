# Fisher App — Phase 2 Roadmap

Work through these phases one at a time, in order. Each phase should be fully working and tested before moving to the next.

---

## Phase 1: Flexible Answer Matching

The app is too literal when checking answers. For example, it marks "a" wrong when the expected answer is "(a)".

- Build an answer normalization layer in the R backend that runs on both the expected answer and the student's input before comparing
- Strip outer parentheses, whitespace, and normalize case
- Treat equivalent numeric forms as equal (e.g., "0.5" = "1/2" = ".5")
- Treat equivalent algebraic forms as equal (e.g., "x+1" = "1+x", "2x" = "2*x")
- Accept both letter answers and full mathematical expressions where appropriate
- Add unit tests for the normalization function covering edge cases

---

## Phase 2: No Repeat Problems on Wrong Answers

The app currently re-serves the same problem immediately when a student gets it wrong.

- Track recently served problem IDs within each session
- When selecting the next problem, exclude problems already seen in the current session
- The spaced repetition system should still re-surface missed problems in future sessions, just not immediately
- If a topic has very few problems and all have been seen, allow repeats but maximize the gap between them

---

## Phase 3: Placement Diagnostic Test

The app was designed with a placement test but it may not be wired up in the UI.

- Check if placement test logic already exists in the codebase (API routes, frontend components). If so, wire it up. If not, build it.
- On first login (new account), prompt the user to take an optional placement test
- The test should cover all 8 topics with 2-3 questions each at varying difficulty
- Based on results, set initial difficulty levels per topic so students start at the right level
- Allow users to skip the placement test and start at beginner level
- Add the option to retake the placement test from a Settings page

---

## Phase 4: Detailed Step-by-Step Solutions

Current solutions/explanations are too brief. Improve them with structured steps.

- When a student gets a problem wrong, the explanation should be formatted as numbered steps: "Step 1: ...", "Step 2: ...", etc.
- For the built-in (non-AI) explanations, rewrite the explanation templates for each topic to use a step-by-step format
- Each step should show the mathematical operation performed and the result
- This phase is about improving the static explanations — AI-powered explanations come in Phase 6

---

## Phase 5: Math Notation Input Keyboard

Add an on-screen math keyboard so users can input notation like integrals, derivatives, fractions, exponents, etc.

- Integrate MathLive (https://cortexjs.io/mathlive/) as the input field for answers
- The math keyboard should appear when the answer input is focused
- Support at minimum: fractions, exponents, square roots, subscripts, summation notation, logarithms
- The rendered LaTeX/MathML output from MathLive needs to be converted to a format the backend answer checker can compare
- Keep a plain text fallback input option for users who prefer typing
- Ensure the input works on both desktop and mobile

---

## Phase 6: BYOK AI Integration for Solutions

Let users connect their own AI API key for AI-powered step-by-step solutions.

### Registration Flow
- Add an optional, collapsible "AI-Powered Solutions" section to the registration form
- Users can select a provider (Anthropic Claude, OpenAI) and paste an API key, or skip
- Do not block registration if skipped

### Settings Page
- Add a Settings page where users can add, update, or remove their AI API key
- Include a "Test Connection" button that validates the key with a lightweight API call
- Show which provider is currently connected, if any

### Backend
- Add a database column for encrypted API keys (encrypt before storing, never store plaintext)
- Add API endpoints: POST /students/:id/ai-config, GET /students/:id/ai-config, DELETE /students/:id/ai-config
- Add a POST /ai/explain endpoint that takes a problem and the student's stored key, then calls their chosen provider for a step-by-step math solution
- Support Anthropic Claude API (messages endpoint) and OpenAI (chat completions endpoint)
- The prompt to the AI should include the problem, the student's incorrect answer, the correct answer, and the topic, and should ask for a clear step-by-step explanation

### Frontend
- Add a "Show AI Solution" button on incorrect answers (alongside the built-in static steps from Phase 4)
- If no AI key is configured, the button should say "Connect AI in Settings" and link to the settings page
- Display the AI response in a formatted step-by-step layout
- Show a loading indicator while waiting for the AI response
