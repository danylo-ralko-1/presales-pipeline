"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { FileText, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { SourceFile } from "@/lib/types";

function formatTokens(n?: number): string {
  if (!n) return "";
  if (n < 1000) return `${n} tokens`;
  return `${(n / 1000).toFixed(1)}k tokens`;
}

export function SourcesViewer({ sources }: { sources: SourceFile[] }) {
  const [selected, setSelected] = useState<string | null>(
    sources[0]?.parsedFile || null
  );

  if (sources.length === 0) {
    return (
      <div className="text-center py-12 text-[hsl(var(--muted-foreground))]">
        <p>No source files ingested yet.</p>
      </div>
    );
  }

  const active = sources.find((s) => s.parsedFile === selected);

  return (
    <div className="flex gap-4 min-h-[500px]">
      {/* File list */}
      <div className="w-72 shrink-0 border rounded-lg overflow-hidden">
        <div className="px-3 py-2 border-b bg-[hsl(var(--muted))]">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-[hsl(var(--muted-foreground))]">
            Source Files ({sources.length})
          </h3>
        </div>
        <div className="divide-y">
          {sources.map((source) => (
            <button
              key={source.parsedFile}
              onClick={() => setSelected(source.parsedFile)}
              className={cn(
                "w-full flex items-start gap-2 px-3 py-2.5 text-left text-sm transition-colors hover:bg-[hsl(var(--accent))]",
                selected === source.parsedFile && "bg-[hsl(var(--accent))]"
              )}
            >
              <FileText className="h-4 w-4 mt-0.5 shrink-0 text-[hsl(var(--muted-foreground))]" />
              <div className="min-w-0 flex-1">
                <p className="font-medium truncate">{source.filename}</p>
                <div className="flex gap-2 mt-0.5">
                  {source.format && (
                    <span className="text-xs text-[hsl(var(--muted-foreground))]">
                      {source.format}
                    </span>
                  )}
                  {source.estimatedTokens && (
                    <span className="text-xs text-[hsl(var(--muted-foreground))]">
                      {formatTokens(source.estimatedTokens)}
                    </span>
                  )}
                </div>
              </div>
              {selected === source.parsedFile && (
                <ChevronRight className="h-4 w-4 mt-0.5 shrink-0 text-[hsl(var(--muted-foreground))]" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Content viewer */}
      <div className="flex-1 border rounded-lg overflow-hidden">
        {active ? (
          <>
            <div className="px-4 py-2.5 border-b bg-[hsl(var(--muted))] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-medium">{active.filename}</h3>
                {active.change && active.change !== "unchanged" && (
                  <Badge
                    variant={active.change === "new" ? "success" : "warning"}
                  >
                    {active.change}
                  </Badge>
                )}
              </div>
              {active.estimatedTokens && (
                <span className="text-xs text-[hsl(var(--muted-foreground))]">
                  {formatTokens(active.estimatedTokens)}
                </span>
              )}
            </div>
            <div className="p-5 overflow-auto max-h-[600px]">
              <article className="prose prose-sm max-w-none prose-headings:text-base prose-headings:font-semibold">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {active.content}
                </ReactMarkdown>
              </article>
            </div>
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-[hsl(var(--muted-foreground))]">
            Select a file to view its contents
          </div>
        )}
      </div>
    </div>
  );
}
