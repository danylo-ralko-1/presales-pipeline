# Extract Design System

**Trigger:** "extract design system", "get design tokens", "read the design system from Figma", "design system"

> **Standalone skill.** This is NOT part of the main pipeline flow. It can be run at any time, independently, to capture a project's visual language from Figma. The output (`design-system.md`) is used by the "generate feature code" skill to produce design-aware code.

**Pre-checks:**
- Figma MCP must be available. If not: "I need the Figma MCP connection to read designs. Make sure the Figma MCP server is configured."
- User must provide **1-3 reference screen URLs** from Figma — screens that best represent the app's visual language (e.g., a main dashboard, a form page, a detail page). If not: "Give me 1-3 Figma screen URLs that show the typical look and feel of this app. Pick screens that show the most variety — a list view, a form, a detail page."
- Project name must be known (to save the output). If not: "Which project is this for?"

**What to do:**

This skill connects to Figma via MCP, reads reference screens, and extracts the design system into a structured markdown file. It captures everything a developer needs to write UI code that looks correct without constantly referencing Figma.

**This runs entirely in conversation.** YOU do all analysis using Figma MCP tools. No Python scripts needed.

---

## Step 1: Gather Reference Screens

Ask the user for 1-3 Figma screen URLs. Good reference screens have:
- A variety of UI elements (buttons, inputs, cards, tables, modals)
- Clear typography hierarchy (headings, body, captions)
- Visible spacing and layout patterns
- Different states (active, hover, disabled, error)

Extract the `fileKey` and `nodeId` from each URL.

## Step 2: Read Design Structure from Figma (MCP is the primary source)

**The Figma file structure is the source of truth** — not screenshots. MCP gives exact values, component hierarchy, auto-layout properties, and variable definitions. Use the structural data to extract everything.

### 2a: Read the file-level design system

Call these once per file (not per screen):

1. **`mcp__figma__get_variable_defs`** — get ALL design tokens: color variables, spacing variables, typography variables. This is the definitive token source.
2. **`mcp__figma__get_styles`** — get all named styles (text styles, color styles, effect styles). These define the reusable type scale and color palette.
3. **`mcp__figma__get_local_components`** — get all reusable components defined in the file. These tell you what UI primitives exist (buttons, inputs, cards, badges, etc.) and their variants.

### 2b: Read each reference screen's structure

For each reference screen URL, call these in order:

1. **`mcp__figma__get_design_context`** — the primary tool. Returns the component tree with exact values: auto-layout direction/padding/gap, fill colors, text content, font properties, border radius, effects. This is where you get the page structure, component nesting, and all property values.
2. **`mcp__figma__get_metadata`** — returns the node tree in XML with IDs, types, names, positions, and sizes. Use this to understand the full hierarchy: which frames contain which children, the top-to-bottom arrangement of sections.
3. **`mcp__figma__get_node_info`** — drill into specific nodes when you need details that `get_design_context` didn't cover (e.g., a deeply nested component, a specific variant state).
4. **`mcp__figma__scan_text_nodes`** — scan all text in the screen to capture labels, placeholders, headings, and button text. This tells you the exact copy used in the design.

### 2c: Screenshot as visual reference (supplementary only)

5. **`mcp__figma__get_screenshot`** — take a screenshot of each screen AFTER reading the structural data. Use it only to:
   - Confirm your structural analysis is correct (quick sanity check)
   - Understand spatial relationships that are ambiguous in the node tree
   - See the visual weight and emphasis of elements

**Do NOT extract values from screenshots.** All token values, spacing, colors, and typography must come from the structural MCP data. Screenshots are for validation, not extraction.

## Step 3: Analyze and Extract

From the structural MCP data, extract the following categories. **Every value must come from the Figma node tree or variables — never estimated from a screenshot:**

