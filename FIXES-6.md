FISHER APP 3.0 — ROUND 6: FINAL POLISH
========================================

This is a short polish round. Read FIXES-5.md for context on what was
done in the previous round.

Read this entire document before writing any code. Implement in order.

Project location: C:\Users\jjcas\Desktop\Fisher App\Fisher App 3.0\
GitHub repo: https://github.com/john-jacobsen/fisherapp

The app runs via Docker Compose (3 services: backend, frontend, db).
  Frontend: React 18+ / Vite at localhost:5173
  Backend: Python 3.11+ / FastAPI at localhost:8000
  Database: PostgreSQL 15 / SQLAlchemy ORM / Alembic migrations


========================================================================
VERSION CONTROL — COMMIT AND PUSH AFTER EACH ITEM
========================================================================

After completing each item, rebuild, test, then commit and push:

  docker compose up --build
  git add -A
  git commit -m "FIXES-6 Item N: [brief description]"
  git push origin main


========================================================================
ITEM 1: SHOW SPECIFIC AI ERROR MESSAGES
========================================================================

Priority: HIGH — users see "AI service unavailable" when the real error
is "credit balance too low."

PROBLEM:
The AI proxy endpoint (backend/app/routers/ai_chat.py) catches Anthropic
API errors and returns a generic 502 "AI service unavailable" message.
The actual error from Anthropic (e.g., "Your credit balance is too low
to access the Anthropic API") is logged but never shown to the user.

FIX:
1. In ai_chat.py, when the Anthropic API returns an error, parse the
   error response body and extract the human-readable message.

2. Return SPECIFIC error messages to the frontend based on the error:

   - 401 from Anthropic → return 401 to frontend:
     "Invalid API key. Check that your key is correct."

   - 400 with "credit balance" in message → return 402 to frontend:
     "Your Anthropic API credit balance is too low. Add credits at
     console.anthropic.com/settings/billing"

   - 400 with other message → return 400 to frontend with Anthropic's
     actual error message

   - 429 from Anthropic → return 429 to frontend:
     "Rate limited. Please wait a moment and try again."

   - 500+ from Anthropic → return 502 to frontend:
     "Anthropic API is temporarily unavailable. Try again later."

   - Network/connection error → return 502 to frontend:
     "Could not reach Anthropic API. Check your internet connection."

3. The frontend already displays the detail message from the response,
   so these specific messages will show up automatically in both the
   AI setup page test and the practice page chat panel.

4. Also update the AI setup page (AISetupPage.jsx): when the test
   connection fails with the "credit balance" error, show a direct
   link to the Anthropic billing page in the error message.


========================================================================
ITEM 2: FIX MASTERY NOT UPDATING KNOWLEDGE MAP
========================================================================

Priority: HIGH — students master a topic but the dashboard doesn't
reflect it.

SYMPTOMS:
- Student answers enough questions correctly in Test Mode
- Mastery celebration banner appears (🏆 Topic Mastered!)
- Student navigates to dashboard
- The knowledge map still shows the old mastery state — the node is
  NOT marked as mastered, and no new topics are unlocked

DIAGNOSIS:
The mastery celebration fires because the submit response includes
is_mastered=true. But the dashboard reads from StudentState (or a
similar persistent record), which is updated by the /complete endpoint.

Check this flow:

1. When is_mastered is true in the submit response, the frontend sets
   sessionDone=true and shows "See Results →" (or similar).

2. When the user clicks that button, PracticePage.jsx calls endSession()
   which posts to /api/practice/{nodeId}/complete.

3. The complete endpoint in practice_service.py should:
   a) Add the node to the student's mastered_nodes set
   b) Update the inner_fringe and outer_fringe
   c) Create a ReviewSchedule for the mastered node
   d) Persist all changes to the database

4. The dashboard endpoint reads from StudentState.mastered_nodes to
   determine node colors.

LIKELY ISSUES:

A) The /complete endpoint might not be called at all. Check if
   endSession() is actually triggered when sessionDone is true.
   Look at PracticePage.jsx — does the "See Results" or "Finish
   Session" button call endSession()? Or does it just navigate away?

B) The /complete endpoint might be called but fail silently. Add
   logging to complete_practice() in practice_service.py to verify
   it runs and check for errors.

C) The /complete endpoint might update the session but NOT update
   StudentState.mastered_nodes. Check if the mastered_nodes set
   is being modified AND persisted (same JSONB mutation issue from
   FIXES-5 Item 1 — need flag_modified).

D) The dashboard endpoint might be reading stale data. Check if
   it queries StudentState correctly.

FIX:
- Debug the complete flow end-to-end with logging
- Ensure mastered_nodes is updated with deepcopy + flag_modified
- Ensure inner_fringe and outer_fringe are recalculated
- Ensure ReviewSchedule is created
- Verify by: master a topic → navigate to dashboard → node color changed

IMPORTANT: This is almost certainly the same deepcopy/flag_modified
bug from FIXES-5 Item 1. Check complete_practice() for any .copy()
calls on JSONB fields and replace with copy.deepcopy() + flag_modified().


========================================================================
ITEM 3: MOVE "READY TO TEST" BUTTON NEXT TO SUBMIT
========================================================================

Priority: MEDIUM — usability improvement.

PROBLEM:
The "Ready to Test →" button is in the mode banner at the top of the
page. New users don't notice it because their attention is on the
problem and answer area.

FIX:
In PracticePage.jsx, when the user is in Learning Mode:

