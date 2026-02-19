export interface ProjectConfig {
  project: string;
  ado?: {
    organization?: string;
    project?: string;
  };
  state?: Record<string, unknown>;
  status?: string;
  changes?: ChangeRecord[];
}

export interface ChangeRecord {
  id: string;
  date: string;
  source: string;
  summary: string;
  classification: string;
  stories_added?: string[];
  stories_modified?: string[];
  effort_delta?: Record<string, number>;
  approved?: boolean;
}

export interface TimelineEvent {
  type: string;
  timestamp: string;
  data: Record<string, unknown>;
}

export interface SourceFile {
  filename: string;
  parsedFile: string;
  content: string;
  format?: string;
  estimatedTokens?: number;
  change?: string;
}

export interface ManifestFile {
  filename: string;
  format: string;
  status: string;
  type: string;
  text_length?: number;
  estimated_tokens?: number;
  content_hash?: string;
  parsed_file?: string;
  change?: string;
  error?: string;
}

export interface Manifest {
  project: string;
  files: ManifestFile[];
  summary: {
    total_files: number;
    successful: number;
    errors: number;
    text_files: number;
    image_files: number;
    total_text_chars: number;
    estimated_tokens: number;
    new_files?: string[];
    changed_files?: string[];
    removed_files?: string[];
  };
}

export interface ProjectSummary {
  name: string;
  status: string;
  adoProject?: string;
  adoOrg?: string;
  filesIngested: number;
  storiesPushed: number;
  changesProcessed: number;
  hasOverview: boolean;
  hasBreakdown: boolean;
}

export interface Communication {
  type: "questions" | "answer" | "change_request";
  filename: string;
  content: string;
  date?: string;
}
