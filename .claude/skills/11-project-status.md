# Project Status

**Trigger:** "status", "what's the state of", "where are we with"

**What to do:**
1. Read `project.yaml` and show a friendly status summary:

   "Here's where we are with **ProjectName**:

   ✅ Requirements ingested (5 files, Feb 9)
   ✅ Overview & questions generated
   ✅ Breakdown created (32 stories, 145 days)
   ✅ Pushed to ADO (32 stories + tasks)
   ⬜ Feature code — not generated yet
   ✅ Product document — last updated Feb 9

   Change requests: 2 processed

   **Next step:** Say 'generate code for story #XXX' to scaffold a feature branch with frontend code, API contract, and review guide."

2. Include staleness warnings if any artifacts are out of date.
3. Always suggest the logical next action.
