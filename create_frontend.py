import os

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir('frontend/components/ui')
ensure_dir('frontend/components')
ensure_dir('frontend/app')
ensure_dir('frontend/services')

files = {
    'frontend/app/globals.css': """@import "tailwindcss";

@theme {
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
}

:root {
  --background: #ffffff;
  --foreground: #09090b;
  --card: #ffffff;
  --card-foreground: #09090b;
  --popover: #ffffff;
  --popover-foreground: #09090b;
  --primary: #18181b;
  --primary-foreground: #fafafa;
  --secondary: #f4f4f5;
  --secondary-foreground: #18181b;
  --muted: #f4f4f5;
  --muted-foreground: #71717a;
  --accent: #f4f4f5;
  --accent-foreground: #18181b;
  --destructive: #ef4444;
  --destructive-foreground: #fafafa;
  --border: #e4e4e7;
  --input: #e4e4e7;
  --ring: #18181b;
  --radius: 0.5rem;
}
.dark {
  --background: #09090b;
  --foreground: #fafafa;
  --card: #09090b;
  --card-foreground: #fafafa;
  --popover: #09090b;
  --popover-foreground: #fafafa;
  --primary: #fafafa;
  --primary-foreground: #18181b;
  --secondary: #27272a;
  --secondary-foreground: #fafafa;
  --muted: #27272a;
  --muted-foreground: #a1a1aa;
  --accent: #27272a;
  --accent-foreground: #fafafa;
  --destructive: #7f1d1d;
  --destructive-foreground: #fafafa;
  --border: #27272a;
  --input: #27272a;
  --ring: #d4d4d8;
}
body {
  background-color: var(--background);
  color: var(--foreground);
  font-family: var(--font-sans), Arial, Helvetica, sans-serif;
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

@media (prefers-reduced-motion: reduce) {
  *,
  ::before,
  ::after {
    animation-delay: -1ms !important;
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    background-attachment: initial !important;
    scroll-behavior: auto !important;
    transition-duration: 0s !important;
    transition-delay: 0s !important;
  }
}
""",
    'frontend/components/theme-provider.tsx': """"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import type { ThemeProviderProps } from "next-themes";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
""",
    'frontend/components/ui/button.tsx': """import * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    let classes = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 ";
    
    if (variant === "default") classes += "bg-[var(--primary)] text-[var(--primary-foreground)] hover:opacity-90 ";
    if (variant === "outline") classes += "border border-[var(--border)] bg-transparent hover:bg-[var(--accent)] hover:text-[var(--accent-foreground)] ";
    if (variant === "ghost") classes += "hover:bg-[var(--accent)] hover:text-[var(--accent-foreground)] ";
    if (variant === "link") classes += "text-[var(--primary)] underline-offset-4 hover:underline ";

    if (size === "default") classes += "h-9 px-4 py-2 ";
    if (size === "sm") classes += "h-8 rounded-md px-3 text-xs ";
    if (size === "lg") classes += "h-10 rounded-md px-8 ";
    if (size === "icon") classes += "h-9 w-9 ";

    return (
      <button ref={ref} className={`${classes} ${className || ""}`} {...props} />
    );
  }
);
Button.displayName = "Button";

export { Button };
""",
    'frontend/components/ui/card.tsx': """import * as React from "react"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={`rounded-xl border border-[var(--border)] bg-[var(--card)] text-[var(--card-foreground)] shadow ${className || ""}`} {...props} />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={`flex flex-col space-y-1.5 p-6 ${className || ""}`} {...props} />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(({ className, ...props }, ref) => (
  <h3 ref={ref} className={`font-semibold leading-none tracking-tight ${className || ""}`} {...props} />
))
CardTitle.displayName = "CardTitle"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={`p-6 pt-0 ${className || ""}`} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={`flex items-center p-6 pt-0 ${className || ""}`} {...props} />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardTitle, CardContent, CardFooter }
""",
    'frontend/components/ui/badge.tsx': """import * as React from "react"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  let classes = "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 "
  if (variant === "default") classes += "border-transparent bg-[var(--primary)] text-[var(--primary-foreground)] hover:opacity-80 "
  if (variant === "secondary") classes += "border-transparent bg-[var(--secondary)] text-[var(--secondary-foreground)] hover:opacity-80 "
  if (variant === "outline") classes += "text-[var(--foreground)] "
  
  return (
    <div className={`${classes} ${className || ""}`} {...props} />
  )
}

export { Badge }
""",
    'frontend/components/Navbar.tsx': """"use client";
import * as React from "react";
import Link from "next/link";
import { useTheme } from "next-themes";
import { Moon, Sun, Menu } from "lucide-react";
import { Button } from "./ui/button";

export function Navbar() {
  const { setTheme, theme } = useTheme();
  
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[var(--border)] bg-[var(--background)]/95 backdrop-blur supports-[backdrop-filter]:bg-[var(--background)]/60">
      <div className="container mx-auto flex h-14 max-w-6xl items-center justify-between px-4 md:px-8">
        <div className="flex items-center space-x-4">
          <Link href="/" className="flex items-center space-x-2">
            <span className="font-bold sm:inline-block hidden">Rakshitha Gowda</span>
            <span className="font-bold sm:hidden">RG</span>
          </Link>
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <Link href="#about" className="transition-colors hover:text-[var(--foreground)] text-[var(--muted-foreground)]">About</Link>
            <Link href="#skills" className="transition-colors hover:text-[var(--foreground)] text-[var(--muted-foreground)]">Skills</Link>
            <Link href="#projects" className="transition-colors hover:text-[var(--foreground)] text-[var(--muted-foreground)]">Projects</Link>
            <Link href="#experience" className="transition-colors hover:text-[var(--foreground)] text-[var(--muted-foreground)]">Experience</Link>
            <Link href="#contact" className="transition-colors hover:text-[var(--foreground)] text-[var(--muted-foreground)]">Contact</Link>
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-end space-x-2">
          <Button variant="ghost" size="icon" onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
          <Button variant="outline" size="sm" className="hidden sm:inline-flex">Download CV</Button>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}
""",
    'frontend/components/Footer.tsx': """import * as React from "react";

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
          <a href="#" className="hover:underline">GitHub</a>
          <a href="#" className="hover:underline">LinkedIn</a>
          <a href="#" className="hover:underline">Email</a>
        </div>
      </div>
    </footer>
  );
}
""",
    'frontend/components/ProjectCard.tsx': """import * as React from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { ExternalLink, Github } from "lucide-react";

export function ProjectCard({ project }: { project: any }) {
  return (
    <Card className="flex flex-col h-full overflow-hidden transition-all hover:shadow-md">
      <div className="h-48 bg-[var(--muted)] flex items-center justify-center border-b border-[var(--border)] overflow-hidden">
        {project.project_image ? (
           <img src={project.project_image} alt={project.title} className="w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity" />
        ) : (
          <div className="font-mono text-[var(--muted-foreground)] text-4xl opacity-20">No Image</div>
        )}
      </div>
      <CardHeader>
        <div className="flex justify-between items-start">
            <CardTitle className="text-xl">{project.title}</CardTitle>
            {project.category && <Badge variant="secondary">{project.category}</Badge>}
        </div>
      </CardHeader>
      <CardContent className="flex-1">
        <p className="text-sm text-[var(--muted-foreground)] mb-4">{project.short_description}</p>
        <div className="flex flex-wrap gap-2">
          {project.technologies?.map((tech: any) => (
            <Badge key={tech.id} variant="outline" className="text-[10px] py-0">{tech.name}</Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="gap-2">
        {project.github_url && (
            <Button variant="outline" size="sm" className="w-full gap-2" asChild>
                <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                    <Github className="h-4 w-4" /> Code
                </a>
            </Button>
        )}
        {project.live_demo_url && (
            <Button variant="default" size="sm" className="w-full gap-2" asChild>
                <a href={project.live_demo_url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-4 w-4" /> Demo
                </a>
            </Button>
        )}
      </CardFooter>
    </Card>
  );
}
""",
    'frontend/services/api.ts': """export const fetchApi = async (endpoint: string) => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    const res = await fetch(`${apiUrl}${endpoint}`, {
      cache: 'no-store'
    });
    if (!res.ok) {
        if (res.status === 404) return [];
        throw new Error(`API responded with status ${res.status}`);
    }
    const data = await res.json();
    return data.results || data || [];
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    return [];
  }
};

export const getProjects = () => fetchApi('/projects/');
export const getProfile = () => fetchApi('/profile/');
export const getSkills = () => fetchApi('/skills/');
export const getExperience = () => fetchApi('/experience/');
export const getEducation = () => fetchApi('/education/');
export const getCertificates = () => fetchApi('/certificates/');
export const getSocialLinks = () => fetchApi('/social-links/');
""",
    'frontend/app/layout.tsx': """import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Rakshitha Gowda | AI & Data Science Portfolio",
  description: "Professional portfolio showcasing AI, Machine Learning, and Software Engineering projects.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-[var(--background)] font-sans antialiased selection:bg-[var(--primary)] selection:text-[var(--primary-foreground)]`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="relative flex min-h-screen flex-col">
            <Navbar />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
""",
    'frontend/app/page.tsx': """import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ProjectCard } from "@/components/ProjectCard";
import { getProjects, getProfile, getSkills, getExperience, getEducation } from "@/services/api";
import { ArrowRight, Terminal, BrainCircuit, Database, GraduationCap, Briefcase } from "lucide-react";

export default async function Home() {
  const projects = await getProjects();
  const profileData = await getProfile();
  const skills = await getSkills();
  const experience = await getExperience();
  const education = await getEducation();

  const profile = profileData.length > 0 ? profileData[0] : null;

  return (
    <div className="flex flex-col items-center">
      
      {/* Hero Section */}
      <section className="w-full py-24 md:py-32 lg:py-40 bg-[var(--background)] relative overflow-hidden border-b border-[var(--border)]">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        <div className="container mx-auto max-w-6xl px-4 md:px-8 relative z-10 flex flex-col items-start gap-6">
            <Badge variant="secondary" className="mb-4">
               <Terminal className="w-3 h-3 mr-2" /> Open to Opportunities
            </Badge>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight">
                {profile?.name || "Rakshitha Gowda"}
            </h1>
            <h2 className="text-xl md:text-3xl text-[var(--muted-foreground)] font-medium max-w-[800px]">
                {profile?.title || "AI • Machine Learning • Data Science • Full-Stack Development"}
            </h2>
            <p className="text-base md:text-lg text-[var(--muted-foreground)] max-w-[600px] leading-relaxed">
                {profile?.bio || "I build intelligent systems and data-driven applications. Passionate about machine learning, deep learning, and robust software engineering."}
            </p>
            <div className="flex flex-wrap gap-4 mt-6">
                <Button size="lg" asChild>
                    <a href="#projects">View Projects <ArrowRight className="ml-2 w-4 h-4" /></a>
                </Button>
                <Button variant="outline" size="lg" asChild>
                    <a href="#contact">Contact Me</a>
                </Button>
            </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="w-full py-20 bg-[var(--secondary)]/30 border-b border-[var(--border)]">
        <div className="container mx-auto max-w-6xl px-4 md:px-8">
            <div className="flex items-center gap-2 mb-10">
                <BrainCircuit className="w-6 h-6 text-[var(--primary)]" />
                <h2 className="text-3xl font-bold tracking-tight">Technical Arsenal</h2>
            </div>
            
            {skills.length > 0 ? (
                <div className="flex flex-wrap gap-3">
                    {skills.map((skill: any) => (
                        <Badge key={skill.id} variant="secondary" className="px-4 py-2 text-sm font-medium">
                            {skill.name} <span className="opacity-50 ml-2 text-xs">{skill.category}</span>
                        </Badge>
                    ))}
                </div>
            ) : (
                <div className="p-8 border border-dashed border-[var(--border)] rounded-xl text-center text-[var(--muted-foreground)]">
                    Skill data is currently being populated.
                </div>
            )}
        </div>
      </section>

      {/* Projects Section */}
      <section id="projects" className="w-full py-24 bg-[var(--background)] border-b border-[var(--border)]">
        <div className="container mx-auto max-w-6xl px-4 md:px-8">
            <div className="flex items-center justify-between mb-10">
                <div className="flex items-center gap-2">
                    <Database className="w-6 h-6 text-[var(--primary)]" />
                    <h2 className="text-3xl font-bold tracking-tight">Featured Work</h2>
                </div>
            </div>

            {projects.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {projects.map((project: any) => (
                        <ProjectCard key={project.id} project={project} />
                    ))}
                </div>
            ) : (
                <div className="p-16 border border-dashed border-[var(--border)] rounded-xl flex flex-col items-center justify-center text-center">
                    <Database className="w-10 h-10 text-[var(--muted-foreground)] mb-4 opacity-50" />
                    <h3 className="text-lg font-semibold mb-2">No Projects Yet</h3>
                    <p className="text-[var(--muted-foreground)] max-w-sm">Projects will appear here once they are added via the administration panel.</p>
                </div>
            )}
        </div>
      </section>

      {/* Experience & Education Section */}
      <section id="experience" className="w-full py-24 bg-[var(--secondary)]/20 border-b border-[var(--border)]">
        <div className="container mx-auto max-w-6xl px-4 md:px-8 grid grid-cols-1 md:grid-cols-2 gap-16">
            
            {/* Experience */}
            <div>
                <div className="flex items-center gap-2 mb-8">
                    <Briefcase className="w-6 h-6 text-[var(--primary)]" />
                    <h2 className="text-2xl font-bold tracking-tight">Experience</h2>
                </div>
                {experience.length > 0 ? (
                    <div className="space-y-8 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-[var(--border)]">
                        {experience.map((exp: any) => (
                             <div key={exp.id} className="relative flex items-start justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                                <div className="flex items-center justify-center w-10 h-10 rounded-full border border-[var(--border)] bg-[var(--background)] text-[var(--primary)] shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                                    <div className="w-2 h-2 rounded-full bg-[var(--primary)]"></div>
                                </div>
                                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-[var(--border)] bg-[var(--card)] shadow-sm">
                                    <div className="flex items-center justify-between space-x-2 mb-1">
                                        <h3 className="font-bold text-[var(--foreground)]">{exp.role}</h3>
                                        <time className="font-mono text-xs font-medium text-[var(--muted-foreground)]">{exp.start_date}</time>
                                    </div>
                                    <div className="text-sm font-medium text-[var(--primary)] mb-2">{exp.company}</div>
                                    <p className="text-sm text-[var(--muted-foreground)]">{exp.description}</p>
                                </div>
                             </div>
                        ))}
                    </div>
                ) : (
                    <div className="p-8 border border-dashed border-[var(--border)] rounded-xl text-center text-[var(--muted-foreground)] text-sm">
                        Experience data is currently being updated.
                    </div>
                )}
            </div>

            {/* Education */}
            <div>
                <div className="flex items-center gap-2 mb-8">
                    <GraduationCap className="w-6 h-6 text-[var(--primary)]" />
                    <h2 className="text-2xl font-bold tracking-tight">Education</h2>
                </div>
                {education.length > 0 ? (
                    <div className="space-y-8">
                        {education.map((edu: any) => (
                            <div key={edu.id} className="p-6 rounded-xl border border-[var(--border)] bg-[var(--card)] shadow-sm">
                                <h3 className="font-bold text-lg mb-1">{edu.degree}</h3>
                                <div className="text-[var(--primary)] font-medium mb-2">{edu.institution}</div>
                                <div className="text-sm text-[var(--muted-foreground)] font-mono mb-4">{edu.start_date} - {edu.end_date || 'Present'}</div>
                                {edu.description && <p className="text-sm text-[var(--muted-foreground)]">{edu.description}</p>}
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="p-8 border border-dashed border-[var(--border)] rounded-xl text-center text-[var(--muted-foreground)] text-sm">
                        Academic background is currently being updated.
                    </div>
                )}
            </div>
        </div>
      </section>

      {/* AI Lab & Contact Teaser */}
      <section id="contact" className="w-full py-32 bg-[var(--background)]">
        <div className="container mx-auto max-w-4xl px-4 md:px-8 text-center flex flex-col items-center">
            <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-6">Let's build something meaningful.</h2>
            <p className="text-lg text-[var(--muted-foreground)] mb-10 max-w-2xl">
                Interested in AI, machine learning, or software engineering collaboration? I'm currently exploring new opportunities. Interactive AI Lab coming in Phase 4.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
                <Button size="lg">Contact Me</Button>
                <Button variant="outline" size="lg">Explore AI Lab (Coming Soon)</Button>
            </div>
        </div>
      </section>
      
    </div>
  );
}
"""
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Created all frontend UI components and pages.")
