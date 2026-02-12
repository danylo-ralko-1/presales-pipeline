# PreSales Pipeline

An AI-powered pre-sales assistant that lives in your terminal. Just open Claude Code, describe what you need in plain English, and it handles requirements, Azure DevOps stories, Figma design validation, and technical specs for you.

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

### Validating designs against requirements

> "Compare my ADO requirements with this Figma design and check if they match"
>
> *paste your Figma link*

Claude will screenshot every Figma screen, read your ADO stories, and produce a validation report showing what matches, what's missing, and what conflicts.

### Enriching stories from designs

> "Enrich the acceptance criteria for my stories using the Figma designs"

Claude will update each story's AC with specific UI details from the designs — without adding pixel-level specs.

### Generating technical specs

> "Generate YAML files with technical specifications for the FAQ page story"

Claude will create detailed FE and BE spec files and can upload them directly to the ADO tasks.

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

| What you want | Just say something like... |
|---|---|
| Set up a new project | "Create a new project called ClientName" |
| Read requirement files | *(drop files into chat)* "These are the requirements" |
| Get a requirements overview | "Summarize the requirements and give me questions for the client" |
| Break down into stories | "Generate a breakdown with estimates" |
| Export to Excel | "Export the breakdown to an Excel file" |
| Push stories to ADO | "Push these stories to Azure DevOps" |
| Validate against Figma | "Compare ADO stories with this Figma link: ..." |
| Enrich acceptance criteria | "Enrich the stories from the Figma designs" |
| Handle a change request | "Analyze this change request" *(drop file)* |
| Generate tech specs | "Generate FE and BE specs for story #123" |
| Upload specs to ADO | "Upload the specs to the ADO tasks" |
| Generate product document | "Create a product document from all the ADO stories" |
| Check project status | "What's the status of the Glossary project?" |

## Project Structure

```
presales-pipeline/
├── presales              # CLI entrypoint (used by Claude behind the scenes)
├── commands/             # Pipeline command implementations
├── core/                 # Config, ADO client, parser, context
├── projects/             # Your project workspaces (gitignored)
│   └── <ProjectName>/
│       ├── project.yaml  # Config: ADO/Figma credentials, pipeline state
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
- (Optional) Figma account with a Personal Access Token for design validation

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
| `python3 presales validate <project> --figma-link <url>` | Compare Figma designs against ADO stories |
| `python3 presales enrich <project> --figma-link <url>` | Enrich story AC from Figma designs |
| `python3 presales specs-upload <project>` | Upload spec files to ADO tasks |
| `python3 presales status <project>` | Show project status |
| `python3 presales list` | List all projects |

</details>
