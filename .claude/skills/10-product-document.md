# Generate / Update Product Document

**Trigger:**
- Explicitly: "generate product document", "create PRD", "update the document", "what does the app look like now"
- Automatically: after ANY of these actions complete successfully:
  - Push to ADO (skill 05)
  - Change request approved and applied (skill 08)
  - Validation approved, if that optional skill was invoked (skill 06)

**What this produces:**
Two Wiki pages in Azure DevOps — a Product Overview for newcomers and a Change Requests page for tracking scope evolution.

**Pre-checks:**
- Stories must exist (in ADO or breakdown.json). If not: "I need stories to generate the document. Run the pipeline through at least the push step."

**What to do:**

1. **Fetch all current data:**
   - All ADO stories with descriptions and acceptance criteria
   - Epic/feature hierarchy
   - Change request history from `project.yaml`
   - Figma mapping if available (to reference design links)

2. **Generate two documents:**

   ### Document 1: Product Overview (`product_overview.md`)

   This is the "what is this project" document. Anyone new to the project reads this first.

   ```markdown
   # [Project Name] — Product Overview

   **Last updated:** [timestamp]
   **Stories:** [count] across [epic count] functional areas

   ## Introduction
   2-3 paragraphs: what this application is, who it's for, what problem it solves,
   the business context.

   ## User Roles
   All user types with descriptions and what parts of the app they access.

   ## Architecture Overview
   High-level description of the system architecture — frontend/backend split,
   key technologies (if known from requirements), integrations with external systems,
   deployment model. Keep it conceptual, not implementation-specific.

   ## Data Flow
   How data moves through the system — what the user inputs, how it gets processed,
   where it's stored, what comes out. Describe the main data entities and their
   relationships.

   ## Functional Areas

   ### [Epic Name]
   Overview of this functional area — what it delivers to users, which features
   it contains, and how they relate.

   #### [Feature Name]
   Description of what this feature group covers and the user value it provides.
   Summarize the key behaviors without listing every story individually.

   ## Key User Flows
   End-to-end flows that span multiple features. Describe the journey, not
   individual acceptance criteria.
   ```

   **What NOT to include in Product Overview:**
   - No full list of ADO tickets/stories
   - No individual story IDs or AC details
   - No change request history (that goes in the other document)

   ### Document 2: Change Requests (`change_requests.md`)

   This tracks every scope change that happened after the initial baseline.

   ```markdown
   # [Project Name] — Change Requests

   **Last updated:** [timestamp]
   **Total change requests:** [count]

   ## Summary
   Brief overview of how the project scope has evolved since the initial baseline.

   ## Change Requests

   ### CR-{N}: [Change Title]
   - **Date:** [YYYY-MM-DD]
   - **Description:** What was requested and what changed
   - **Reason:** Why this change was needed (from project.yaml or ADO Change Log)
   - **Impact:** Stories added, modified, or marked outdated
   - **ADO Links:**
     - [Story Title](https://dev.azure.com/{org}/{project}/_workitems/edit/{id}) — [created/modified/outdated]
     - [Story Title](https://dev.azure.com/{org}/{project}/_workitems/edit/{id}) — [created/modified/outdated]

   ### CR-{N-1}: [Change Title]
   ...
   ```

   List change requests in reverse chronological order (newest first). Each CR links to every ADO ticket it touched. If a story was created, modified, or marked outdated by the CR, note that next to the link.

   If there are no change requests yet, write: "No change requests have been processed. This document will be updated when scope changes occur."

3. **Save locally and publish to ADO Wiki:**

   a. Save `output/product_overview.md` and `output/change_requests.md` locally.

   b. **Get or create the project Wiki.** Use the ADO Wiki REST API via the Python `core.ado` module:
      - `GET https://dev.azure.com/{org}/{project}/_apis/wiki/wikis?api-version=7.1` to list existing wikis
      - If a project wiki exists (type `projectWiki`), use it
      - If no project wiki exists, create one:
        ```
        POST https://dev.azure.com/{org}/{project}/_apis/wiki/wikis?api-version=7.1
        Body: { "name": "{project}.wiki", "type": "projectWiki" }
        ```
      - Save the wiki ID in `project.yaml` under `state.wiki_id`

   c. **Create or update the Wiki pages.** The page structure in the wiki:
      ```
      /Product Documentation              ← parent page (can be minimal or a TOC)
      /Product Documentation/Product Overview
      /Product Documentation/Change Requests
      ```

      Use `PUT` to create or update each page:
      ```
      PUT https://dev.azure.com/{org}/{project}/_apis/wiki/wikis/{wikiId}/pages?path={pagePath}&api-version=7.1
      Headers:
        Content-Type: application/json
        If-Match: {eTag}          ← required for updates, omit for creation
      Body: { "content": "{markdown content}" }
      ```

      - For **new pages** (first time): omit `If-Match`, the page is created.
      - For **existing pages** (updates): first GET the page to retrieve its `eTag`, then PUT with `If-Match: {eTag}` to update.
      - GET a page: `GET https://dev.azure.com/{org}/{project}/_apis/wiki/wikis/{wikiId}/pages?path={pagePath}&includeContent=true&api-version=7.1`

   d. Save the wiki page paths in `project.yaml` under:
      - `state.wiki_overview_path: /Product Documentation/Product Overview`
      - `state.wiki_changes_path: /Product Documentation/Change Requests`

4. **Report:**
   ```
   Product documentation published to ADO Wiki:
   - Product Overview: https://dev.azure.com/{org}/{project}/_wiki/wikis/{wikiName}/Product-Documentation/Product-Overview
   - Change Requests: https://dev.azure.com/{org}/{project}/_wiki/wikis/{wikiName}/Product-Documentation/Change-Requests

   What changed: [brief summary]
   ```

   Always include the direct Wiki URLs so the user can click through.

**Auto-update behavior:**
When auto-triggered after another skill completes, Claude should:
1. Read the existing `output/product_overview.md` and `output/change_requests.md` if they exist
2. Regenerate both documents from current ADO data
3. If the trigger was a change request, add a new CR entry to the Change Requests document
4. Update both Wiki pages in ADO (GET eTag first, then PUT with updated content)
5. Show a brief summary with Wiki links: "Updated product documentation: [what changed]."

**Important:** The documents must reflect the ACTUAL current state in ADO, not what was planned. If a story was modified by a change request, the overview reflects the modified version. The Change Requests document tracks the full history of what changed and when.
