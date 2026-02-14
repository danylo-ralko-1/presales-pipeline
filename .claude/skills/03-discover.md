# Generate Overview & Questions

**Trigger:** "generate overview", "analyze requirements", "create client questions", "what should we ask the client"

**Pre-checks:**
- Requirements must be ingested. If not: "I need to ingest requirements first. Drop the files here in the chat or put them in the input folder."
- If requirements were re-ingested since last overview, warn about staleness.

**What to do:**

## Step 1: Generate overview.md
Read `requirements_context.md` and generate a structured scope summary covering:
- Business problem and desired solution
- Functional scope (grouped by feature area)
- User roles and permissions
- Data model / term fields
- Non-functional requirements
- Timeline, deliverables, risks & dependencies
- Items marked TBD or uncertain

Save to `projects/<ProjectName>/output/overview.md`.

## Step 2: Generate questions.txt (client-ready email)

Generate clarification questions formatted as a **ready-to-send email** — not a technical document.

### Rules:

1. **Maximum 15 questions.** Prioritize questions that have the biggest impact on:
   - Architecture decisions (affects how the system is built)
   - Effort estimation (could swing the estimate significantly)
   - Timeline (blocks progress if unanswered)

   Skip nice-to-have questions that can be figured out later during development.

2. **Email format.** Structure the output like this:
   - **Greeting** — 1-2 sentences: what document we reviewed, what we're asking for
   - **Questions** — grouped into 3-4 simple, non-technical categories (e.g., "How the app should work", "Users & permissions", "Data & migration", "Technical setup"). NOT labels like "NFRs" or "Auth & SSO"
   - **Closing** — friendly note offering to jump on a quick call to go through the questions together

3. **Tone & language:**
   - Friendly, professional — write for a business stakeholder, not a developer
   - Each question should be short and clear (1-2 sentences max)
   - No sub-options (a/b/c/d) unless absolutely necessary for clarity
   - Avoid technical jargon. Examples:
     - Instead of "Is WCAG AA a hard requirement?" → "How important is accessibility for users with disabilities — is this a must-have for launch?"
     - Instead of "Confirm Azure AD / Entra ID for SSO" → "Can your IT team set up single sign-on so employees log in with their existing company accounts?"
     - Instead of "Should Sub-domains have a parent-child relationship with Domains?" → "When someone picks a domain (like Finance), should the sub-domain list automatically narrow down to match, or are they independent choices?"

4. **Overflow:** If there are more than 15 important questions, pick the top 15 for the email and save the rest in `projects/<ProjectName>/output/additional-questions.md` with a note that these are lower-priority items for internal tracking.

Save the email to `projects/<ProjectName>/output/questions.txt`.

## Step 3: Present results
1. Show a brief summary of the overview
2. Show the full questions email
3. If additional-questions.md was created, mention it
4. **Next steps:** "Two things to do now: (1) Review the overview — does it match your understanding? (2) Send the questions to the client. When you get answers, drop the response here in the chat or save it in `projects/<ProjectName>/answers/`. Then say 'create breakdown'."
