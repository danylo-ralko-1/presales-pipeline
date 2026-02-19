import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function OverviewViewer({ content }: { content: string }) {
  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="px-4 py-2.5 border-b bg-[hsl(var(--muted))]">
        <h3 className="text-sm font-medium">overview.md</h3>
      </div>
      <div className="p-5 overflow-auto max-h-[700px]">
        <article className="prose prose-sm max-w-none prose-headings:font-semibold prose-h1:text-xl prose-h2:text-lg prose-h3:text-base prose-table:text-sm">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        </article>
      </div>
    </div>
  );
}
