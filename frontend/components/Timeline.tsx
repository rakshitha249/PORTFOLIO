import * as React from "react";

export function Timeline({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-8 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-[var(--border)]">
      {children}
    </div>
  );
}

export function TimelineItem({
  title,
  subtitle,
  date,
  description,
}: {
  title: string;
  subtitle?: string;
  date: string;
  description?: string;
}) {
  return (
    <div className="relative flex items-start justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
      <div className="flex items-center justify-center w-10 h-10 rounded-full border border-[var(--border)] bg-[var(--background)] text-[var(--primary)] shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
        <div className="w-2 h-2 rounded-full bg-[var(--primary)]"></div>
      </div>
      <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-[var(--border)] bg-[var(--card)] shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between space-y-1 sm:space-y-0 sm:space-x-2 mb-1">
          <h3 className="font-bold text-[var(--foreground)]">{title}</h3>
          <time className="font-mono text-xs font-medium text-[var(--muted-foreground)]">{date}</time>
        </div>
        {subtitle && <div className="text-sm font-medium text-[var(--primary)] mb-2">{subtitle}</div>}
        {description && <p className="text-sm text-[var(--muted-foreground)]">{description}</p>}
      </div>
    </div>
  );
}
