# Scan Reference Implementation (Codebase Patterns)

**Trigger:** "scan codebase", "scan patterns", "extract patterns", "learn from codebase", "scan reference", "codebase patterns"

> **Standalone skill.** Run this AFTER developers have manually implemented 2-3 reference stories in the target codebase. The output (`codebase-patterns.md`) is used by the "generate feature code" and "generate tests" skills to produce code that matches the project's conventions exactly.

**Pre-checks:**
- User must provide the **target codebase path** — the actual product repo. If not: "Where is your product codebase? Give me the absolute path."
- The codebase must have at least 2-3 implemented features to scan. If the `src/` directory has fewer than 10 files: "This codebase looks too bare for pattern extraction. I recommend developers manually implement 2-3 stories first (a list page, a form page, and a detail page) so I have real patterns to learn from."
- Project name must be known (to save the output). If not: "Which project is this for?"
- Optional: User can specify **reference story IDs** (ADO IDs) to focus the scan on specific implementations. If not provided, scan the whole codebase.

---

## Step 1: Gather Inputs

Collect from the user (ask for anything missing):

1. **Target codebase path** — absolute path to the product repo
2. **Reference stories** (optional) — ADO story IDs that were manually implemented. If provided, focus analysis on those files. If not, scan the full codebase.
3. **Project name** — to save the output file

## Step 2: Understand the Project

### 2a: Read package.json / project config

