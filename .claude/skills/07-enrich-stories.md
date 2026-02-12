# Enrich Stories with Designs

**Trigger:** "enrich stories", "add detailed AC", "update stories from designs", "designs are ready"

**Pre-checks:**
- ADO credentials must be configured and stories must exist in ADO. If no credentials: "I need ADO credentials. What's your organization, project, and PAT?" If connected but no stories: "I connected to ADO but didn't find any user stories."
- Figma credentials required (`figma.pat` in project.yaml). Same handling as validation.
- If user specifies story IDs, confirm: "I'll enrich just stories 720 and 721. Is that right?"

**What to do:**

This skill uses the **screenshot-based approach**: Python fetches screenshots, you analyze them with vision to write detailed AC.

## Step 1: Gather Data (Python)

Run: `python3 ~/Downloads/presales-pipeline/presales enrich <ProjectName> --figma-link <url>`
(Add `--story-ids 720,721` for targeted mode)

This does:
- Reuses existing screenshots from `output/screenshots/` if available from a previous validation run
- Only fetches fresh screenshots if none exist
- Fetches all ADO stories (or filtered set) with current AC
- Saves bundle to `output/enrichment_bundle.json`

## Step 2: Match Screens to Stories (YOU do this)

Read the bundle JSON. For each story, identify which screenshot(s) show its UI by:
- Comparing story title and AC to visible screen content
- Matching screen names to story themes
- Using any mapping data from a previous validation run

## Step 3: Generate Detailed AC Using Vision

For each story that has a matching screenshot, look at the image and write **4-7 grouped acceptance criteria**:

**Rules for detailed AC:**
- Reference SPECIFIC elements you can see: exact field names, button labels, placeholder text
- Include validation rules visible in the design (required markers, format hints)
- Include error/loading/empty states if separate screens show them
- Include responsive behavior if multiple screen sizes exist
- Each criterion 1-3 sentences, written like developer notes
- No Given/When/Then format

**Example of good detailed AC:**
```
1. Login form has Email (required, placeholder "you@company.com") and Password (required, type password) fields. Submit button "Sign In" is disabled until both fields have content.
2. Validation: email must be valid format, password min 8 chars. Errors show inline below each field on blur. Form-level error banner appears on failed authentication.
3. "Forgot password?" link navigates to /reset-password. "Create account" link navigates to /signup. Social login buttons for Google and Microsoft are below the form divider.
4. Loading state: "Sign In" button shows spinner and becomes disabled during API call. Success redirects to /dashboard.
```

## Step 4: Present Changes for Approval

Show each story:
```
ADO #720: User Login
  Matched screen: Login Page
  Current AC: (show brief version)
  Proposed AC:
    1. [detailed AC 1]
    2. [detailed AC 2]
    ...
```

Also list:
- **Stories skipped** (no matching screen) — these will be enriched in a future run
- **Unmatched screens** (potential new stories)

**WAIT for user approval before making any changes.**

## Step 5: On Approval — Update ADO

For each approved story, update ADO using `core.ado`:

- Update ONLY `Microsoft.VSTS.Common.AcceptanceCriteria` field
- Format as HTML ordered list: `<ol><li>AC 1</li><li>AC 2</li>...</ol>`
- Do NOT modify the Description field
- Confirm each update with ADO ID

Use the Python ADO module — never raw curl:
```python
python3 -c "
from core.config import load_project
from core.ado import from_project, update_work_item
p = load_project('<ProjectName>')
c = from_project(p)
update_work_item(c, <ADO_ID>, {
    'Microsoft.VSTS.Common.AcceptanceCriteria': '<ol><li>AC 1</li><li>AC 2</li></ol>'
})
"
```

## Step 6: Next Steps

Tell the user:
"Acceptance criteria are updated in ADO. The stories are now dev-ready. You can:
1. **'generate specs'** for developer handoff
2. Continue enriching more stories as new designs come in"

## Step 7: Auto-update Product Document

Regenerate the product document (see skill 10-product-document) to reflect the enriched acceptance criteria.

---

**Incremental mode:** If user specifies story IDs, only those stories are processed. Useful when designers deliver screens in batches.

**Key principle:** Screenshots give you everything you need for AC writing. Only use Figma MCP node reads if you need data you literally cannot see (hidden layers, component variant names).