### Colors
- **Primary palette** — brand colors, primary action color, accent
- **Neutral palette** — backgrounds, borders, text colors (light to dark scale)
- **Semantic colors** — success (green), warning (yellow/amber), error (red), info (blue)
- **Surface colors** — page background, card background, sidebar background, modal overlay
- Use the variable names from Figma if available (e.g., `color/primary/500`, `bg/surface`)

### Typography
- **Font families** — primary (headings), secondary (body), monospace (code)
- **Type scale** — each level with: name, font size, line height, font weight, letter spacing
  - Display / H1 / H2 / H3 / H4 / Body Large / Body / Body Small / Caption / Overline
- **Text colors** — primary text, secondary text, disabled text, link text, inverse text

### Spacing
- **Spacing scale** — the base unit and common values (e.g., 4px base: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64)
- **Component spacing** — padding inside cards, buttons, inputs, modals
- **Layout spacing** — gap between sections, page margins, sidebar width, header height

### Borders & Corners
- **Border widths** — default, focus, divider
- **Border colors** — default, hover, focus, error
- **Border radius** — small (inputs, buttons), medium (cards), large (modals), full (avatars/pills)

### Shadows & Effects
- **Elevation levels** — each shadow with offset, blur, spread, color
  - Level 1 (cards/dropdowns), Level 2 (floating elements), Level 3 (modals)
- **Blur effects** — backdrop blur values if used
- **Transitions** — any visible animation patterns (duration, easing)

### Component Patterns
For each common component found in the Figma node tree and local components, document:
- **Buttons** — variants (primary, secondary, ghost, destructive), sizes (sm, md, lg), states (default, hover, active, disabled, loading)
- **Inputs** — text field, textarea, select, checkbox, radio, toggle — with label position, placeholder style, error state
- **Cards** — padding, border, shadow, header/body/footer pattern
- **Tables** — header style, row height, hover state, borders, sorting indicators
- **Navigation** — top nav, sidebar, tabs, breadcrumbs — active/inactive states
- **Modals/Dialogs** — overlay color, width, padding, header/body/footer layout
- **Badges/Tags** — color variants, size, border radius
- **Icons** — library used, default size, color convention

### Layout Patterns
- **Page layout** — sidebar + content, full width, centered container
- **Grid system** — column count, gutter width, breakpoints
- **Responsive behavior** — if multiple screen sizes exist in Figma, note breakpoints and layout shifts
- **Content width** — max-width for content areas

### Screen Blueprints

**This is the most important section for code generation.** For each reference screen, derive the component structure directly from the Figma node tree (`get_design_context` + `get_metadata`). Walk the top-level frame's children in order — each major child frame is a section of the page.

**How to derive blueprints from the node tree:**
- The top-level frame's immediate children are the page sections (header, content, footer, etc.)
- Each child frame's name and auto-layout properties tell you what it is and how it's arranged
- Text nodes inside give you exact labels, headings, and placeholder text (confirmed by `scan_text_nodes`)
- Component instances reference local components — note which design system primitives are used
- Auto-layout direction (HORIZONTAL/VERTICAL) + padding + gap values tell you the exact layout

For each reference screen, document:

1. **Screen name and purpose** — the frame name from Figma + what page this is
2. **Component inventory (top to bottom)** — walk the node tree's children in order:
   - Frame name and its auto-layout properties (direction, padding, gap)
   - What elements it contains — read from child nodes (text nodes, component instances, nested frames)
   - Exact text content from `scan_text_nodes` (labels, placeholders, headings, button text)
3. **Custom/unique components** — frames or component instances that aren't standard primitives. These are critical because code gen will invent the wrong thing without them. Examples:
   - Alphabet navigation bar (A-Z horizontal strip)
   - Search bar with attached mode toggles (All | Term | Description)
   - Table with letter-based row grouping (A section, B section...)
   - Expandable/collapsible rows with chevrons
   - Status badge with specific color-to-value mapping (Draft=gray, Verified=green, In Review=orange)
