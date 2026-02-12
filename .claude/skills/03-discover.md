# Generate Overview & Questions

**Trigger:** "generate overview", "analyze requirements", "create client questions", "what should we ask the client"

**Pre-checks:**
- Requirements must be ingested. If not: "I need to ingest requirements first. Drop the files here in the chat or put them in the input folder."
- If requirements were re-ingested since last overview, warn about staleness.

**What to do:**
1. Run `python3 ~/Downloads/presales-pipeline/presales discover <ProjectName>`
2. Show a brief summary of the overview
3. Show the questions that were generated
4. **Next steps:** "Two things to do now: (1) Review the overview — does it match your understanding? (2) Send the questions to the client. When you get answers, drop the response here in the chat or save it in `projects/<ProjectName>/answers/`. Then say 'create breakdown'."