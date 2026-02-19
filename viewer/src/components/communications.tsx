"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { format } from "date-fns";
import { Mail, MessageSquare, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { Communication } from "@/lib/types";

const TYPE_CONFIG: Record<
  string,
  { icon: React.ElementType; label: string; variant: "default" | "secondary" | "success" | "warning" }
> = {
  questions: {
    icon: Mail,
    label: "Discovery Questions",
    variant: "default",
  },
  answer: {
    icon: MessageSquare,
    label: "Client Answer",
    variant: "success",
  },
  change_request: {
    icon: AlertTriangle,
    label: "Change Request",
    variant: "warning",
  },
};

export function Communications({ comms }: { comms: Communication[] }) {
  const [expanded, setExpanded] = useState<string | null>(
    comms[0]?.filename || null
  );

  if (comms.length === 0) {
    return (
      <div className="text-center py-12 text-[hsl(var(--muted-foreground))]">
        <p>No communications yet.</p>
        <p className="text-sm mt-1">
          Discovery questions, client answers, and change requests will appear
          here.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {comms.map((comm) => {
        const config = TYPE_CONFIG[comm.type] || TYPE_CONFIG.answer;
        const Icon = config.icon;
        const isExpanded = expanded === comm.filename;

        return (
          <Card key={comm.filename}>
            <CardHeader
              className="cursor-pointer py-3"
              onClick={() =>
                setExpanded(isExpanded ? null : comm.filename)
              }
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Icon className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
                  <CardTitle className="text-sm">{comm.filename}</CardTitle>
                  <Badge variant={config.variant}>{config.label}</Badge>
                </div>
                {comm.date && (
                  <span className="text-xs text-[hsl(var(--muted-foreground))]">
                    {format(new Date(comm.date), "MMM d, yyyy")}
                  </span>
                )}
              </div>
            </CardHeader>
            {isExpanded && (
              <CardContent>
                <div className="border rounded-md p-4 bg-[hsl(var(--muted))] overflow-auto max-h-[400px]">
                  <article className="prose prose-sm max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {comm.content}
                    </ReactMarkdown>
                  </article>
                </div>
              </CardContent>
            )}
          </Card>
        );
      })}
    </div>
  );
}
