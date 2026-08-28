import * as React from "react";
import { Database } from "lucide-react";

export function EmptyState({ title = "No Data Found", message = "Data is currently being updated or is unavailable." }) {
  return (
    <div className="w-full p-16 border border-dashed border-[var(--border)] rounded-xl flex flex-col items-center justify-center text-center">
      <Database className="w-10 h-10 text-[var(--muted-foreground)] mb-4 opacity-50" />
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-[var(--muted-foreground)] max-w-sm">{message}</p>
    </div>
  );
}
