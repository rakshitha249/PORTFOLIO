"use client";
import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { Moon, Sun, Menu, X } from "lucide-react";
import { Button } from "./ui/button";

export function Navbar() {
  const { setTheme, theme } = useTheme();
  const pathname = usePathname();
  const [isOpen, setIsOpen] = React.useState(false);
  
  const links = [
    { href: "/about", label: "About" },
    { href: "/skills", label: "Skills" },
    { href: "/projects", label: "Projects" },
    { href: "/experience", label: "Experience" },
    { href: "/education", label: "Education" },
    { href: "/certifications", label: "Certifications" },
  ];
  
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[var(--border)] bg-[var(--background)]/95 backdrop-blur supports-[backdrop-filter]:bg-[var(--background)]/60">
      <div className="container mx-auto flex h-14 max-w-6xl items-center justify-between px-4 md:px-8">
        <div className="flex items-center space-x-4">
          <Link href="/" className="flex items-center space-x-2 shrink-0">
            <span className="font-bold md:inline-block hidden">Rakshitha S S</span>
            <span className="font-bold md:hidden">RG</span>
          </Link>
          <nav className="hidden md:flex items-center space-x-4 lg:space-x-6 text-sm font-medium">
            {links.map((link) => (
               <Link key={link.href} href={link.href} className={`transition-colors hover:text-[var(--foreground)] ${pathname?.startsWith(link.href) ? "text-[var(--foreground)] font-semibold" : "text-[var(--muted-foreground)]"}`}>
                  {link.label}
               </Link>
            ))}
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-end space-x-2">
          <Button variant="ghost" size="icon" onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
          <Button variant="outline" size="sm" className="shrink-0" asChild>
            <Link href="/resume">Resume</Link>
          </Button>
          <Button variant="ghost" size="icon" className="md:hidden shrink-0" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>
      </div>
      {isOpen && (
        <div className="md:hidden border-t border-[var(--border)] bg-[var(--background)]">
          <nav className="flex flex-col space-y-4 p-4 text-sm font-medium">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className={`transition-colors hover:text-[var(--foreground)] ${pathname?.startsWith(link.href) ? "text-[var(--foreground)] font-semibold" : "text-[var(--muted-foreground)]"}`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
}
