# Generate Implementation Specs

**Trigger:** "generate specs", "create YAML specs", "implementation specs", "generate specs for Claude Code"

**Pre-checks:**
- ADO credentials must be configured and stories must exist in ADO. If no credentials: "I need ADO credentials. What's your organization, project, and PAT?" If connected but no stories: "I connected to ADO but didn't find any user stories to generate specs for."
- If stories have only basic/lightweight AC, suggest: "Stories have basic AC — the specs will be more useful if you enrich the stories with Figma designs first. Want to do that, or proceed with what we have?"

**What to do:**

This skill runs ENTIRELY in conversation. You generate the spec YAML files directly, then use a Python utility to upload them to ADO.

## Step 1: Read Inputs

**ADO is the single source of truth.** Always read current story data from ADO.

1. Fetch current ADO stories with full descriptions and AC:
   `python3 -c "from core.config import load_project; from core.ado import from_project, get_all_work_items; import json; p=load_project('<ProjectName>'); c=from_project(p); print(json.dumps(get_all_work_items(c), indent=2))"`
2. Read `projects/<ProjectName>/output/ado_mapping.json` — to map stories to their `[FE]` and `[BE]` task ADO IDs
3. If `output/validation_bundle.json` exists, read it for Figma screen-to-story mappings and file_key

## Step 2: For Each Story, Generate Two Specs

Process stories that have FE or BE tasks. Skip stories with no FE and no BE effort.

For targeted mode (`--story-ids 720,721`), only process specified stories.

### FE Spec (saved to `output/specs/fe/<story_id>_<safe_title>.yaml`)

Generate a YAML spec focused on frontend concerns:

```yaml
story:
  title: "Story title"
  ado_id: 720
  epic: "Epic name"
  feature: "Feature name"

figma:
  link: "https://www.figma.com/design/{file_key}?node-id={node_id}"
  instructions: "Use Figma MCP to read this screen for exact layout, spacing, and component details."

components:
  - name: "ComponentName"
    type: "page | component | modal | layout"
    path: "src/components/path/ComponentName.tsx"
    description: "What this component does"
    props:
      - name: "propName"
        type: "string"
        required: true
        description: "What this prop controls"
    state:
      - name: "stateName"
        type: "type"
        initial: "initial value"
    events:
      - name: "onEventName"
        trigger: "What triggers this"
        action: "What happens"

api_contract:
  consumes:
    - method: "GET"
      path: "/api/v1/resource"
      description: "What this endpoint returns"
      request:
        params: []
      response:
        success: { status: 200, body: {} }
        errors:
          - { status: 404, condition: "Not found" }

ui_states:
  - state: "loading"
    behavior: "Show skeleton loader for the data table"
  - state: "empty"
    behavior: "Show empty state with call-to-action"
  - state: "error"
    behavior: "Show error banner with retry button"

validations:
  - field: "email"
    rules: ["required", "email format"]
    error_message: "Please enter a valid email"

testing_notes:
  - "Verify responsive layout at 768px and 1024px breakpoints"
  - "Test keyboard navigation through form fields"
```

### BE Spec (saved to `output/specs/be/<story_id>_<safe_title>.yaml`)

Generate a YAML spec focused on backend concerns:

```yaml
story:
  title: "Story title"
  ado_id: 720
  epic: "Epic name"
  feature: "Feature name"

api_endpoints:
  - method: "POST"
    path: "/api/v1/resource"
    description: "What this endpoint does"
    auth: true
    request:
      headers: { "Content-Type": "application/json" }
      body:
        field_name:
          type: "string"
          required: true
          validation: "min:1, max:255"
    response:
      success:
        status: 201
        body: { id: "uuid", created_at: "timestamp" }
      errors:
        - status: 400
          condition: "Validation failed"
          body: { message: "Field X is required" }
        - status: 409
          condition: "Duplicate resource"
          body: { message: "Resource already exists" }

database:
  tables:
    - name: "table_name"
      columns:
        - name: "id"
          type: "UUID"
          primary: true
        - name: "field_name"
          type: "VARCHAR(255)"
          nullable: false
          index: true
  migrations:
    - description: "Create table_name table with indexes"

business_logic:
  - rule: "Description of business rule"
    implementation: "How to implement it"
  - rule: "Validation rule"
    implementation: "Details"

integration_points:
  - service: "External service name"
    type: "REST API"
    details: "What data flows where"

testing_notes:
  - "Test validation for all required fields"
  - "Test concurrent creation with unique constraint"
```

**Rules for spec generation:**
- Include ONLY what's needed for THIS story — don't spec the entire application
- API endpoints should include all possible error responses
- Validations should match the acceptance criteria exactly
- Be specific about file paths — use a consistent project structure
- If a story has no backend, skip BE spec. If no frontend, skip FE spec.
- FE specs reference the API as a **consumer** (what to call). BE specs define the API as a **provider** (full contract).

**Figma integration in FE specs:**
- If validation_bundle.json exists, find the screen node_id mapped to this story
- Construct the Figma link: `https://www.figma.com/design/{file_key}?node-id={node_id}`
- Include it in the `figma` section with instructions for developers to use Figma MCP
- If no mapping exists, try to extract Figma links from the ADO story description
- Do NOT embed screenshots — reference the live Figma file

## Step 3: Save Spec Files

Create directory structure:
```
output/specs/
├── fe/
│   ├── US-001_dev-environment-setup.yaml
│   ├── US-003_user-login.yaml
│   └── ...
└── be/
    ├── US-003_user-login.yaml
    ├── US-005_data-import.yaml
    └── ...
```

Use safe filenames: replace special characters, limit to 80 chars.

## Step 4: Upload to ADO

Run: `python3 ~/Downloads/presales-pipeline/presales specs-upload <ProjectName>`

This uploads each spec file as an attachment to the corresponding task in ADO:
- FE spec → attached to the `[FE] Story Title` task
- BE spec → attached to the `[BE] Story Title` task

If the upload command doesn't exist yet, tell the user: "Spec files are saved locally. The ADO upload utility isn't wired up yet — you can attach them manually or I can help build that."

## Step 5: Report & Next Steps

Report: "Generated X FE specs and Y BE specs. Saved to output/specs/ and attached to ADO tasks."

Tell the user:
"Specs are ready for developers. Frontend devs download the FE spec from their `[FE]` task, backend devs download the BE spec from their `[BE]` task. Each pastes it into Claude Code and says 'implement this'."