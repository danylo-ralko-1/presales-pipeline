# PreSales Pipeline

An AI-powered pre-sales assistant that lives in your terminal. Just open Claude Code, describe what you need in plain English, and it handles requirements, Azure DevOps stories, and feature code generation for you.

**You don't need to memorize any commands.** Just chat with Claude like you would with a colleague.

## How It Works

Open your terminal in the project folder and start Claude Code:

```bash
claude
```

Then just tell it what you want. Here are some real examples:

### Starting a new project

> "Create a new presales project called Glossary"

Claude will set up the folder structure, ask for your Azure DevOps org and project name, and get everything ready.

### Processing requirements

Just drag and drop your files (PDF, DOCX, XLSX, images) directly into the Claude Code chat. No need to manually copy anything into folders — Claude will place them in the right location automatically and start processing.

> *drop files into chat*
>
> "These are the requirements for the project. Read them and give me an overview."

Claude will save the files, parse them, extract the requirements, and generate a summary with clarification questions for the client.

### Generating stories

> "Break down these requirements into user stories with estimates"

Claude will create a structured breakdown with epics, features, stories, and effort estimates (FE/BE/DevOps/Design).

### Pushing to Azure DevOps

> "Push these stories to ADO"

Claude will create the full hierarchy in Azure DevOps — Epics, Features, User Stories with acceptance criteria, and FE/BE tasks — all properly linked.

### Generating feature code

> "Generate code for story #752"
>
> *provide the target codebase path*

Claude will read the story from ADO, analyze your codebase's patterns and design system, generate working starter code, an API contract for the backend developer, and a review guide. It pushes everything as a feature branch and links it back in ADO. Frontend and backend developers check out the branch and start from a working baseline.

### Extracting a design system

> "Extract the design system from Figma"
>
> *provide 1-3 reference screen URLs*

Claude will read the Figma designs via MCP and capture colors, typography, spacing, borders, shadows, and component patterns into a `design-system.md` file. This is used by the code generation skill to produce design-aware output.

### Handling change requests

> "I got a change request from the client — they want to add a new filter. Here's the document."
>
> *drop the file into chat*

Claude will analyze the impact, identify affected stories, and propose updates to ADO.

## One-Time Setup

### 1. Clone and install

```bash
git clone https://github.com/danylo-ralko-1/presales-pipeline.git
cd presales-pipeline
pip install pyyaml click openpyxl requests python-docx pdfplumber
chmod +x presales
```

### 2. Add your credentials

```bash
cp .env.example .env
```

Open `.env` and paste your tokens:

```
ADO_PAT=your_azure_devops_pat_here
FIGMA_PAT=your_figma_personal_access_token_here
```

**Where to get them:**
- **ADO PAT:** dev.azure.com → User Settings → Personal Access Tokens (needs Work Items read/write)
- **Figma PAT:** figma.com → Settings → Personal Access Tokens

### 3. Start chatting

```bash
claude
```

That's it. Claude reads the `CLAUDE.md` instructions automatically and knows how the pipeline works. Just tell it what you need.

## What You Can Ask Claude To Do

### Main Pipeline

| What you want | Just say something like... |
|---|---|
| Set up a new project | "Create a new project called ClientName" |
| Read requirement files | *(drop files into chat)* "These are the requirements" |
| Get a requirements overview | "Summarize the requirements and give me questions for the client" |
| Break down into stories | "Generate a breakdown with estimates" |
| Export to Excel | "Export the breakdown to an Excel file" |
| Push stories to ADO | "Push these stories to Azure DevOps" |
| Generate feature code | "Generate code for story #752" *(produces frontend code + API contract + review guide)* |
| Handle a change request | "Analyze this change request" *(drop file)* |
| Generate product document | "Create a product document from all the ADO stories" |
| Check project status | "What's the status of the Glossary project?" |

### Standalone Tools

| What you want | Just say something like... |
|---|---|
| Extract design system | "Extract the design system from Figma" *(provide screen URLs)* |
| Validate designs vs ADO | "Compare ADO stories with this Figma link: ..." |

## Project Structure

```
presales-pipeline/
├── presales              # CLI entrypoint (used by Claude behind the scenes)
├── commands/             # Pipeline command implementations
├── core/                 # Config, ADO client, parser, context
├── projects/             # Your project workspaces (gitignored)
│   └── <ProjectName>/
│       ├── project.yaml  # Config: ADO/Figma credentials, pipeline state
│       ├── design-system.md  # Extracted design tokens (from Figma)
│       ├── input/        # Drop your requirement files here
│       ├── answers/      # Client answers to clarification questions
│       ├── changes/      # Change request files
│       ├── output/       # Everything Claude generates
│       └── snapshots/    # Auto-snapshots before change requests
├── .env                  # Your credentials (gitignored)
└── CLAUDE.md             # Instructions Claude follows automatically
```

## Prerequisites

- Python 3.10+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- Azure DevOps account with a Personal Access Token
- (Optional) Figma account with a Personal Access Token for design system extraction

---

<details>
<summary><b>CLI Command Reference (advanced)</b></summary>

These are the Python commands that Claude runs behind the scenes. You don't need to use them directly — Claude will call them for you. But if you prefer running things manually:

| Command | Description |
|---------|-------------|
| `python3 presales init <project>` | Create a new project |
| `python3 presales ingest <project>` | Parse requirements from input files |
| `python3 presales breakdown-export <project>` | Export breakdown to Excel |
| `python3 presales push <project>` | Push stories to Azure DevOps |
| `python3 presales validate <project> --figma-link <url>` | *(Optional)* Compare Figma designs against ADO stories |
| `python3 presales status <project>` | Show project status |
| `python3 presales list` | List all projects |

</details>
