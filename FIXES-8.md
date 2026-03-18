# FIXES-8: Mastery Persistence Bug + Free Topic Access

**Date:** 2026-03-11
**Commit:** 3037586 (main)

---

## Item 1: Mastery not persisting to dashboard after Test Mode completion

### Symptom

User completes a topic in Test Mode, frontend shows "topic mastered" (meaning `d.mastery.is_mastered` returned `true` from the submit endpoint), but after navigating back to the dashboard:
- The node box stays yellow (not green)
- Mastered count in stats doesn't update

### Diagnosis

The mastery persistence chain is:

1. `POST /practice/{nodeId}/submit` — BKT updates posterior, returns `is_mastered: true` when `posterior >= 0.85 and questions_asked >= 3`
2. Frontend sets `masteryAchieved = true` and `sessionDone = true`
3. **Something must call `POST /practice/{nodeId}/complete`** — this is where `complete_practice()` runs, which adds `node_id` to `StudentState.mastered_nodes`, recomputes fringes, and schedules review
4. Dashboard fetches `GET /dashboard` on mount, which reads `StudentState.mastered_nodes` to build node statuses

The break is almost certainly between steps 2 and 3. One of these is happening:

**Most likely:** The frontend flow after `sessionDone = true` never calls the `/complete` endpoint, or calls it only in some code paths. Check `PracticePage.jsx` for what happens when `sessionDone` is true — there's probably a "Done" or "Continue" button. Trace whether that button calls `api.post(\`/practice/${nodeId}/complete\`, { session_id: sessionId })` before navigating to `/score/${nodeId}`. If it navigates without calling complete, that's the bug.

**Also possible:** The `/complete` endpoint is called but `complete_practice()` checks mastery from the session's `state_snapshot.posterior` rather than from the submit response. If the session state wasn't properly persisted after the last submit (the JSONB shallow copy bug), the complete function would see stale posterior and not mark it mastered.

### Fix instructions

Read `frontend/src/pages/PracticePage.jsx` in full. Find every code path that fires when `sessionDone` becomes true or when the user clicks to leave the session. Verify that ALL paths call `POST /practice/{nodeId}/complete` with `{ session_id }` BEFORE navigating away.

Then read `backend/app/services/practice_service.py` — the `complete_practice` function. Verify it reads `state_snapshot["posterior"]` and compares against `MASTERY_THRESHOLD` (0.85). If the posterior in the snapshot is stale (not updated by the last submit), that's a second bug — submit must persist the updated posterior to `state_snapshot` via `deepcopy` + `flag_modified` before complete can read it.

Specific checks:

1. In `PracticePage.jsx`, search for calls to `/practice/${nodeId}/complete` or `complete`. Confirm this is called when mastery is achieved, not just when the user manually ends the session.

2. In `submit_practice_answer` in `practice_service.py`, confirm the BKT-updated posterior is written back to `session.state_snapshot["posterior"]` with `flag_modified(session, "state_snapshot")` and `db.commit()`. The prior FIXES-6 addressed a JSONB shallow copy bug — verify the fix is in place for the submit path.

3. In `complete_practice`, confirm it reads `session.state_snapshot["posterior"]` (not some other source) and compares it to `MASTERY_THRESHOLD`.

4. If the frontend never calls `/complete` after mastery, add the call. The cleanest approach: add a `useEffect` that fires when `sessionDone && masteryAchieved` (or just `sessionDone`) becomes true, which calls the complete endpoint. Don't rely on a button click — the complete call should be automatic when the session ends.

### Verification

After fixing, run this sequence:
1. Navigate to a topic (e.g., `frac-simplify`)
2. Enter Test Mode
3. Answer problems correctly until mastery is achieved
4. Confirm the "mastered" screen appears
5. Navigate back to dashboard
6. Confirm the node is green and mastered count has incremented
7. Hard-refresh the dashboard (Ctrl+Shift+R) to double-check it persisted to the DB

Also check the backend logs during step 4 for any errors in the complete endpoint.

---

## Item 2: Free topic access (remove prerequisite gate)

### Current behavior

`start_practice()` in `practice_service.py` (line ~117) calls `_check_prereqs(node_id, user_id, db)` and raises `PermissionError` if prerequisites aren't met. The frontend shows locked topics that can't be clicked. This means a student who already knows calculus must grind through every prerequisite before accessing it.

### Desired behavior

Students should be able to practice ANY topic at ANY time, regardless of prerequisites. The prerequisite graph should be *advisory* (informing the recommended path and the adaptive routing), not a *gate*.

Additionally, students should be able to enter Test Mode on any topic to "test out" — if they demonstrate mastery, the BLIM updates accordingly.

### Fix — Backend

In `backend/app/services/practice_service.py`:

1. Find the `_check_prereqs` call in `start_practice()`. Remove the `PermissionError` raise. Instead, keep the prereq check but use it only to set an advisory flag in the response:

```python
prereqs_met = _check_prereqs(node_id, user_id, db)
# ... rest of start_practice ...
return {
    "session_id": str(session.id),
    "problem": first_problem,
    "mastery": {
        "current_posterior": round(posterior, 3),
        "threshold": MASTERY_THRESHOLD,
        "min_questions": 3,
        "soft_cap": 10,
    },
    "prereqs_met": prereqs_met,  # advisory, not blocking
}
```

2. If `_check_prereqs` also gates things elsewhere (e.g., in the dashboard endpoint determining node status), find those too. The dashboard should still label nodes as "recommended" vs "not recommended" based on prereqs, but never "locked" / unclickable.

### Fix — Frontend

In `frontend/src/components/KnowledgeGraph.jsx`:

1. Find where node status is determined. Currently there are likely 4 states: `mastered`, `ready`, `locked`, `practicing`. Change `locked` to something like `available` or `not-recommended` — still visually distinct (e.g., lighter color, dotted border) but CLICKABLE. The node should navigate to `/lesson/{nodeId}` on click regardless of status.

2. If there's a disabled/unclickable state on locked nodes, remove the click gate. All nodes should be clickable.

In `frontend/src/pages/PracticePage.jsx`:

3. If the practice page checks prereqs and redirects away (e.g., catches the 403 from the old prereq gate), remove that redirect. Since the backend no longer returns 403, this may not be needed, but check for any frontend-side prereq checks.

4. Optionally, if `prereqs_met` is false in the start response, show a small banner: "Heads up — some prerequisite topics haven't been completed yet. You can still practice, but you might want to review [list] first." This is purely advisory.

### Fix — Dashboard endpoint

In the dashboard endpoint (likely `backend/app/routers/dashboard.py` or the service it calls), find where node statuses are computed. The logic probably assigns "locked" to nodes whose prereqs aren't mastered. Change this: nodes should be "ready" (or a new "available" status) even if prereqs aren't mastered. The only distinction should be visual priority — recommended nodes (outer fringe) should be highlighted, others should be accessible but less prominent.

### Verification

After fixing:
1. Create a fresh user (or clear mastery state)
2. Navigate to dashboard — confirm all topics are clickable (none are locked/grayed out)
3. Click on an advanced topic (e.g., `stat-ci-t`) — confirm it loads and you can practice
4. Enter Test Mode on that topic — confirm you can submit answers and mastery tracking works
5. Confirm the recommended_next sidebar still shows sensible suggestions based on the prerequisite graph
6. Confirm that mastering a topic still propagates correctly (fringes recompute, downstream nodes become "recommended")