4. **Auto-layout hierarchy** — how the page is structured: which frames are fixed/sticky, which scroll, nesting depth
5. **Column/field layout for data-heavy screens** — extract column names from table header text nodes, note column order and relative widths from frame sizes, identify which columns have sort/filter icons

**Example screen blueprint:**
```
### Screen: Glossary Terms Page

**Purpose:** Main listing page for glossary terms with search, filtering, and alphabetical navigation.

**Component inventory (top to bottom):**

1. **App header** (dark background, fixed top)
   - App title "US Business Term Glossary" left-aligned
   - Tab navigation: "Glossary" (active, white bg pill), "FAQ" — horizontal tabs

2. **Page title section**
   - H1: "Glossary"

3. **Search and filter bar** (single horizontal row)
   - Search input with placeholder "Search Term & Description" + search icon
   - Attached toggle buttons: "All" | "Term" | "Description" (radio-style, one active at a time)
   - "Associated Data Set" dropdown filter
   - "Term Type" dropdown filter

4. **Alphabet navigation bar**
   - Horizontal strip of letters A-Z, evenly spaced
   - Clicking a letter scrolls/filters to that section
   - Dark background, white text

5. **Terms table** (grouped by first letter)
   - **Letter group headers:** "A", "B", "C"... as section dividers within the table
   - **Columns:** Term (link, blue), Description (multi-line, truncated with expand chevron), Stakeholder(s), Domain, Sub-Domain, Subject Area
   - **No Status column** in this view
   - Rows are expandable — chevron (▼) below Description to show full text
   - No alternating row colors — separated by light borders
```

**Why this matters:** Without blueprints, code gen sees the AC say "user can search terms" and generates a generic search input above a flat table. With the blueprint, it knows to generate: dark header with tabs → search bar with mode toggles → A-Z strip → letter-grouped table with expandable rows. The difference between "technically correct" and "matches the design."

## Step 4: Generate design-system.md

Write the extracted design system to `projects/<ProjectName>/design-system.md`:

