"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { format } from "date-fns";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Send,
  Paperclip,
  X,
  FileText,
  MessageSquare,
  Upload,
  User,
  Bot,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { ChatMessage } from "@/lib/chat";

export function ChatPanel({
  projectName,
  initialMessages,
}: {
  projectName: string;
  initialMessages: ChatMessage[];
}) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [text, setText] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [sending, setSending] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSubmit = async () => {
    if (!text.trim() && files.length === 0) return;

    setSending(true);
    const formData = new FormData();
    formData.append("text", text);
    for (const f of files) {
      formData.append("files", f);
    }

    // Optimistic user message
    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      text,
      files: files.map((f) => ({ name: f.name, savedTo: "" })),
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setText("");
    setFiles([]);

    try {
      const res = await fetch(`/api/projects/${projectName}/chat`, {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        // Refresh messages from server to get system response
        const allMessages = await fetch(
          `/api/projects/${projectName}/chat`
        ).then((r) => r.json());
        setMessages(allMessages);
      }
    } catch (err) {
      console.error("Failed to send message:", err);
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...dropped]);
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div
        className="flex-1 overflow-auto p-4 space-y-4"
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        {messages.length === 0 && (
          <div className="text-center py-12 text-[hsl(var(--muted-foreground))]">
            <MessageSquare className="h-8 w-8 mx-auto mb-3 opacity-40" />
            <p className="text-sm font-medium">Drop files or type a message</p>
            <p className="text-xs mt-1">
              Requirements go to input/, client answers to answers/, change
              requests to changes/
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={cn(
              "flex gap-3",
              msg.role === "user" ? "justify-end" : "justify-start"
            )}
          >
            {msg.role === "system" && (
              <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[hsl(var(--muted))]">
                <Bot className="h-3.5 w-3.5" />
              </div>
            )}
            <div
              className={cn(
                "max-w-[80%] rounded-lg px-3.5 py-2.5 text-sm",
                msg.role === "user"
                  ? "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]"
                  : "bg-[hsl(var(--muted))]"
              )}
            >
              {msg.text && (
                <div className={cn(
                  "prose prose-sm max-w-none",
                  msg.role === "user" && "prose-invert"
                )}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>
              )}
              {msg.files && msg.files.length > 0 && (
                <div className="mt-2 space-y-1">
                  {msg.files.map((f, i) => (
                    <div
                      key={i}
                      className={cn(
                        "flex items-center gap-1.5 text-xs",
                        msg.role === "user" ? "opacity-80" : "opacity-70"
                      )}
                    >
                      <FileText className="h-3 w-3" />
                      <span>{f.name}</span>
                      {f.savedTo && (
                        <span className="opacity-60">→ {f.savedTo}</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
              <div
                className={cn(
                  "text-[10px] mt-1.5",
                  msg.role === "user" ? "opacity-50" : "opacity-40"
                )}
              >
                {format(new Date(msg.timestamp), "HH:mm")}
              </div>
            </div>
            {msg.role === "user" && (
              <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[hsl(var(--primary))]">
                <User className="h-3.5 w-3.5 text-[hsl(var(--primary-foreground))]" />
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Drop overlay */}
      {dragOver && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-[hsl(var(--background))]/80 border-2 border-dashed border-[hsl(var(--primary))] rounded-lg">
          <div className="text-center">
            <Upload className="h-8 w-8 mx-auto mb-2 text-[hsl(var(--primary))]" />
            <p className="text-sm font-medium">Drop files here</p>
          </div>
        </div>
      )}

      {/* Attached files preview */}
      {files.length > 0 && (
        <div className="px-3 py-2 border-t flex flex-wrap gap-2">
          {files.map((f, i) => (
            <div
              key={i}
              className="flex items-center gap-1.5 bg-[hsl(var(--muted))] rounded-md px-2 py-1 text-xs"
            >
              <FileText className="h-3 w-3" />
              <span className="max-w-[120px] truncate">{f.name}</span>
              <button
                onClick={() => removeFile(i)}
                className="hover:text-[hsl(var(--destructive))] transition-colors"
              >
                <X className="h-3 w-3" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="border-t p-3">
        <div className="flex items-end gap-2">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md hover:bg-[hsl(var(--accent))] transition-colors text-[hsl(var(--muted-foreground))]"
            title="Attach files"
          >
            <Paperclip className="h-4 w-4" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className="hidden"
            onChange={(e) => {
              if (e.target.files) {
                setFiles((prev) => [...prev, ...Array.from(e.target.files!)]);
              }
              e.target.value = "";
            }}
          />
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message or drop files..."
            rows={1}
            className="flex-1 resize-none rounded-md border bg-transparent px-3 py-2 text-sm placeholder:text-[hsl(var(--muted-foreground))] focus:outline-none focus:ring-1 focus:ring-[hsl(var(--ring))]"
          />
          <button
            onClick={handleSubmit}
            disabled={sending || (!text.trim() && files.length === 0)}
            className={cn(
              "flex h-9 w-9 shrink-0 items-center justify-center rounded-md transition-colors",
              sending || (!text.trim() && files.length === 0)
                ? "opacity-30 cursor-not-allowed"
                : "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] hover:opacity-90"
            )}
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
