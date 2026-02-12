# Generate / Update Product Document

**Trigger:**
- Explicitly: "generate product document", "create PRD", "update the document", "what does the app look like now"
- Automatically: after ANY of these actions complete successfully:
  - Push to ADO (skill 05)
  - Validation approved and stories created/modified (skill 06)
  - Enrichment approved and AC updated (skill 07)
  - Change request approved and applied (skill 08)

**What this document is:**
A comprehensive, always-current description of the entire application — what it does, how it works, every feature, every screen, every user flow. Think of it as the single source of truth that anyone (new BA, PM, developer, stakeholder) can read to understand the full product.

**Pre-checks:**
- Stories must exist (in ADO or breakdown.json). If not: "I need stories to generate the document. Run the pipeline through at least the push step."

**What to do:**

1. **Fetch all current data:**
   - All ADO stories with descriptions and acceptance criteria
   - Epic/feature hierarchy
   - Change request history from `project.yaml`
   - Figma mapping if available (to reference design links)

2. **Generate the document** by calling Claude with all stories organized by epic/feature. The document structure:

   ```markdown
   # [Project Name] — Product Document

   **Last updated:** [timestamp]
   **Stories:** [count] across [epic count] functional areas

   ## Executive Summary
   2-3 paragraphs: what this application is, who it's for, what problem it solves.

   ## User Roles
   All user types with descriptions and what parts of the app they access.

   ## Functional Areas

   ### [Epic Name]
   Overview of this functional area — what it delivers to users.

   #### [Feature Name]
   Description of this feature group.

   **[Story Title]** (ADO #ID)
   - What it does (from description)
   - Key behaviors (from acceptance criteria)
   - Figma: [link if mapped]
   - Status: [New/Active/Closed]

   ## User Flows
   Key end-to-end flows that span multiple stories.

   ## Change Log
   | Date | What changed | Trigger |
   |------|-------------|---------|
   | 2026-02-10 | Added 3 stories from design validation | Validation |
   | 2026-02-09 | Initial document — 32 stories pushed to ADO | Push |
   ```

3. **Save and publish to ADO:**
   - Overwrite `output/product_document.md` locally
   - Append a new row to the Change Log table — do not remove previous rows
   - Find or create an Epic in ADO called **"Product Document"** with tag `product-document;<ProjectName>`
   - Delete any existing file attachments on that Epic (previous versions)
   - Upload the new `product_document.md` as an attachment to the Epic
   - Update the Epic description with the Executive Summary section and a note: "Full document attached. Download the .md file for the complete product description."
   - Save the Epic's ADO ID in `project.yaml` under `state.product_doc_epic_id` for future updates

4. **Report:** "Product document updated and attached to ADO Epic #[id]. What changed: [brief summary]."

**Auto-update behavior:**
When auto-triggered after another skill completes, Claude should:
1. Read the existing `output/product_document.md` if it exists
2. Regenerate the full document from current ADO data
3. Preserve the existing Change Log rows and append a new entry describing what just changed
4. Delete the old attachment from the Product Document Epic in ADO and upload the new file
5. Show a brief summary: "Updated product document: added 3 new stories from validation, updated AC for 5 stories from enrichment."

**Deleting old attachments from ADO:**
To replace the attachment, use the ADO REST API:
1. GET the Epic work item with `$expand=relations` to find existing AttachedFile relations
2. For each relation where `rel == "AttachedFile"`, send a PATCH to remove it:
   ```json
   [{"op": "remove", "path": "/relations/{index}"}]
   ```
3. Then upload and link the new file as usual

**Important:** The document must reflect the ACTUAL current state in ADO, not what was planned. If a story was modified by a change request, the document shows the modified version, not the original. The Change Log at the bottom tracks what changed and when.