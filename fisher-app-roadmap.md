Here are Phase 2.5 fixes and improvements to implement one at a time:

1. ADDITIONAL AI PROVIDERS: Add support for Google Gemini and DeepSeek API keys alongside the existing Claude and OpenAI options. For Gemini, use the Generative Language API endpoint. For DeepSeek, use their OpenAI-compatible chat completions endpoint at api.deepseek.com.

2. TOPIC SELECTION: Allow users to select which topics they want to practice from the 8 available topics. Add a topic selection screen or checkboxes so users can focus on specific areas (e.g., just logarithms and summation notation). This selection should be changeable at any time.

3. MATH KEYBOARD EXPONENT BUG: When entering a two-digit exponent (like 15) using the MathLive keyboard, only the first digit registers in the exponent position — the second digit drops to the base level. Also, entering the exponent as (15) with parentheses should be accepted as equivalent to 15. Fix both the input behavior and the answer matching to handle parenthesized exponents.

4. PLACEMENT TEST CRASH AT QUESTION 16: The placement test crashes at question 16 with "argument is of length zero." The R backend is likely running out of problems to serve or hitting an index out-of-bounds error. Debug the placement test problem generation logic — check array indexing, ensure enough problems exist for all 16+ questions, and handle edge cases where no problems match the current difficulty/topic filter.
