# Generate Breakdown & Estimates

**Trigger:** "create breakdown", "estimate the project", "generate stories", or when the user drops client answers and says something like "here are the answers, create the breakdown"

**Pre-checks:**
- Overview must exist (`output/overview.md`). If not: "I need to analyze the requirements first. Say 'generate overview' to start."
- If `answers/` folder has new files since last breakdown, mention: "I see new client answers. I'll factor those into the estimates."
- If overview was regenerated since last breakdown, warn about staleness.

**If the user drops client answer files in the chat:**
1. Copy each file to `projects/<ProjectName>/answers/`
2. Confirm: "Saved the client answers. I'll factor them into the breakdown."
3. Proceed with breakdown — don't make them say "create breakdown" separately

**What to do:**

This skill runs ENTIRELY in conversation. You read files, generate the breakdown JSON, and save it. Then run a Python script only for Excel export.

## Step 1: Read Inputs

1. Read `projects/<ProjectName>/output/overview.md`
2. Read `projects/<ProjectName>/output/requirements_context.md`
3. Read any files in `projects/<ProjectName>/answers/` (if they exist)
   - If no answers: use reasonable defaults and mark assumptions

## Step 2: Generate Epic/Feature/Story Structure

Analyze the requirements, overview, and client answers. Generate the hierarchy:

**Rules for structure:**
- Aim for 30-40 user stories total. If the project is complex, consolidate related work into broader stories rather than splitting into granular tasks.
- Epics group major functional areas (Authentication, Search, Content Management, etc.)
- Features are sub-areas within an epic (Login, Password Reset, SSO within Authentication)
- Stories are specific deliverable units within a feature
- Each story should be independently deliverable and testable
- First epic should always be "Technical Setup" with stories for dev environment, CI/CD, and database schema

## Step 3: Add Details and Estimates to Every Story

For each story, determine:
- `title`: clear, descriptive story title
- `acceptance_criteria`: brief scope-level AC (1-2 sentences — detailed AC comes later from Figma)
- `fe_days`: frontend effort in days
- `be_days`: backend effort in days
- `devops_days`: DevOps effort in days (0 for most stories)
- `design_days`: UI/UX design time (0 for purely technical stories)
- `risks`: primary risk or concern
- `comments`: technical notes, dependencies, implementation hints
- `assumptions`: what we're assuming to be true for this estimate

**Estimation guidelines:**
- FE (days): UI components, state management, API integration, responsive behavior
- BE (days): API endpoints, business logic, data validation, database queries
- DevOps (days): Infrastructure, CI/CD, deployment config, monitoring. Most stories are 0.
- Design (days): UI/UX design time. 0 for purely technical stories.
- Minimum granularity is 0.5 days. A trivial task is 0.5, not 0.
- A "day" = ~6 productive hours
- Be realistic. A login form is not 5 days of FE work. A complex search with filters is not 0.5 days.
- Include stories for error handling, loading states, and edge cases — these are real work.

## Step 4: Save breakdown.json

Write the result to `projects/<ProjectName>/output/breakdown.json` in EXACTLY this format:

```json
{
  "epics": [
    {
      "id": "EP-001",
      "name": "Technical Setup",
      "description": "Infrastructure and environment setup",
      "features": [
        {
          "id": "FT-001",
          "name": "Environment Setup",
          "stories": [
            {
              "id": "US-001",
              "title": "Development Environment Configuration",
              "acceptance_criteria": "Dev environment with hot reload, linting, and test runner configured for both FE and BE.",
              "fe_days": 1,
              "be_days": 1,
              "devops_days": 0.5,
              "design_days": 0,
              "risks": "Team may have different local setups",
              "comments": "Use Docker for consistency. Include README with setup instructions.",
              "assumptions": "Team uses VS Code or compatible IDE"
            }
          ]
        }
      ]
    }
  ]
}
```

**Critical:** The JSON must be valid and parseable. Use proper escaping for quotes in text fields.

## Step 5: Export to Excel

Run: `python3 ~/Downloads/presales-pipeline/presales breakdown-export <ProjectName>`

This converts `breakdown.json` → `breakdown.xlsx` with formatting. If the command doesn't exist yet, skip this step and note it.

## Step 6: Update State

Update `projects/<ProjectName>/project.yaml`:
- Set `state.breakdown_generated: true`
- Set `status: "estimation"`

## Step 7: Show Summary

Present the summary to the user:

```
Breakdown complete:
- X epics, Y features, Z stories
- Total effort: N days
  - FE: X days
  - BE: X days  
  - DevOps: X days
  - Design: X days

Top epics:
- Epic Name: X stories, Y days
- Epic Name: X stories, Y days
...
```

## Step 8: Next Steps

Tell the user:
"The breakdown is ready. You can:
1. **'push to ADO'** to create work items in Azure DevOps
2. Ask me to **adjust specific estimates** if anything looks off
3. Review the Excel file at `output/breakdown.xlsx`"