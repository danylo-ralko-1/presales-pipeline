# New User Stories from Design Validation
## GlossaryTest Project

Generated: 2026-02-11
Source: Figma validation - untracked design elements

---

## Story 1: [FAQ] FAQ Page Layout and Navigation

**Epic**: Glossary Platform
**Feature**: FAQ Management

**Title**: [FAQ] FAQ Page Layout and Navigation

**Description**:
As a user,
I want to access a dedicated FAQ page with organized question categories,
So that I can find answers to common questions about the Glossary application.

**Acceptance Criteria**:

1. **FAQ Page Structure**: Create a new FAQ page accessible from the main navigation. The page includes a header section with search/filter capabilities matching the Terms page layout, and the main content area displays FAQ sections in a collapsible accordion format.

2. **FAQ Section Organization**: Display three main FAQ sections: "About glossary", "Features & usage", and "Collaboration & teams". Each section contains multiple questions, with section headers clearly visible and distinguishable from individual questions.

3. **Collapsible Question Behavior**: Each question can be independently expanded or collapsed. When clicked, the question expands to reveal the answer text below. Multiple questions can be open simultaneously. The expand/collapse icon updates to reflect the current state (chevron down when collapsed, chevron up when expanded).

4. **Visual Hierarchy**: Section headers use bold, larger text with a divider line below. Individual questions use standard weight text with adequate spacing. Expanded answers display in a slightly muted text color to distinguish from questions. All sections and questions have consistent padding and alignment.

5. **Submit Question Button**: Display a "Submit question" button at the bottom of the FAQ page. The button is prominently styled and fixed to the bottom-right area, remaining visible as users scroll through FAQ content.

**Effort Estimate**:
- Frontend: 2 days
- Backend: 0 days (static content initially)
- DevOps: 0 days
- Design: 0 days (already complete)
- **Total**: 2 days

---

## Story 2: [FAQ] Submit Question Modal

**Epic**: Glossary Platform
**Feature**: FAQ Management

**Title**: [FAQ] Submit Question Modal

**Description**:
As a user,
I want to submit my own questions when I can't find an answer in the FAQ,
So that I can get help with specific issues not covered in the standard FAQ.

**Acceptance Criteria**:

1. **Modal Trigger and Layout**: When the user clicks the "Submit question" button, display a modal dialog overlaying the current page. The modal includes a semi-transparent backdrop, is centered on screen, and contains a title "Submit question" at the top with a close (X) icon in the upper-right corner.

2. **Topic Selection Field**: Include a required "Topic" dropdown field marked with an asterisk (*). The dropdown displays "Select your topic" as placeholder text. Available topic options match the FAQ sections: "About glossary", "Features & usage", "Collaboration & teams", and "Other".

3. **Question Input Field**: Include a required "Question" textarea field marked with an asterisk (*). The textarea displays "Type your question" as placeholder text, allows multi-line input, and expands to accommodate up to 500 characters. Character count indicator shows remaining characters.

4. **Modal Actions and Validation**: Display "Submit" and "Cancel" buttons at the bottom of the modal. Submit button is disabled until both required fields are completed. Clicking Cancel or the X icon closes the modal without submitting. Clicking Submit validates inputs and displays a confirmation message.

5. **Form Submission Handling**: On successful submission, close the modal, display a success toast notification "Your question has been submitted. We'll respond within 2 business days." Store the submitted question with timestamp and user information for review by support team.

**Effort Estimate**:
- Frontend: 1.5 days
- Backend: 2 days (submission endpoint, storage, notification)
- DevOps: 0.5 days (email notification setup)
- Design: 0 days (already complete)
- **Total**: 4 days

---

## Story 3: [FAQ] FAQ Content Management

**Epic**: Glossary Platform
**Feature**: FAQ Management

**Title**: [FAQ] FAQ Content Management

**Description**:
As an administrator,
I want to manage FAQ content through a backend system,
So that I can update FAQ questions and answers without code deployments.

**Acceptance Criteria**:

1. **FAQ Data Model**: Create a database schema for FAQ content with fields: id, section (enum: About, Features, Collaboration), question, answer, display_order, is_active, created_date, last_updated. Support hierarchical organization with sections containing multiple questions.

2. **API Endpoints**: Provide GET endpoint to retrieve all active FAQ items grouped by section and ordered by display_order. Support filtering by section. Include metadata like last_updated timestamp to enable client-side caching.

3. **Content Initialization**: Populate the FAQ database with initial content matching the Figma designs. Include at least 3 questions per section covering common topics: how the glossary works, search capabilities, collaboration features, and data update frequency.

4. **Future Admin Interface**: Structure the backend to support future admin functionality for adding, editing, reordering, and deactivating FAQ items. All CRUD operations should validate data integrity and maintain audit logs of changes.

**Effort Estimate**:
- Frontend: 0 days
- Backend: 2.5 days
- DevOps: 0.5 days (database migration)
- Design: 0 days
- **Total**: 3 days

---

## Story 4: [Terms] Advanced Stakeholder Filtering

**Epic**: Glossary Platform
**Feature**: Terms Grid Filtering

**Title**: [Terms] Advanced Stakeholder Filtering