Read `package.json` (or `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to identify:
- Framework and version
- All dependencies — these determine available libraries and patterns
- Scripts — how the project builds, tests, lints
- Any workspaces or monorepo structure

### 2b: Read configuration files

Read ALL relevant config files (read them in parallel):
- `tsconfig.json` / `jsconfig.json` — path aliases, strict mode, target
- `tailwind.config.*` / `postcss.config.*` — theme extensions, plugins, custom utilities
- `.eslintrc*` / `eslint.config.*` — linting rules, custom rules
- `.prettierrc*` — formatting conventions
- `vite.config.*` / `next.config.*` / `webpack.config.*` — build configuration, aliases, plugins
- `jest.config.*` / `vitest.config.*` — test setup, transforms, module mocking
- `.env.example` — environment variable patterns (NOT .env — never read secrets)
- `docker-compose.yml` / `Dockerfile` — deployment patterns if present

### 2c: Map the full directory structure

Scan the complete `src/` (or equivalent) tree to understand the folder organization. Note:
- How features/domains are grouped (by feature? by type? hybrid?)
- Where shared code lives vs feature-specific code
- Barrel export pattern (`index.ts`) usage
- Any code generation output folders (don't scan those)

## Step 3: Deep Pattern Extraction

For each of the 12 categories below, find 2-3 real examples in the codebase and extract **actual code snippets** (not descriptions). Each pattern should include the file path, the relevant code, and a brief note on when/how to use it.

### Category 1: Project Structure

Document the exact folder hierarchy with purpose annotations:

```
src/
├── app/                    # Next.js app router pages
│   ├── (auth)/             # Auth-required layout group
│   ├── api/                # API route handlers
│   └── layout.tsx          # Root layout
├── components/
│   ├── ui/                 # Primitive components (Button, Input, Modal)
│   └── features/           # Feature-specific composed components
├── hooks/                  # Custom React hooks
├── lib/                    # Utilities, API client, constants
├── services/               # API service functions
├── stores/                 # State management (Zustand stores, Redux slices)
├── types/                  # Shared TypeScript types
└── styles/                 # Global styles, theme overrides
```

Note where new feature files should go. If there's a naming convention for feature folders, document it.

### Category 2: Component Patterns

Extract the canonical component structure by reading the most well-written component. Document:

**Standard component template:**
```typescript
// Extract an actual component showing:
// - Import ordering convention
// - Props interface definition and naming
// - Component function signature (arrow vs function, default export position)
// - Hook usage ordering (framework hooks first, then custom)
// - Return structure (fragments, wrappers, conditional rendering pattern)
// - Export style (named, default, barrel)
```

**Sub-component pattern:**
- How child components are organized (same file? separate files? co-located folder?)
- How props are passed down (prop drilling vs context vs composition)

**Compound component pattern (if used):**
- Provider/Consumer pattern, dot notation (`Table.Header`, `Table.Row`)

### Category 3: Data Layer

Extract the data fetching and state management patterns:

**API client setup:**
```typescript
// The actual API client instance — base URL config, interceptors, auth header injection
```

**Data fetching hook:**
```typescript
// A real custom hook that fetches data — shows the project's pattern for:
// - React Query / SWR / useEffect / server components
// - Cache key naming convention
// - Loading/error state handling
// - Refetch triggers
// - Pagination pattern
```

**State management:**
```typescript
// A real store/slice/context — shows:
// - Store structure (Zustand create, Redux slice, Context provider)
// - Action naming convention
// - How derived state is computed
// - How the store is consumed in components
```

**Mutation pattern:**
```typescript
// A real mutation (create/update/delete) — shows:
// - Optimistic updates (if used)
// - Cache invalidation after mutation
// - Error rollback pattern
// - Success notification/redirect
```

### Category 4: Form Handling

Extract form patterns from an existing form page:

**Form setup:**
```typescript
// The actual form implementation — shows:
// - Form library used (react-hook-form, Formik, native)
// - Validation schema definition (Zod, Yup, custom)
// - Default values pattern
// - Submit handler structure
```

**Form field pattern:**
```typescript
// How a single form field is wired — shows:
// - Field registration / binding
// - Error message display
// - Label association
// - Required/optional indication
```

**Validation schema:**
```typescript
// A real validation schema — shows:
// - Schema definition style
// - Custom validation rules
// - Cross-field validation (if any)
// - Error message format
```

### Category 5: Routing & Navigation

Extract the routing and navigation patterns:

**Route definition:**
```typescript
// How routes are defined — file-based routing structure, route config, or router setup
// Include any route guards, middleware, or layout nesting
```

**Navigation pattern:**
```typescript
// How navigation is triggered — Link component usage, programmatic navigation
// Shows breadcrumb generation, active state detection, param extraction
```

**Protected route pattern:**
```typescript
// How auth-gated routes work — redirect logic, role checking, loading state
```

### Category 6: Styling

Extract the styling approach and conventions:

**Component styling:**
```typescript
// A real component's styling — shows:
// - Tailwind class organization (if Tailwind: responsive, state, layout, typography, color ordering)
// - CSS Module usage (if CSS Modules: naming convention, composition)
// - styled-components (if SC: theme access, prop-based styling)
// - CSS-in-JS pattern (if applicable)
```

**Theme/design tokens usage:**
```typescript
// How the codebase accesses design tokens:
// - Tailwind: theme() function, custom utilities, design token classes
// - CSS vars: var(--color-primary), how vars are defined and consumed
// - Theme object: theme.colors.primary, how theme is provided and accessed
```

**Responsive pattern:**
```typescript
// How responsive design is handled — breakpoint usage, mobile-first vs desktop-first
```

**Animation pattern (if present):**
```typescript
// Transition/animation conventions — Framer Motion, CSS transitions, keyframes
```

### Category 7: Shared UI Components

Catalog all reusable components the project provides. For each, note:

| Component | Path | Props Summary | Variants |
|-----------|------|---------------|----------|
| Button | `src/components/ui/Button.tsx` | `variant`, `size`, `disabled`, `loading`, `onClick` | primary, secondary, ghost, destructive |
| Input | `src/components/ui/Input.tsx` | `label`, `error`, `placeholder`, `type` | text, email, password, search |
| Modal | `src/components/ui/Modal.tsx` | `open`, `onClose`, `title`, `size` | sm, md, lg |
| ... | ... | ... | ... |

For complex components (Table, Form, Select), extract a **usage example** showing the typical invocation pattern:

```typescript
// How Table is actually used in the project — columns definition, data binding, sorting, pagination
```

### Category 8: Type Patterns

Extract the TypeScript conventions:

**Entity/model types:**
```typescript
// A real entity type — shows:
// - Interface vs type alias convention
// - Naming convention (UserDTO, IUser, User)
// - How optional fields are handled
// - How enums/unions are defined
// - How timestamps, IDs, and common fields are typed
```

**API response types:**
```typescript
// How API responses are typed — generic wrapper, pagination type, error type
```

**Component prop types:**
```typescript
// How props are typed — inline vs extracted, extends pattern, children typing
```

**Utility types (if custom):**
```typescript
// Any project-specific utility types (Nullable<T>, PartialBy<T, K>, etc.)
```

### Category 9: Error Handling

Extract error handling patterns:

**API error handling:**
```typescript
// How API errors are caught and displayed — error boundary, toast notification, inline error
```

**Form error handling:**
```typescript
// How form validation errors and submission errors are presented
```

**Global error boundary (if present):**
```typescript
// Error boundary component — fallback UI, error reporting
```

**Error types:**
```typescript
// Custom error classes or error response shape
```

### Category 10: Authentication & Authorization

Extract auth patterns (if the app has auth):

**Auth context/provider:**
```typescript
// How auth state is managed — user object, token storage, login/logout actions
```

**Protected component pattern:**
```typescript
// How components check permissions — useAuth hook, role-based rendering, guard pattern
```

**Auth header injection:**
```typescript
// How the auth token gets into API requests — interceptor, middleware, manual header
```

### Category 11: Testing Patterns

Extract testing conventions from existing test files:

**Unit test structure:**
```typescript
// A real component test — shows:
// - Test file naming and location
// - Import pattern (testing library, helpers, mocks)
// - Render helper (with providers, with router, with theme)
// - Describe/it nesting convention
// - Setup/teardown (beforeEach, afterEach)
// - Assertion style
```

**Mock patterns:**
```typescript
// How the project mocks — shows:
// - API mocking (MSW handlers, jest.mock, vi.mock)
// - Module mocking (next/router, custom hooks)
// - Mock data factories (if any)
```

**Integration/E2E test pattern (if present):**
```typescript
// Playwright or Cypress test — shows page interaction conventions
```

### Category 12: Code Style & Conventions

Document implicit conventions not captured by linter config:

- **File naming:** PascalCase components, camelCase utilities, kebab-case routes?
- **Import ordering:** framework → external libs → internal absolute → relative? Sorted?
- **Export style:** named exports from components, default from pages, barrel files?
- **Comment style:** JSDoc? Inline only? When are comments used?
- **Async patterns:** async/await everywhere? .then() for fire-and-forget?
- **Null handling:** strict null checks? Optional chaining preference? Nullish coalescing?
- **String conventions:** template literals vs concatenation? Single vs double quotes?
- **Magic numbers/strings:** constants file? Inline with comment? Enum?

## Step 4: Build Reference Implementations Table

If the user provided reference story IDs, create a mapping table:

| Story ID | Title | Files | Patterns Demonstrated |
|----------|-------|-------|-----------------------|
| #752 | Glossary Terms Page | `src/features/glossary/GlossaryPage.tsx`, `src/hooks/useGlossaryTerms.ts`, ... | List page, search, filtering, table, pagination |
| #753 | Add New Term | `src/features/glossary/AddTermModal.tsx`, ... | Form, modal, validation, mutation |
| #754 | Term Detail Page | `src/features/glossary/TermDetail.tsx`, ... | Detail page, edit mode, breadcrumbs |

This tells future code gen: "For a list page, look at #752. For a form, look at #753."

## Step 5: Record Git Commit Hash

Record the current commit hash for staleness detection:

```bash
cd <target_codebase_path> && git rev-parse HEAD
```

Store this at the top of the output file. Code gen will check this hash against the current HEAD to detect if the patterns file is stale.

## Step 6: Generate codebase-patterns.md

Write the full patterns file to `projects/<ProjectName>/codebase-patterns.md`:

```markdown
# Codebase Patterns — [Project Name]

**Scanned from:** [target codebase path]
**Commit:** [full commit hash]
**Date:** [YYYY-MM-DD]
**Reference stories:** [#XXX, #YYY, #ZZZ] or "Full codebase scan"

> This file captures the conventions and patterns used in the product codebase.
> It is the primary reference for code generation — generated code MUST follow
> these patterns exactly. If you modify project conventions, re-scan with
> "scan codebase" to keep this file current.

---

## 1. Project Structure

[folder tree with annotations]

---

## 2. Component Patterns

[actual code snippets with file paths]

---

## 3. Data Layer

[actual code snippets with file paths]

---

[... all 12 categories ...]

---

## Reference Implementations

[mapping table if reference stories were provided]
```

**Rules:**
- Every code snippet must include the source file path as a comment or heading
- Use the project's actual variable names, not generic placeholders
- If a category has no examples in the codebase (e.g., no forms exist yet), write: `No examples found in the codebase. This pattern will be established by the first story that needs it.`
- Keep snippets focused — show the pattern, not the entire file. 10-30 lines per snippet is ideal.
- If the codebase is large, don't try to document every component — focus on the canonical examples that best represent each pattern.

## Step 7: Present Summary

Show the user what was extracted:

```
Codebase patterns extracted and saved to projects/<ProjectName>/codebase-patterns.md

Scanned: [X] source files across [Y] directories
Commit: [short hash]

Patterns found:
✅ Project Structure — [brief note]
✅ Component Patterns — [N] components analyzed
✅ Data Layer — [fetching lib], [state management lib]
✅ Form Handling — [form lib], [validation lib]
✅ Routing — [router type]
✅ Styling — [CSS approach]
✅ Shared UI Components — [N] components cataloged
✅ Type Patterns — [strict/loose], [naming convention]
✅ Error Handling — [approach]
✅ Auth — [approach] (or ⬜ No auth patterns found)
✅ Testing — [framework], [N] test files analyzed
✅ Code Style — [key conventions]

Gaps (no examples found):
⬜ [category] — will be established by the first story that needs it
```

## Step 8: Next Steps

Tell the user:

"Codebase patterns extracted and saved. This file is now the primary reference for code generation.

You can:
1. **Review and refine** — open `codebase-patterns.md` and adjust anything I got wrong
2. **Generate feature code** — say 'generate code for story #XXX' and it will follow these patterns exactly
3. **Re-scan later** — when conventions evolve significantly (I'll suggest it if the codebase drifts >30 commits from the scan)"

---

## Staleness Detection

When code generation (skill 12) or test generation (skill 14) reads this file, it should:

1. Read the `**Commit:**` line to get the scan hash
2. Run `git rev-list <scan-hash>..HEAD --count` to count commits since the scan
3. If **>30 commits**: warn the user: "The codebase patterns file was scanned 47 commits ago. Conventions may have changed. Want me to re-scan before generating code?"
4. If **scan hash is not found** (rebased away): warn and suggest re-scan
5. If **≤30 commits**: proceed normally — patterns are fresh enough

The threshold of 30 commits is a rough heuristic. A project with 50 devs will hit this quickly; a solo project won't hit it for weeks. The user can always force a re-scan.

---

## Refresh Mode

If `codebase-patterns.md` already exists and the user says "re-scan" or "refresh patterns":

1. Read the existing file to understand what was previously captured
2. Re-scan the codebase from scratch (don't try to diff — full re-extraction is cleaner)
3. Overwrite the file with fresh patterns
4. Show a summary of what changed: "Updated patterns file. Notable changes: [switched from CSS Modules to Tailwind in styling section, added 3 new shared components, ...]"