1. After the Submit button, add a secondary button:
   "Switch to Test Mode →"

   Layout: Submit button (primary, full width or left-aligned) and
   "Switch to Test Mode →" (secondary/outlined, right-aligned) on
   the same row.

   Example layout:
   ┌─────────────────────────────┬──────────────────────┐
   │     Submit Answer           │  Switch to Test →    │
   └─────────────────────────────┴──────────────────────┘

2. Keep the mode banner at the top as well (it provides context),
   but the primary call-to-action for switching modes should be
   near the submit button where the user is already looking.

3. In Test Mode, show the Submit button and a smaller "Back to
   Learning" link (not a full button) below it.

4. The "Switch to Test Mode →" button should call the same
   switchToTest() function as the banner button.

5. Style the "Switch to Test Mode" button as secondary — outlined
   border, not filled. It should be noticeable but not compete with
   "Submit Answer" for attention.


========================================================================
ITEM 4: VIDEO CONFIG FILE + YOUTUBE SEARCH FALLBACK
========================================================================

Priority: MEDIUM — lesson videos don't load.

CURRENT STATE:
Lesson videos are stored as YouTube URLs in the database via
seed_lessons.py. Many URLs are dead or placeholder. The YouTube search
fallback from earlier rounds may not be working consistently.

NEW APPROACH — TWO-TIER VIDEO SYSTEM:

TIER 1: Curated video config file
Create a JSON config file that maps node_ids to curated YouTube video
URLs. The owner (John) will populate this manually with good free
content (Khan Academy, Math and Science Tutor, etc.).

1. Create file: backend/data/lesson_videos.json

   {
     "frac-simplify": {
       "title": "Simplifying Fractions",
       "videos": [
         {
           "url": "https://www.youtube.com/watch?v=DnFrOetuUKg",
           "title": "Simplifying Fractions - Khan Academy",
           "source": "Khan Academy"
         }
       ]
     },
     "frac-add-like": {
       "title": "Adding Fractions (Like Denominators)",
       "videos": []
     }
   }

   Include ALL 30 node_ids with empty "videos" arrays. John will fill
   them in later. For now, add placeholder entries for a few topics
   using well-known Khan Academy videos if you can find valid URLs,
   but it's fine to leave them all empty.

2. Create an endpoint: GET /api/lessons/{node_id}/videos
   - Reads from lesson_videos.json
   - Returns the videos array for that node_id
   - Returns empty array if node_id not found

3. Update the lesson page (LessonPage.jsx) video section:
   - First, try to load videos from /api/lessons/{node_id}/videos
   - If videos exist, show the first one as an embedded YouTube player
   - If multiple videos exist, show a list below the player so the
     student can switch between them
   - If no videos exist (empty array), show Tier 2 fallback

TIER 2: YouTube search fallback
When no curated video exists for a topic:

1. Show a clean placeholder box with:
   - Text: "No curated video available for this topic yet."
   - A search bar with a pre-filled query: "[topic name] algebra tutorial"
   - A "Search YouTube →" button that opens a new tab with the search

2. The search bar should be editable so the student can refine their
   search query before clicking.

3. The YouTube search URL format:
   https://www.youtube.com/results?search_query=[encoded query]

4. Below the search bar, show 2-3 suggested search links for common
   free math resources:
   - "Search Khan Academy: [topic]" →
     https://www.youtube.com/results?search_query=khan+academy+[topic]
   - "Search Organic Chemistry Tutor: [topic]" →
     https://www.youtube.com/results?search_query=organic+chemistry+tutor+[topic]
   - "Search Professor Leonard: [topic]" →
     https://www.youtube.com/results?search_query=professor+leonard+[topic]

   These open in new tabs. No API needed.

IMPLEMENTATION NOTES:
- The JSON file should be readable without a database migration
- The endpoint should load the file fresh each request (or cache with
  a short TTL) so John can edit the file and see changes without
  restarting the server
- The frontend should gracefully handle the endpoint being unavailable
  (fall back to Tier 2)


========================================================================
IMPLEMENTATION ORDER
========================================================================

1. Item 1 — Specific AI error messages
2. Item 2 — Fix mastery → knowledge map propagation
3. Item 3 — Move "Ready to Test" button next to Submit
4. Item 4 — Video config file + YouTube search fallback

After each item:
  1. Rebuild: docker compose up --build
  2. Test in browser
  3. Commit and push


========================================================================
TESTING AFTER ALL ITEMS
========================================================================

AI ERRORS:
  [ ] Enter an API key with no credits → see "credit balance too low"
      message with link to billing page
  [ ] Enter an invalid API key → see "Invalid API key" message
  [ ] Enter a valid API key with credits → AI chat works

MASTERY → DASHBOARD:
  [ ] Master a topic in Test Mode (3+ correct answers)
  [ ] See 🏆 mastery celebration
  [ ] Click "See Results" or "Finish Session"
  [ ] Navigate to dashboard → mastered node has changed color
  [ ] A new topic is unlocked (was locked, now ready)

TEST MODE BUTTON:
  [ ] In Learning Mode, "Switch to Test Mode →" visible next to Submit
  [ ] Clicking it switches to Test Mode
  [ ] In Test Mode, "Back to Learning" link visible

VIDEOS:
  [ ] Lesson page with a curated video → video plays
  [ ] Lesson page without curated video → YouTube search fallback shows
  [ ] Search bar is pre-filled with topic name
  [ ] "Search YouTube →" opens new tab with correct URL
  [ ] Khan Academy / OCT / Professor Leonard links work
