import { formatDistanceToNow, format } from "date-fns";
import type { TimelineEvent } from "@/lib/types";
import {
  FileText,
  Search,
  HelpCircle,
  BarChart3,
  Upload,
  GitBranch,
  AlertTriangle,
  CheckCircle,
  Package,
  FileSpreadsheet,
} from "lucide-react";

const EVENT_CONFIG: Record<
  string,
  { icon: React.ElementType; label: string; color: string }
> = {
  project_created: {
    icon: Package,
    label: "Project created",
    color: "text-slate-500",
  },
  files_ingested: {
    icon: FileText,
    label: "Files ingested",
    color: "text-blue-600",
  },
  overview_generated: {
    icon: Search,
    label: "Overview generated",
    color: "text-indigo-600",
  },
  questions_generated: {
    icon: HelpCircle,
    label: "Discovery questions generated",
    color: "text-purple-600",
  },
  breakdown_generated: {
    icon: BarChart3,
    label: "Breakdown generated",
    color: "text-cyan-600",
  },
  breakdown_exported: {
    icon: FileSpreadsheet,
    label: "Breakdown exported to Excel",
    color: "text-cyan-500",
  },
  push_ready_generated: {
    icon: CheckCircle,
    label: "Push-ready stories generated",
    color: "text-green-600",
  },
  pushed_to_ado: {
    icon: Upload,
    label: "Pushed to Azure DevOps",
    color: "text-green-700",
  },
  change_request: {
    icon: AlertTriangle,
    label: "Change request",
    color: "text-amber-600",
  },
  code_generated: {
    icon: GitBranch,
    label: "Feature code generated",
    color: "text-violet-600",
  },
};

function EventDetail({ data }: { data: Record<string, unknown> }) {
  const entries = Object.entries(data).filter(
    ([, v]) => v !== null && v !== undefined && v !== ""
  );
  if (entries.length === 0) return null;

  return (
    <div className="mt-2 text-sm text-[hsl(var(--muted-foreground))]">
      {entries.map(([key, value]) => (
        <div key={key} className="flex gap-2">
          <span className="font-medium min-w-[80px]">
            {key.replace(/_/g, " ")}:
          </span>
          <span>
            {Array.isArray(value)
              ? value.length > 3
                ? `${value.slice(0, 3).join(", ")} (+${value.length - 3} more)`
                : value.join(", ")
              : String(value)}
          </span>
        </div>
      ))}
    </div>
  );
}

export function Timeline({ events }: { events: TimelineEvent[] }) {
  if (events.length === 0) {
    return (
      <div className="text-center py-12 text-[hsl(var(--muted-foreground))]">
        <p>No events yet. Start by ingesting requirements.</p>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Vertical line */}
      <div className="absolute left-[19px] top-3 bottom-3 w-px bg-[hsl(var(--border))]" />

      <div className="space-y-1">
        {events.map((event, i) => {
          const config = EVENT_CONFIG[event.type] || {
            icon: FileText,
            label: event.type.replace(/_/g, " "),
            color: "text-slate-500",
          };
          const Icon = config.icon;
          const date = new Date(event.timestamp);

          return (
            <div key={`${event.type}-${i}`} className="relative flex gap-4 py-3">
              {/* Icon */}
              <div
                className={`relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[hsl(var(--card))] border ${config.color}`}
              >
                <Icon className="h-4 w-4" />
              </div>

              {/* Content */}
              <div className="flex-1 pt-1">
                <div className="flex items-baseline justify-between gap-4">
                  <h4 className="text-sm font-medium">{config.label}</h4>
                  <time
                    className="shrink-0 text-xs text-[hsl(var(--muted-foreground))]"
                    title={format(date, "PPpp")}
                  >
                    {format(date, "MMM d, yyyy")}
                    <span className="ml-1 opacity-60">
                      ({formatDistanceToNow(date, { addSuffix: true })})
                    </span>
                  </time>
                </div>
                <EventDetail data={event.data} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