```markdown
# Design System — [Project Name]

**Extracted from:** Figma file [file name]
**Reference screens:** [list of screen names used]
**Date:** [YYYY-MM-DD]

---

## Colors

### Primary
| Token | Value | Usage |
|-------|-------|-------|
| `primary-500` | #3B82F6 | Primary actions, links |
| `primary-600` | #2563EB | Primary hover |
| `primary-100` | #DBEAFE | Primary light background |

### Neutral
| Token | Value | Usage |
|-------|-------|-------|
| `gray-900` | #111827 | Primary text |
| `gray-500` | #6B7280 | Secondary text |
| `gray-200` | #E5E7EB | Borders |
| `gray-50` | #F9FAFB | Page background |

### Semantic
| Token | Value | Usage |
|-------|-------|-------|
| `success` | #10B981 | Success states |
| `warning` | #F59E0B | Warnings |
| `error` | #EF4444 | Errors, destructive |
| `info` | #3B82F6 | Informational |

---

## Typography

**Font family:** Inter (headings + body), JetBrains Mono (code)

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| H1 | 30px | 700 | 36px | Page titles |
| H2 | 24px | 600 | 32px | Section titles |
| H3 | 20px | 600 | 28px | Card titles |
| Body | 14px | 400 | 20px | Default text |
| Caption | 12px | 400 | 16px | Labels, hints |

---

## Spacing

**Base unit:** 4px

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight gaps (icon + label) |
| `sm` | 8px | Inside compact elements |
| `md` | 16px | Default component padding |
| `lg` | 24px | Section gaps |
| `xl` | 32px | Page sections |
| `2xl` | 48px | Major layout gaps |

**Page margins:** 24px (mobile), 32px (tablet), 48px (desktop)
**Content max-width:** 1280px

---

## Borders & Corners

| Property | Value |
|----------|-------|
| Default border | 1px solid gray-200 |
| Focus border | 2px solid primary-500 |
| Error border | 1px solid error |
| Radius small | 6px (buttons, inputs) |
| Radius medium | 8px (cards) |
| Radius large | 12px (modals) |
| Radius full | 9999px (avatars, pills) |

---

## Shadows

| Level | Value | Usage |
|-------|-------|-------|
| sm | 0 1px 2px rgba(0,0,0,0.05) | Cards |
| md | 0 4px 6px rgba(0,0,0,0.07) | Dropdowns, popovers |
| lg | 0 10px 15px rgba(0,0,0,0.1) | Modals, dialogs |

---

## Component Patterns

### Buttons
- **Primary:** bg primary-500, text white, hover primary-600, radius 6px, padding 8px 16px
- **Secondary:** bg white, border gray-200, text gray-700, hover bg gray-50
- **Ghost:** no bg, no border, text primary-500, hover bg primary-50
- **Destructive:** bg error, text white, hover darker
- **Sizes:** sm (32px height), md (36px height), lg (40px height)
- **Disabled:** opacity 0.5, cursor not-allowed

### Inputs
- Height: 36px, padding 8px 12px, border gray-200, radius 6px
- Focus: border primary-500, ring 2px primary-100
- Error: border error, text below in error color
- Label: above input, font-weight 500, caption size
- Placeholder: gray-400

### Cards
- Background: white, border gray-200, radius 8px, shadow sm
- Padding: 16px (compact) or 24px (default)
- Header: bold title + optional subtitle, bottom border divider

### Tables
- Header: bg gray-50, font-weight 600, text-transform uppercase caption size
- Rows: border-bottom gray-100, hover bg gray-50
- Cell padding: 12px 16px

[... more components as visible in the reference screens ...]

---

## Layout Patterns

- **Page:** sidebar (256px) + scrollable content area
- **Content:** max-width 1280px, centered with auto margins
- **Grid:** 12-column, 24px gutter
- **Breakpoints:** sm 640px, md 768px, lg 1024px, xl 1280px

---

## Screen Blueprints

### Screen: [Screen Name]

**Purpose:** [What this page does]

**Component inventory (top to bottom):**

1. **[Component name]** ([visual notes])
   - [Element 1]
   - [Element 2]

2. **[Component name]**
   - [Element 1]
   - [Element 2]

3. **[Data table / main content]**
   - Columns: [col1], [col2], [col3]...
   - [Grouping, sorting, expandable behavior]
   - [Row interaction patterns]

**Custom components:**
- [Unique component 1]: [description of what it looks like and how it works]
- [Unique component 2]: [description]

[... repeat for each reference screen ...]
```

**Important:** Only document what you can actually see and extract. Don't invent tokens or values. If something is unclear, note it with a `[?]` marker.

## Step 5: Confirm and Save

Show the user a summary of what was extracted:
- Number of colors, type levels, spacing tokens, component patterns
- Any gaps or uncertain values marked with `[?]`

Save the file to `projects/<ProjectName>/design-system.md`.

## Step 6: Next Steps

Tell the user:

"Design system extracted and saved to `projects/<ProjectName>/design-system.md`.

This file is used by the 'generate feature code' skill to produce code that matches your designs. You can:
1. **Review and refine** — open the file and adjust any values I got wrong
2. **Generate feature code** — say 'generate code for story #XXX' and it will use this design system
3. **Re-extract later** — if the designs change significantly, run this again with updated reference screens"

---

## Notes

- This skill produces a **snapshot** of the design system at one point in time. If designs evolve significantly, re-run it.
- The output is intentionally in markdown (not JSON/YAML) so it's easy for humans to read and edit.
- The file lives at the project root, not in `output/`, because it's a reference artifact that persists across pipeline runs.
- The "generate feature code" skill (12) reads this file in its Step 4d ("Check Design System") to apply correct tokens and patterns.
