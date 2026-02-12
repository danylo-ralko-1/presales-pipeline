# Push to ADO

**Trigger:** "push to ADO", "create work items", "push stories"

**Pre-checks:**
- Breakdown must exist (`output/breakdown.json`). If not: "I need a breakdown first. Say 'create breakdown'."
- ADO credentials must be configured in `project.yaml` (`ado.organization`, `ado.project`, `ado.pat`). If not: "I need ADO credentials. What's your organization name, project name, and Personal Access Token?"
- If breakdown changed since last push, warn.

**What to do:**

This skill has TWO phases: you generate the story details, then the Python script pushes to ADO.

## Phase 1: Generate push_ready.json (YOU do this)

Read `projects/<ProjectName>/output/breakdown.json` and `projects/<ProjectName>/output/overview.md`.

For EVERY story in the breakdown, generate:
- `user_story`: "As a [role], I want to [action], so that [benefit]."
- `acceptance_criteria`: array of 2-4 brief scope-level AC strings

**Rules for user story text:**
- Clear, specific "As a... I want to... so that..." format
- The role should match the user roles identified in the overview
- The action should describe what the user does, not how it's built
- The benefit should tie to a business outcome

**Rules for lightweight AC:**
- 2-4 brief criteria per story — just enough to define SCOPE, not implementation
- Focus on WHAT the story delivers, not HOW it should be built
- No UI specifics (exact field names, button labels, error messages) — those come from Figma later
- Keep each AC to 1 sentence
- For backend/infra stories, be more specific since they don't depend on designs

**Example:**
```json
{
  "id": "US-003",
  "title": "User Login",
  "user_story": "As a registered user, I want to log in with my email and password, so that I can access my dashboard.",
  "acceptance_criteria": [
    "Users can authenticate with email and password credentials.",
    "Invalid credentials show an appropriate error message.",
    "Successful login redirects to the user's dashboard.",
    "Session persists across page refreshes until explicit logout."
  ],
  "fe_days": 2,
  "be_days": 2,
  "devops_days": 0,
  "design_days": 1,
  "risks": "...",
  "comments": "...",
  "assumptions": "..."
}
```

Write the full structure to `projects/<ProjectName>/output/push_ready.json`. Same format as `breakdown.json` but with `user_story` and `acceptance_criteria` (as array) added to every story.

## Phase 2: Push to ADO (Python script)

Run: `python3 ~/Downloads/presales-pipeline/presales push <ProjectName>`

The script reads `push_ready.json` and creates the following hierarchy in ADO:
- **Epics** → **Features** → **User Stories** (with the AC you generated)
- **Tasks** under each User Story for each required discipline:
  - `[FE] <Story Title>` — if the story has frontend effort > 0
  - `[BE] <Story Title>` — if the story has backend effort > 0
  - `[DevOps] <Story Title>` — if the story has DevOps effort > 0
  - Design tasks are NOT created

**Story Description format** (the script builds this):
```html
<p><em>As a [role], I want to [action], so that [benefit].</em></p>

<table>
<tr><td><b>Epic</b></td><td>{epic name}</td></tr>
<tr><td><b>Feature</b></td><td>{feature name}</td></tr>
</table>
```

**AC format** (the script builds this from the array):
```html
<ol>
<li>First AC</li>
<li>Second AC</li>
</ol>
```

**Effort:** `Microsoft.VSTS.Scheduling.Effort` = total days (FE + BE + DevOps + Design)

The script saves `output/ado_mapping.json` mapping local IDs to ADO IDs. This mapping is saved incrementally (after each item) so progress isn't lost on failure.

## Phase 3: Report & Next Steps

After the script completes, report what was created (epics, features, stories, tasks).

Tell the user:
"Stories and tasks are in ADO with basic acceptance criteria. When your designer has Figma screens ready, say 'validate designs' and share the Figma link — I'll compare them against the stories and find any gaps."

## Phase 4: Auto-update Product Document

After successful push, regenerate the product document (see skill 10-product-document) to reflect the new stories.