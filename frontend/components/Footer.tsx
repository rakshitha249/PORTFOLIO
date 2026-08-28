import * as React from "react";

export function Footer() {
  return (
    <footer className="border-t border-[var(--border)] bg-[var(--background)]">
      <div className="container mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 py-10 md:h-24 md:flex-row md:py-0 px-4 md:px-8">
        <div className="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
          <p className="text-center text-sm leading-loose text-[var(--muted-foreground)] md:text-left">
            Built by Rakshitha Gowda. AI & Data Science Portfolio.
          </p>
        </div>
        <div className="flex items-center space-x-4 text-sm text-[var(--muted-foreground)]">
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="hover:underline">GitHub</a>
          <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="hover:underline">LinkedIn</a>
          <a href="/about" className="hover:underline">About</a>
        </div>
      </div>
    </footer>
  );
}
