# New User Stories for GlossaryTest

## ADO #720: [Terms] Complete Empty State (No Data in System)

**State:** New
**Priority:** High
**Story Type:** User Story

### User Story
As a user, When I navigate to the Glossary application that has no terms loaded from the system at all, I want to see a clear empty state with appropriate messaging, So that I understand that the application is working correctly but simply has no data yet, rather than thinking there is an error.

### Description
This story addresses the true "empty state" when the glossary application has zero terms in the system (different from "no search results"). This is distinct from ADO #712 which may have been intended for this purpose but is not clearly specified.

### Acceptance Criteria
- [ ] When the glossary has NO terms loaded from Informatica API (zero terms in system)
- [ ] Display an empty state illustration/graphic in the main content area
- [ ] Show clear messaging: "No terms available yet" or similar user-friendly text
- [ ] Provide context: "Terms will appear here once they are loaded from the system"
- [ ] The search bar, filters, and alphabetical navigation should either be:
  - Hidden in empty state, OR
  - Visible but disabled with appropriate tooltips
- [ ] Empty state should be visually centered in the content area
- [ ] Design should follow existing design system patterns for empty states

### Technical Notes
- This is different from the "No results" state which shows when search/filter returns empty
- Backend should return empty array when no terms exist
- Frontend should detect empty data set and render empty state component

### Dependencies
- Requires design in Figma (currently missing)
- Depends on ADO #711 (API integration) being partially complete

### Estimated Effort
- **Design:** 0.25 days
- **Frontend:** 0.5 days
- **Backend:** 0.25 days (API response handling)
- **Testing:** 0.25 days
- **Total:** 1.25 days

---

## ADO #721: [Terms] Alphabetical Quick Navigation

**State:** New
**Priority:** Medium
**Story Type:** User Story

### User Story
As a user, When I am viewing the Glossary with many terms, I want to quickly navigate to terms starting with a specific letter by clicking on alphabetical buttons (A-Z), So that I can quickly jump to the section of terms I need without scrolling through the entire list.

### Description
Alphabetical navigation bar (A-Z buttons) is present in the Figma design below the search/filter area. This feature allows users to quickly jump to terms starting with a specific letter, improving navigation efficiency for large glossaries.

### Acceptance Criteria
- [ ] Display A-Z letter buttons in a horizontal row below the search/filter area
- [ ] Each letter button should be clearly visible and clickable
- [ ] Clicking a letter button should:
  - Jump/scroll the table to the first term starting with that letter
  - Highlight or indicate the active letter
- [ ] Letters that have no terms should be:
  - Visually disabled (grayed out or reduced opacity)
  - Non-clickable
