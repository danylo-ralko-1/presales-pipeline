# US Business Term Glossary — Product Document

## 1. Overview

The **US Business Term Glossary** is an internal web application that provides a centralized, searchable repository of business terms used across the US Member Firm. The application synchronizes data daily from **Informatica** (the organization's data governance platform) and presents it in a clean, filterable grid interface.

The primary goal is to enable employees to quickly look up business terms, understand their definitions, identify stakeholders, and see how terms are categorized within the organizational taxonomy (Domain > Sub-Domain > Subject Area).

**Target users:** All employees within the US Member Firm who have a Company account.

**Access URL:** glossary.Company.com

**Authentication:** Company SSO (Microsoft-based)

---

## 2. Architecture & Data Flow

### 2.1 Data Source

All glossary data originates from the **Informatica** data governance platform. A scheduled **cron job** runs daily at **9:00 AM EST** to fetch an export file containing:

- Term names
- Term descriptions
- Stakeholder security groups
- Hierarchical classification paths (Domain / Sub-Domain / Subject Area)
- Term type classifications (Master Data, KPI, Transactional, Policy, Regulatory, Undesignated)

### 2.2 Data Mapping

| Grid Column | Informatica Source Field |
|---|---|
| Term | `Name` |
| Description | `Description` |
| Stakeholder(s) | Names from all stakeholder security groups except "SG-US-CDGC Data Steward" |
| Domain | 1st value in `HierarchicalPath` |
| Sub-Domain | 2nd value in `HierarchicalPath` |
| Subject Area | 3rd value in `HierarchicalPath` |

### 2.3 Search Infrastructure

The application uses **Azure Search** for intelligent search capabilities, supporting both exact matches and semantic similarity (e.g., searching "Car" may return results containing "Vehicle").

---

## 3. Application Structure

The application consists of two main pages:

| Page | URL Path | Description |
|---|---|---|
| **Glossary (Terms)** | `/` (default) | Searchable grid of all business terms |
| **FAQ** | `/faq` | Frequently asked questions with collapsible answers |

Both pages share a common header with navigation tabs.

---

## 4. Global Layout & Navigation

### 4.1 Header Bar

- **Black background** spanning the full width
- **Left side:** "US Business Term Glossary" application name
- **Right side:** "Glossary" and "FAQ" tab navigation; active tab is visually highlighted
- **User profile icon** on the far right (provides access to logout)

### 4.2 User Authentication & Logout

- Users authenticate via Company SSO (Microsoft)
- Clicking the profile icon opens a dropdown showing: profile picture, full name, and a "Log Out" button
- Logout follows the standard Company Microsoft logout flow (Microsoft logout screen > Company-branded confirmation > login screen)

### 4.3 Sticky Header Behavior

When the user scrolls down on either page, the entire header area remains fixed at the top of the viewport. This includes:

- Header bar with navigation
- Page title
- Search bar and filter controls
- Alphabet bar (Glossary page only)

Only the content area (grid / FAQ items) scrolls underneath.

---

## 5. Glossary Page (Terms)

### 5.1 Page Layout (Top to Bottom)

1. **Header bar** (black) with app name + tab navigation
2. **Page title**: "Glossary" in large white text on black background
3. **Search bar**: input field with search options (see 5.2)
4. **Filter dropdowns**: "Term Type" dropdown (see 5.4)
5. **Alphabet bar**: clickable A–Z letters
6. **Grid table**: scrollable data grid with terms

### 5.2 Search

**Search field** is positioned above the grid with the following elements:

- Magnifying glass icon (left side of input)
- Text input with dynamic placeholder
- **X (clear) icon**: appears when 1+ characters are entered; clears the input and restores the grid
- **Toggle buttons** on the right side: "All" (default) | "Term" | "Description"

**Placeholder text** changes based on the selected toggle:

| Toggle | Placeholder |
|---|---|
| All | "Search Term & Description" |
| Term | "Search Term" |
| Description | "Search Description" |

**Search behavior** (triggers at 3+ characters):

- **Exact matches**: matching text portions are highlighted with a **yellow background** in the relevant column(s)
- **Similar matches** (via Azure Search): displayed without highlight
- **No results**: centered illustration (magnifying glass with X), bold text "No results for '{value}'", and a green "Reset Search" link

**Search scope by toggle:**

| Toggle | Searches in | Highlights in |
|---|---|---|
| All | Term + Description | Both columns |
| Term | Term only | Term column only |
| Description | Description only | Description column only |

**Live update**: results update dynamically as the user types/deletes characters (as long as 3+ characters remain).

**Filter combination**: search applies only within the scope of any active filters (alphabet, column filters, dropdowns).

### 5.3 Search Alphabet Navigation

When search results span multiple letter groups, **clickable alphabet letter pills** appear below the search bar:

- Only letters with matching results are shown (e.g., A, C, M, W)
- Clicking a letter filters results to that letter group; active pill is highlighted
- A "Cancel" link dismisses the letter filter and shows all results

### 5.4 Filter Dropdowns

**Term Type** dropdown in the header area:

- Options: Master Data, KPI, Transactional, Policy, Regulatory, Undesignated
- Multi-select with checkboxes, "Select All", "Apply" / "Cancel"
- When active, shows selected values as comma-separated text with an X to clear

> **Note:** An "Associated Data Set" dropdown exists in earlier designs but is **hidden** per Change Request #743. The underlying code should retain the functionality for potential future re-enablement.

### 5.5 Column Value Filtering

The following columns have **filter funnel icons** in their headers:

- Stakeholder(s)
- Domain
- Sub-Domain
- Subject Area

**Filter dropdown behavior:**

- Search field to find values
- "Select All" checkbox
- Scrollable list of unique values with checkboxes
- "Apply" / "Cancel" buttons

**Stakeholder(s) column** has additional behavior:
- Selected filters are shown as **removable chips** below the column header (e.g., "Danylo Petrenko X", "Oleksii Ivanov X")
- If more than 2 values selected, a **"+N" counter** appears

### 5.6 Alphabet Bar

A horizontal row of clickable letters **A through Z** is displayed below the search/filter area. Clicking a letter filters the grid to show only terms starting with that letter.

### 5.7 Grid Table

**Columns:**

| Column | Style | Max Width | Filter |
|---|---|---|---|
| Term | Blue hyperlink | 240px | No |
| Description | Black text (gray when truncated) | No max | No |
| Stakeholder(s) | Comma-separated names | 320px | Yes (funnel) |
| Domain | Regular text | 160px (fixed) | Yes (funnel) |
| Sub-Domain | Regular text | 160px (fixed) | Yes (funnel) |
| Subject Area | Regular text | 160px (fixed) | Yes (funnel) |

- **Minimum column width**: 160px for all columns
- **Side gaps** by resolution: 1280px → 32px, 1440px → 74px, 1920px → 120px

**Alphabet grouping:**
- Terms are sorted A–Z
- A **letter header** (e.g., "A", "B") appears on the left before the first term in each group
- **Longer dividers** separate letter groups; thinner dividers separate rows within the same group

**Row truncation & expand/collapse:**
- If any column value exceeds 3 lines, remaining text appears in lighter gray
- A **down-arrow (v)** icon is centered below the row
- Clicking expands the row to full content; icon becomes **up-arrow (^)**
- Clicking again collapses back to 3-line truncation

**Sticky column headers:**
- When scrolling, the column title row stays fixed at the top of the grid area

**Infinite scroll:**
- Initial load: 25 terms
- Scrolling to the bottom triggers loading the next batch (small circular spinner shown)
- Loading should take less than one second

### 5.8 "Last Update" Label

A label is displayed on the Glossary page showing the last synchronization timestamp:

**Format:** `Last Update: Saturday, May 31 at 11:59 AM CT`

This reflects the last time the platform synchronized with Informatica, regardless of whether new data was received.

### 5.9 Empty / Loading States

| State | Display |
|---|---|
| **Loading** | Centered spinner with "Searching..." text |
| **Empty (no data)** | Grid with column headers visible, no rows |
| **No search results** | Illustration + "No results for '{value}'" + "Reset Search" link |

---

## 6. FAQ Page

### 6.1 Layout

- Same header bar as Glossary page (black background, tab navigation with "FAQ" active)
- **Page title**: "FAQ" in large white text
- **Search field**: placeholder "Search Question & Answer"
- **Content area**: accordion-style FAQ items grouped by category

### 6.2 FAQ Categories & Items

FAQ items are organized into collapsible sections:

- **About glossary**: "How does it work?", "What types of terms can I find?", "Can I use the glossary offline?"
- **Features & usage**: "How do I search for a specific term?", "Can I suggest a new term?", "Can I bookmark or favorite terms?", "How are definitions reviewed or verified?", "Is there a way to see related or similar terms?"
- **Collaboration & teams**: "Can teams create shared glossaries?", "Can I restrict who sees or edits certain terms?", "Can I track changes or version history for a definition?"

Each item has a **chevron icon**; clicking expands to reveal the answer.

### 6.3 Submit Question

A **"Submit question"** button is fixed at the bottom-left of the page. Clicking opens a modal dialog with:

- **Topic** (required): dropdown to select a topic
- **Question** (required): textarea to type the question
- **Submit** / **Cancel** buttons

---

## 7. Change Request Log

| CR # | Title | Description | Status |
|---|---|---|---|
| #742 | Sticky header area | Header + search/filter area stays sticky on scroll (both pages) | New |
| #743 | Hide "Associated Data Set" | Hide the dropdown from filter bar and right-side menu (keep code for future use) | New |
| #744 | Show "Last Update" label | Display last Informatica sync timestamp on Glossary page | New |
| #745 | Move "Term Type" Filter to Grid View | Move the Term Type filter into the grid view area | New (no AC) |

---

## 8. Known Design Gaps

| Gap | Related Story | Severity |
|---|---|---|
| No user profile icon in header | #738 | Medium |
| No logout dropdown or flow designed | #738 UC2, UC3 | Medium |
| "Associated Data Set" dropdown still visible in Figma | #743 / Bug #749 | High |
| "Last Update" label not present in Figma designs | #744 | High |
| Right-side term details panel not designed | #743 UC2 | Medium |
| Missing 1440px and 1920px responsive design variants | #740 UC2 | Low |
| Story #745 has no acceptance criteria yet | #745 | Medium |

---

## 9. ADO Work Item Index

### Epic: Glossary Application (Phase 1) — #735

#### Feature: Terms Page — #736

| ID | Type | Title |
|---|---|---|
| #737 | User Story | [Terms] Informatica API Integrations |
| #738 | User Story | [Terms] Page Empty State |
| #739 | User Story | [Terms] Grid Search |
| #740 | User Story | [Terms] Grid Table |
| #742 | User Story | [Terms + FAQ] [CR] Stick header area |
| #743 | User Story | [Terms] [CR] Hide "Associated Data Set" dropdown and attribute |
| #744 | User Story | [Terms] [CR] Show "Last Update" label |
| #745 | User Story | [Terms] [CR] Move "Term Type" Filter to Grid View |
| #746 | User Story | [FAQ] FAQ Page Layout & Content |
| #747 | User Story | [Terms] Column Value Filtering |
| #748 | User Story | [Terms] Search Alphabet Navigation |
| #749 | Bug | [Terms] [Design Bug] "Associated Data Set" dropdown not hidden in Figma |

---

*Document generated from ADO work items and Figma design validation on 2026-02-11.*