**Description**:
As a user,
I want to filter terms by specific stakeholders using a multi-select dropdown,
So that I can find all terms associated with particular team members or stakeholder groups.

**Acceptance Criteria**:

1. **Stakeholder Display Format**: In the Stakeholder(s) column, display stakeholder names as tags/chips with proper truncation. When more than 3 stakeholders are assigned to a term, show the first 2 names followed by a "+N" indicator (e.g., "Danylo Petrenko" "Oleksii Ivanov +3").

2. **Stakeholder Filter Dropdown**: Add a "Stakeholder" dropdown filter in the header area alongside existing filters. The dropdown displays a searchable list of all stakeholders in the system with checkboxes for multi-selection. Include a "Select All" option at the top and "Apply"/"Cancel" buttons at the bottom.

3. **Multi-Select Filter Logic**: Users can select multiple stakeholders. Clicking "Apply" filters the grid to show only terms that have at least one of the selected stakeholders. The filter indicator shows the count of selected stakeholders (e.g., "Stakeholder (2)"). Clicking "Cancel" closes the dropdown without applying changes.

4. **Column-Level Stakeholder Filter**: Add a filter icon in the Stakeholder(s) column header. Clicking this icon opens a similar multi-select dropdown scoped to stakeholders visible in the current filtered results. Column filter behavior stacks with the header filter.

5. **Filter State Persistence and Clearing**: Selected stakeholder filters persist during the session when navigating away and returning to the Terms page. Display an "X" icon next to the filter name when active, allowing users to quickly clear the stakeholder filter. When cleared, the grid returns to showing all terms.

**Effort Estimate**:
- Frontend: 2 days
- Backend: 1 day (stakeholder list endpoint, filter query logic)
- DevOps: 0 days
- Design: 0 days (already complete)
- **Total**: 3 days

---

## Story 5: [Terms] Alphabetical Quick Navigation

**Epic**: Glossary Platform
**Feature**: Terms Grid Filtering

**Title**: [Terms] Alphabetical Quick Navigation

**Description**:
As a user,
I want to quickly jump to terms starting with a specific letter,
So that I can navigate large term lists more efficiently.

**Acceptance Criteria**:

1. **Alphabet Navigation Bar**: Display a horizontal row of letter buttons (A-Z) below the search/filter area and above the grid table. Each letter represents the first character of term names. Letters with no associated terms are displayed in a disabled/muted state.

2. **Letter Selection Behavior**: Clicking an active letter filters the grid to show only terms starting with that letter. The selected letter is highlighted with a different background color to indicate the active filter. The letter grouping headers in the grid remain visible to maintain context.

3. **Quick Letter Filter Integration**: When performing a search that returns results across multiple letters, display a quick filter bar showing only the letters that have matching results (e.g., "A", "C", "M", "W" with a "Cancel" button). Clicking a letter further filters results to that letter. Clicking "Cancel" removes the letter filter but keeps the search active.

4. **Filter Combination Logic**: Alphabetical filtering works in combination with other filters (search, stakeholder, term type, etc.). When multiple filters are active, the alphabet bar shows only letters that have terms matching all active filters. Disabled letters update dynamically as other filters change.

5. **Clear Navigation and State**: Display a clear indicator when a letter filter is active (highlighted button + count of terms shown). Clicking the same letter again or clicking a "Clear" button removes the alphabetical filter. The URL updates to include the selected letter for bookmarking and sharing.

**Effort Estimate**:
- Frontend: 2 days
- Backend: 0.5 days (query optimization for letter counts)
- DevOps: 0 days
- Design: 0 days (already complete)
- **Total**: 2.5 days

---

## Summary of New Stories

| Story ID | Title | Epic | Feature | Total Effort |
|----------|-------|------|---------|--------------|
| TBD | [FAQ] FAQ Page Layout and Navigation | Glossary Platform | FAQ Management | 2 days |
| TBD | [FAQ] Submit Question Modal | Glossary Platform | FAQ Management | 4 days |
| TBD | [FAQ] FAQ Content Management | Glossary Platform | FAQ Management | 3 days |
| TBD | [Terms] Advanced Stakeholder Filtering | Glossary Platform | Terms Grid Filtering | 3 days |
| TBD | [Terms] Alphabetical Quick Navigation | Glossary Platform | Terms Grid Filtering | 2.5 days |

**Total Additional Effort**: 14.5 days

**Breakdown by Discipline**:
- Frontend: 7.5 days
- Backend: 6 days
- DevOps: 1 day
- Design: 0 days (all designs already complete in Figma)

---

## Next Steps

1. **Review and Approve**: Review these story proposals and provide feedback
2. **Adjust Estimates**: Modify effort estimates if needed based on team velocity
3. **Create in ADO**: Push approved stories to Azure DevOps
4. **Link to Designs**: Attach Figma screenshots to each story in ADO
5. **Update Project State**: Update project.yaml to reflect the new scope

---

## Notes

- All designs for these features are already complete in Figma
- FAQ feature represents the largest scope addition (~9 days)
- Stakeholder and alphabet filtering are smaller enhancements (~5.5 days combined)
- No design work is needed - only implementation
- These stories align with existing patterns and don't introduce new technical dependencies