- [ ] Active letter state should be clearly visible (highlight, underline, or color change)
- [ ] Navigation should work with current filters applied (only jump to letters that have visible terms after filtering)
- [ ] Smooth scroll behavior when jumping to a letter section
- [ ] The alphabetical navigation should remain visible (consider sticky behavior with header per ADO #716)

### Technical Notes
- Design already exists in Figma (Main Screen)
- Backend may need to provide letter availability in API response
- Consider performance with very large datasets (virtual scrolling)
- Should integrate with existing scroll behavior

### Dependencies
- ADO #714 (Grid Table) must be complete
- May depend on ADO #716 (Sticky header) for optimal UX

### Estimated Effort
- **Design:** 0 days (already in Figma)
- **Frontend:** 1 day
- **Backend:** 0.5 days (API enhancement to return letter availability/counts)
- **Testing:** 0.5 days
- **Total:** 2 days

---

## ADO #722: [Terms] Add "Last Update" Column to Grid

**State:** New
**Priority:** High
**Story Type:** Change Request / Enhancement

### User Story
As a glossary user, When I review the list of terms in the grid table, I want to see a "Last Update" column showing when each term was last modified, So that I can quickly identify which terms have recent changes and determine if the information is current.

### Description
This story implements the requirement from ADO #718 but provides more specific acceptance criteria about WHERE and HOW the "Last Update" should be displayed. The column should be added to the main grid table.

### Acceptance Criteria
- [ ] Add "Last Update" column to the grid table
- [ ] Column should be positioned after "Subject Area" column (rightmost position)
- [ ] Display format: "MM/DD/YYYY" or "Month DD, YYYY" (follow existing date format standards)
- [ ] Column should be sortable (ascending/descending) with sort indicator
- [ ] Show relative time for recent updates: "Today", "Yesterday", "2 days ago" for items updated within last 7 days
- [ ] For older items, show full date
- [ ] Column header should have sort arrow/indicator
- [ ] Tooltip on hover should show full timestamp: "Last updated: MM/DD/YYYY HH:MM AM/PM"
- [ ] Column should be included in table export functionality (if exists)
- [ ] "Last Update" filter may be added to top filter area (optional - discuss with team)

### Technical Notes
- Backend API must return lastUpdateDate field for each term
- Frontend should handle date formatting and relative time calculation
- Consider timezone handling (display in user's local timezone or UTC)
- Sort functionality should work on actual datetime, not formatted string

### Dependencies
- ADO #711 (API Integration) must include lastUpdateDate field
- ADO #714 (Grid Table) must be complete
- Design update needed in Figma

### Estimated Effort
- **Design:** 0.25 days (add column to Figma)
- **Frontend:** 0.75 days (column addition, date formatting, sorting)
- **Backend:** 0.5 days (ensure API returns lastUpdateDate)
- **Testing:** 0.5 days
- **Total:** 2 days

---

## ADO #723: [Terms] Add "Term Type" Column to Grid

**State:** New
**Priority:** High
**Story Type:** Change Request / Enhancement

### User Story
As a glossary user, I want to view and filter term types directly within the main data grid as a column, So that I can quickly see the type of each term and filter by type without using the separate top filter section.

### Description
This story implements the requirement from ADO #719. The "Term Type" should be moved from being only a top filter dropdown to being a visible column in the grid table. This provides better visibility and allows for grid-level filtering.

### Acceptance Criteria
- [ ] Add "Term Type" column to the grid table
- [ ] Column should be positioned between "Sub-Domain" and "Subject Area" columns
- [ ] Display term type values: "Policy", "KPI", "Master Data", "Business Term", etc.
- [ ] Column should be sortable (A-Z, Z-A) with sort indicator
- [ ] Column should have inline filter capability (dropdown or multi-select in column header)
- [ ] Filter dropdown should show all available term types with counts (e.g., "Policy (15)")
- [ ] Multiple term types can be selected simultaneously for filtering
- [ ] Selected filters should be clearly indicated in the column header
- [ ] Clear filter button should be available when filters are active
- [ ] The top "Term Type" dropdown filter should be:
  - **Option A:** Removed entirely (recommended), OR
  - **Option B:** Kept but synchronized with grid column filter

### Design Considerations
- Follow existing grid column design patterns
- Filter dropdown should match existing filter UI components
- Consider column width (term type names may vary in length)

### Technical Notes
- Backend API already returns term type data (visible in dropdown)
- Frontend needs to add column and implement grid-level filtering
- If keeping top dropdown, ensure state synchronization between top filter and grid filter
- Consider performance with multiple active filters

### Dependencies
- ADO #714 (Grid Table) must be complete
- ADO #715 (Grid Filtration) functionality should be extended
- Design update needed in Figma (add column, possibly remove top dropdown)

### Related Stories
- ADO #719 - Original requirement (may be marked as duplicate or closed when this is complete)
- ADO #717 - Similar pattern (hiding top-level filter)

### Estimated Effort
- **Design:** 0.5 days (add column, update filter area)
- **Frontend:** 1.5 days (column addition, grid-level filtering, state management)
- **Backend:** 0.25 days (ensure proper API support)
- **Testing:** 0.75 days
- **Total:** 3 days

---

## ADO #724: [Terms] Expandable Stakeholder Details

**State:** New
**Priority:** Low
**Story Type:** Enhancement

### User Story
As a user, When I view a term row in the glossary that has multiple stakeholders, I want to be able to expand the stakeholder cell to see the full list of stakeholders, So that I can see all stakeholders without the information being truncated.

### Description
The Figma design shows small dropdown arrows in some stakeholder cells, suggesting expandable/collapsible functionality. This story formalizes that feature. When multiple stakeholders are associated with a term, the cell should support expansion to show all stakeholders.

### Acceptance Criteria
- [ ] When a term has 2 or more stakeholders, display them in a truncated format: "Stakeholder1, Stakeholder2, ..." with a dropdown arrow icon
- [ ] Clicking the dropdown arrow or cell should expand to show full list of stakeholders
- [ ] Expanded view should show each stakeholder on a separate line or in a clear list format
- [ ] Clicking again should collapse the list back to truncated view
- [ ] Only one row should be expanded at a time (expanding a new row collapses the previous)
- [ ] Alternative: Tooltip on hover showing all stakeholders (discuss with UX team)
- [ ] If only one stakeholder exists, no dropdown arrow should be shown
- [ ] Expansion should not break table layout or cause horizontal scrolling
- [ ] Smooth animation for expand/collapse transition

### Design Considerations
- Confirm if expansion is inline (row height grows) or as an overlay/popover
- Ensure expanded state is clearly visible
- Consider mobile/responsive behavior

### Technical Notes
- Design appears to have this feature but details are unclear from static screenshots
- May need to verify in Figma prototypes or with designer
- Consider if expansion affects sorting/filtering behavior
- Performance consideration: limit number of stakeholders displayed even when expanded

### Dependencies
- ADO #714 (Grid Table) must be complete
- Requires design clarification/documentation in Figma

### Open Questions
- Should this be inline expansion or popover/tooltip?
- Maximum number of stakeholders to display when expanded?
- Should there be a "View all stakeholders" link if there are many?

### Estimated Effort
- **Design:** 0.5 days (clarify behavior, document interaction)
- **Frontend:** 1 day (expansion logic, state management, animation)
- **Backend:** 0 days (assumes stakeholder data already available)
- **Testing:** 0.5 days
- **Total:** 2 days

---

## Summary of New Stories

| Story ID | Title | Priority | Estimated Effort | Status |
|----------|-------|----------|------------------|--------|
| ADO #720 | Complete Empty State (No Data) | High | 1.25 days | New |
| ADO #721 | Alphabetical Quick Navigation | Medium | 2 days | New |
| ADO #722 | Add "Last Update" Column | High | 2 days | New |
| ADO #723 | Add "Term Type" Column | High | 3 days | New |
| ADO #724 | Expandable Stakeholder Details | Low | 2 days | New |

**Total Estimated Effort:** 10.25 days

---

## Recommended Story Updates

### ADO #717: [Terms] [CR] Hide "Associated Data Set" dropdown
**Recommendation:** Update story to clarify:
- Should the dropdown be completely removed from the design?
- Or should it be hidden conditionally (e.g., only when no options available)?
- Current design still shows the dropdown prominently

**Suggested AC Addition:**
- [ ] Remove "Associated Data Set" dropdown from top filter area completely, OR
- [ ] Hide dropdown when no data sets are available (display: none)
- [ ] Update Figma design to reflect this change

### ADO #716: [Terms + FAQ] [CR] Stick header area
**Recommendation:** Add specific acceptance criteria:

**Suggested AC Addition:**
- [ ] The header area (search bar, filters, alphabetical navigation) should remain fixed at the top when scrolling down the page
- [ ] The sticky header should activate after scrolling past the "Glossary" page title
- [ ] Smooth transition when header becomes sticky
- [ ] Z-index should ensure sticky header appears above table content
- [ ] Sticky behavior should work on all supported screen sizes
- [ ] Performance: sticky scroll should not cause lag or jank

### ADO #719: [Terms] [CR] Move "Term Type" Filter to Grid View
**Recommendation:** This story can be replaced by ADO #723 (above) which provides more detailed acceptance criteria. Mark ADO #719 as "Duplicate" and reference ADO #723.

---

## Next Steps

1. **Review** these new stories with the product owner and stakeholders
2. **Prioritize** stories based on business value and dependencies
3. **Update Figma** designs to include missing elements (empty state, Last Update column, Term Type column)
4. **Refine estimates** with the development team during sprint planning
5. **Update existing stories** (#716, #717, #719) with clarified acceptance criteria
6. **Add stories to backlog** and assign to appropriate sprint

---

*Generated from Design Validation Report - GlossaryTest Project*
*Date: 2026-02-09*
