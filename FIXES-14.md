# FIXES-14: Walkthrough Polish, UI Fixes, and Outstanding Items

## Priority 1 — Walkthrough Bugs (found during testing)

### 14-1: Matrix LaTeX rendering
The `\begin{array}` LaTeX environment does not render in walkthrough intros or steps. Matrices display as flat text like `[2 3 | 8 4 | 1 | 6]` instead of properly stacked rows with brackets.

**Fix:** Update the LaTeX rendering pipeline (rehype-katex / remark-math configuration) in WalkthroughPage.jsx to support `\begin{array}`, `\begin{pmatrix}`, `\begin{bmatrix}`, and `\left[\begin{array}{cc|c}...\end{array}\right]` environments. If KaTeX doesn't support these, switch to MathJax for the walkthrough page, or pre-render the matrix HTML. Test with the linalg-row-reduce intro which uses augmented matrix notation extensively.

### 14-2: Row-reduce multiplier phrasing
When the multiplier is negative (e.g., -1), the walkthrough says "subtract -1 times Row 1" which is technically correct but confusing. When adding rows would be more natural (opposite-sign coefficients), the phrasing should say "add Row 1 to Row 2" instead.

**Fix:** In linalg-row-reduce.json, update the Step 2 prompt to handle negative multipliers more naturally. If multiplier > 0, say "subtract {multiplier} times Row 1 from Row 2." If multiplier < 0, say "add {abs_multiplier} times Row 1 to Row 2." Update the Step 3/4 prompts similarly to match the phrasing.

### 14-3: Completed steps display
Verify that completed walkthrough steps show the full content (prompt, student's correct answer) and not just a collapsed title with "Done." If the earlier fix wasn't applied or was reverted, re-implement: completed steps should remain fully visible so the student can review all their work throughout and at the end.

### 14-4: MathLive toolbar / virtual keyboard
The MathLive input component has no toolbar or virtual keyboard. Students cannot enter matrices, integrals, summations, trig functions (sin, cos, tan), Greek letters, or other advanced notation.

**Fix:** Configure MathLive's virtual keyboard in both WalkthroughPage.jsx and PracticePage.jsx. Enable the full keyboard with these tab groups: basic arithmetic, algebra (fractions, exponents, roots), calculus (integrals, derivatives, limits, summation), matrices, trig functions, Greek letters. Reference MathLive docs: https://cortexjs.io/mathlive/guides/virtual-keyboards/

### 14-5: Video slot in walkthroughs
Each walkthrough should have an optional video at the top of the intro screen, before the conceptual explanation. The infrastructure exists (lesson_videos.json + frontend iframe), but walkthroughs don't use it.

**Fix:** Add an optional `video_id` field to the walkthrough JSON schema. In WalkthroughPage.jsx, if `video_id` is present, render a YouTube iframe embed at the top of the intro screen (before the body text). Use the same embed component/pattern used in LessonPage.jsx. For now, leave video_id empty in all templates — videos will be populated in a later pass.

---

## Priority 2 — Outstanding FIXES-8 Items (never run)

### 14-6: Mastery persistence to dashboard
The frontend never calls the `/complete` endpoint after a student achieves mastery on a topic. Mastery status resets when the page reloads.

**Fix:** In PracticePage.jsx, when the student reaches the mastery threshold, POST to `/api/practice/{nodeId}/complete` (or the appropriate endpoint). Verify the dashboard reflects the updated mastery status after navigation.

### 14-7: Free topic access
Topics currently throw a PermissionError if the student tries to access a topic whose prerequisites aren't all mastered. Remove this gate — all topics should be accessible (the prerequisite structure should be advisory, not enforced).

**Fix:** Remove the PermissionError gate in the backend. Keep the visual distinction (locked/gray appearance on the dashboard for topics with unmet prereqs) but allow navigation to the walkthrough/lesson/practice for any topic.

---

## Priority 3 — Generator and Content Fixes

### 14-8: log-rules generator rewrite
The `log-rules` generator currently expects computed numerical answers (e.g., "4" for log₂(16)). Answers must stay in log form (e.g., "log₂(16)"). The change-of-base formula was also incorrectly added during FIXES-10 and should be removed from the log-rules generator — it belongs in a separate node.

**Fix:** Rewrite the log-rules generator variants to produce problems whose answers are log expressions. Use `strict_form: { type: "log_form" }` on the answer step to reject plain numbers. Remove any change-of-base variants.

### 14-9: Knowledge graph color coding
The "ready to learn" gold/amber color isn't propagating correctly to all eligible nodes on the KnowledgeGraph. Some nodes whose prerequisites are all mastered still display as locked/gray.

**Fix:** In the frontend KnowledgeGraph.jsx, review the logic that determines node status. A node should show as "ready to learn" (amber) if ALL its prerequisites are mastered AND the node itself is not yet mastered. Debug with a test case: master frac-simplify and frac-add-sub, then check if frac-mult (which depends on both) turns amber.

### 14-10: Review enforcement (spaced repetition soft gate)
Currently no enforcement of review schedules. Implement escalating prompts:
- Days 1-2 overdue: dismissible banner on dashboard
- Days 3-5: persistent banner, "Review now" prompt before each practice session
- Days 6+: limit new practice to 3 sessions/day until reviews cleared
- Failed review drops topic from mastered → ready
- Spaced repetition intervals: 1 week → 2 weeks → 1 month → 3 months

---

## Priority 4 — Walkthrough Scaling

### 14-11: AI-generate remaining ~170 walkthrough templates
After stat-ci-z is complete, use the 6 gold-standard walkthroughs as few-shot examples to AI-generate walkthrough JSON + Python generator for all remaining nodes. Process:
1. Write a master prompt referencing the 6 examples
2. Generate in batches by subject (like the lesson rewrites)
3. Run the test suite after each batch to verify hydration and constraints
4. Manual spot-check 5-10 per batch

### 14-12: Video population
Find and populate YouTube video links in lesson_videos.json for all 176 nodes. Preferred channels: Math and Science, Khan Academy, The Organic Chemistry Tutor, A Probability Space. Also acceptable: 3Blue1Brown, Professor Leonard, MIT OpenCourseWare.

---

## Commit Strategy
- Items 14-1 through 14-5: commit as "FIXES-14: Walkthrough UI polish"
- Items 14-6 through 14-7: commit as "FIXES-14: Mastery persistence and free topic access (FIXES-8)"
- Items 14-8 through 14-10: commit as "FIXES-14: Generator fixes and review enforcement"
- Items 14-11 through 14-12: commit as "FIXES-14: Walkthrough scaling and video population"
