import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import type {
  ProjectConfig,
  ProjectSummary,
  TimelineEvent,
  SourceFile,
  Manifest,
  Communication,
} from "./types";

const PROJECTS_DIR = path.resolve(process.cwd(), "../projects");

function projectPath(name: string, ...segments: string[]): string {
  return path.join(PROJECTS_DIR, name, ...segments);
}

function readFileIfExists(filePath: string): string | null {
  try {
    return fs.readFileSync(filePath, "utf-8");
  } catch {
    return null;
  }
}

function readJsonIfExists<T>(filePath: string): T | null {
  const content = readFileIfExists(filePath);
  if (!content) return null;
  try {
    return JSON.parse(content) as T;
  } catch {
    return null;
  }
}

// --- Project listing ---

export function listProjects(): ProjectSummary[] {
  if (!fs.existsSync(PROJECTS_DIR)) return [];

  const dirs = fs
    .readdirSync(PROJECTS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  const results: ProjectSummary[] = [];
  for (const name of dirs) {
    const config = getProjectConfig(name);
    if (!config) continue;

    const manifest = readJsonIfExists<Manifest>(
      projectPath(name, "output", "requirements_manifest.json")
    );
    const mapping = readJsonIfExists<{ stories?: unknown[] }>(
      projectPath(name, "output", "ado_mapping.json")
    );
    const hasOverview = fs.existsSync(
      projectPath(name, "output", "overview.md")
    );
    const hasBreakdown = fs.existsSync(
      projectPath(name, "output", "breakdown.json")
    );

    results.push({
      name,
      status: config.status || "new",
      adoProject: config.ado?.project,
      adoOrg: config.ado?.organization,
      filesIngested: manifest?.summary?.successful || 0,
      storiesPushed: mapping?.stories?.length || 0,
      changesProcessed: config.changes?.length || 0,
      hasOverview,
      hasBreakdown,
    });
  }
  return results;
}

// --- Project config ---

export function getProjectConfig(name: string): ProjectConfig | null {
  const yamlPath = projectPath(name, "project.yaml");
  const content = readFileIfExists(yamlPath);
  if (!content) return null;
  try {
    return yaml.load(content) as ProjectConfig;
  } catch {
    return null;
  }
}

// --- Timeline ---

export function getTimeline(name: string): TimelineEvent[] {
  // Read events.json (pipeline-logged events)
  const events =
    readJsonIfExists<TimelineEvent[]>(
      projectPath(name, "output", "events.json")
    ) || [];

  // Supplement with file-based events if events.json is sparse
  const supplemental = deriveEventsFromFiles(name);
  const allEvents = [...events, ...supplemental];

  // Deduplicate by type (keep the explicit event if both exist)
  const seen = new Set(events.map((e) => e.type));
  const merged = [
    ...events,
    ...supplemental.filter((e) => !seen.has(e.type)),
  ];

  return merged.sort(
    (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );
}

function deriveEventsFromFiles(name: string): TimelineEvent[] {
  const events: TimelineEvent[] = [];

  const check = (
    filePath: string,
    eventType: string,
    data: Record<string, unknown> = {}
  ) => {
    const full = projectPath(name, ...filePath.split("/"));
    if (fs.existsSync(full)) {
      const stat = fs.statSync(full);
      events.push({
        type: eventType,
        timestamp: stat.mtime.toISOString(),
        data,
      });
    }
  };

  check("project.yaml", "project_created");
  check("output/requirements_manifest.json", "files_ingested");
  check("output/overview.md", "overview_generated");
  check("output/questions.txt", "questions_generated");
  check("output/breakdown.json", "breakdown_generated");
  check("output/breakdown.xlsx", "breakdown_exported");
  check("output/push_ready.json", "push_ready_generated");
  check("output/ado_mapping.json", "pushed_to_ado");

  // Change requests
  const config = getProjectConfig(name);
  if (config?.changes) {
    for (const cr of config.changes) {
      events.push({
        type: "change_request",
        timestamp: new Date(cr.date).toISOString(),
        data: {
          id: cr.id,
          summary: cr.summary,
          classification: cr.classification,
          approved: cr.approved,
        },
      });
    }
  }

  return events;
}

// --- Sources ---

export function getSources(name: string): SourceFile[] {
  const parsedDir = projectPath(name, "output", "parsed");
  if (!fs.existsSync(parsedDir)) return [];

  const manifest = readJsonIfExists<Manifest>(
    projectPath(name, "output", "requirements_manifest.json")
  );

  const files = fs
    .readdirSync(parsedDir)
    .filter((f) => f.endsWith(".md"))
    .sort();

  return files.map((f) => {
    const content = fs.readFileSync(path.join(parsedDir, f), "utf-8");
    const manifestEntry = manifest?.files?.find(
      (mf) => mf.parsed_file === f
    );

    return {
      filename: manifestEntry?.filename || f.replace(/\.md$/, ""),
      parsedFile: f,
      content,
      format: manifestEntry?.format,
      estimatedTokens: manifestEntry?.estimated_tokens,
      change: manifestEntry?.change,
    };
  });
}

// --- Communications ---

export function getCommunications(name: string): Communication[] {
  const comms: Communication[] = [];

  // Discovery questions
  const questions = readFileIfExists(
    projectPath(name, "output", "questions.txt")
  );
  if (questions) {
    const stat = fs.statSync(projectPath(name, "output", "questions.txt"));
    comms.push({
      type: "questions",
      filename: "questions.txt",
      content: questions,
      date: stat.mtime.toISOString(),
    });
  }

  // Client answers
  const answersDir = projectPath(name, "answers");
  if (fs.existsSync(answersDir)) {
    const files = fs.readdirSync(answersDir).filter((f) => !f.startsWith("."));
    for (const f of files) {
      const full = path.join(answersDir, f);
      const stat = fs.statSync(full);
      const content = readFileIfExists(full) || "(binary file)";
      comms.push({
        type: "answer",
        filename: f,
        content,
        date: stat.mtime.toISOString(),
      });
    }
  }

  // Change requests
  const changesDir = projectPath(name, "changes");
  if (fs.existsSync(changesDir)) {
    const files = fs
      .readdirSync(changesDir)
      .filter((f) => !f.startsWith("."));
    for (const f of files) {
      const full = path.join(changesDir, f);
      const stat = fs.statSync(full);
      const content = readFileIfExists(full) || "(binary file)";
      comms.push({
        type: "change_request",
        filename: f,
        content,
        date: stat.mtime.toISOString(),
      });
    }
  }

  return comms.sort(
    (a, b) =>
      new Date(a.date || 0).getTime() - new Date(b.date || 0).getTime()
  );
}

// --- Overview ---

export function getOverview(name: string): string | null {
  return readFileIfExists(projectPath(name, "output", "overview.md"));
}
