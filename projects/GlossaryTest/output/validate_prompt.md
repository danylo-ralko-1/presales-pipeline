# Design Validation: GlossaryTest

## What This Does
Compares Figma designs against ADO user stories to find:
- Missing designs (stories without corresponding screens)
- Incomplete designs (screens missing elements from acceptance criteria)
- Inconsistencies (mismatched labels, fields, flows, states)
- Untracked design elements (in Figma but no ADO story — potential scope creep)

## Prerequisites
- The official Figma MCP is connected in Claude Code
  ```
  /mcp
  figma · ✓ connected
  ```
- Figma file is accessible: https://www.figma.com/design/xo7gE69nspbRI8yDMo1waf

## Instructions

Paste everything below the line into Claude Code:

---

You are performing a design validation for the **GlossaryTest** project.
Your task: Compare the Figma designs against Azure DevOps user stories to find inconsistencies.

## Step 1: Read Figma Designs

Use the figma MCP to read the design file at this link:
https://www.figma.com/design/xo7gE69nspbRI8yDMo1waf

For each page in the file:
1. Get the page structure and list all top-level frames (these are screens)
2. For each screen, extract:
   - Frame name and dimensions
   - All child elements: type, text content, labels, placeholders, button text
   - Component instances and their variants
   - Any state variations (error states, loading states, empty states)

Build a structured inventory like:
```
Screen: "Login Page"
  Elements:
  - Heading: "Welcome back"
  - Input: label="Email", placeholder="you@company.com"
  - Input: label="Password", type=password
  - Button: "Sign In", variant=primary
  - Link: "Forgot password?"
  States: [default, error, loading]
```

## Step 2: ADO User Stories

Here are the current user stories from Azure DevOps:

### ADO #711: [Terms] Informatica API Integrations
**State:** New
**Description:**
As a user, When I review the Glossary application page, I want to see this page being populated with data, So that I can review the terms and their meanings.

### ADO #712: [Terms] Page Layout and Authentication
**State:** New
**Description:**
As a user, When I navigate to the Glossary application, which does not have any data, I want to see the empty state of the page, So that I know that currently no data has been added to the system.

### ADO #713: [Terms] Grid Search
**State:** New
**Description:**
As a user, I want to be able to search for the needed terms, So that I can easily find the term I need.

### ADO #714: [Terms] Grid Table
**State:** New
**Description:**
As a user, When I navigate to the Glossary application, I want to see the Grid Table with the list of Terms, So that I can easily understand the meaning of the Term I am interested in.

### ADO #716: [Terms + FAQ] [CR] Stick header area
**State:** New
**Description:**
As a user, I want to constantly see the headers area with the Search/Filtration options, So that I can easily search/filter page content even after scrolling the page.

### ADO #717: [Terms] Associated Data Set Filtering
**State:** New
**Description:**
As a user, I want to filter terms by their associated data sets, So that I can find terms related to specific data sources or applications.

### ADO #718: [Terms] Last Update Backend Support
**State:** New
**Description:**
As a developer, I want the backend to track and expose the last synchronization timestamp, So that we can display data freshness information in future releases.

### ADO #719: [Terms] Term Type Filtering
**State:** New
**Description:**
As a glossary user, I want to filter terms by their type using the header dropdown, So that I can quickly find Master Data, KPIs, Policies, or other term categories.

### ADO #720: [FAQ] Submit Question Modal
**State:** New
**Description:**
As a user, I want to submit my own questions when I can't find an answer in the FAQ, so that I can get help with specific issues not covered in the standard FAQ. Epic Glossary Platform Feature FAQ Management

### ADO #724: [FAQ] FAQ Content Management
**State:** New
**Description:**
As an administrator, I want to manage FAQ content through a backend system, so that I can update FAQ questions and answers without code deployments. Epic Glossary Platform Feature FAQ Management

### ADO #727: [Terms] Advanced Stakeholder Filtering
**State:** New
**Description:**
As a user, I want to filter terms by specific stakeholders using a multi-select dropdown, so that I can find all terms associated with particular team members or stakeholder groups. Epic Glossary Platform Feature Terms Grid Filtering

### ADO #730: [Terms] Alphabetical Quick Navigation
**State:** New
**Description:**
As a user, I want to quickly jump to terms starting with a specific letter, so that I can navigate large term lists more efficiently. Epic Glossary Platform Feature Terms Grid Filtering

### ADO #733: [FAQ] FAQ Page Layout and Navigation
**State:** New
**Description:**
As a user, I want to access a dedicated FAQ page with organized question categories, so that I can find answers to common questions about the Glossary application. Epic Glossary Platform Feature FAQ Management


## Step 3: Project Context

Requirements summary:


Overview:


## Step 4: Cross-Reference

For EACH Figma screen:
1. Identify which ADO story/stories it implements
2. Read that story's acceptance criteria
3. Check every AC line against the design:
   - Does the screen have the required fields/buttons/elements?
   - Do labels and text match what the AC specifies?
   - Are error states designed if AC mentions validation?
   - Are loading/empty states designed if AC mentions data fetching?
4. Note any design elements that have NO corresponding AC (potential scope creep)

For EACH ADO story:
1. Find the corresponding Figma screen(s)
2. If no screen exists and the story needs UI → critical gap
3. If screen exists but is incomplete → list what's missing
4. If the story is backend-only → skip (no design expected)

## Step 5: Generate Report

### ✅ Fully Matched
Screens that align with all acceptance criteria. List each screen and its matching stories.

### 🔴 Missing Designs
ADO stories that need UI but have no Figma screen.
For each: story ID, title, what screen is expected.
**Action:** Create the missing screen in Figma.

### 🟡 Incomplete Designs
Screens that exist but are missing elements from acceptance criteria.
For each: screen name, story ID, specific missing elements or states.
**Action:** Add the missing elements to the Figma screen.

### 🟠 Inconsistencies
Both exist but don't match — wrong labels, missing fields, incorrect flow, missing states.
For each: screen name, story ID, what AC says vs what Figma shows.
**Action:** Update Figma OR update the ADO story (specify which).

### 🔵 Untracked Design Elements
Elements in Figma with no corresponding ADO story. Should they be:
- Added as a new story in ADO
- Removed from Figma (scope creep)
- Ignored (structural element like navigation, headers)

### Summary Table
| Category | Count |
|---|---|
| Fully matched | X |
| Missing designs | X |
| Incomplete designs | X |
| Inconsistencies | X |
| Untracked elements | X |

### Proposed New Stories
For any new stories needed:
- Title
- Epic / Feature
- Brief acceptance criteria
- Estimated effort (FE/BE/DevOps/Design days)

### Proposed Story Modifications
For stories that need AC updates:
- Story ID and title
- What to change
- Effort impact (if any)

---

Present this report and WAIT for my review.
Do NOT make any changes to ADO or Figma until I approve.

