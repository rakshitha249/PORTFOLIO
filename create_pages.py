import os

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir('frontend/components/ui')
ensure_dir('frontend/components')
ensure_dir('frontend/app/about')
ensure_dir('frontend/app/skills')
ensure_dir('frontend/app/education')
ensure_dir('frontend/app/experience')
ensure_dir('frontend/app/projects/[slug]')
ensure_dir('frontend/app/certifications')
ensure_dir('frontend/app/resume')

files = {
    'frontend/services/api.ts': """export const fetchApi = async (endpoint: string) => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    const res = await fetch(`${apiUrl}${endpoint}`, {
      cache: 'no-store'
    });
    if (!res.ok) {
        if (res.status === 404) return null;
        throw new Error(`API responded with status ${res.status}`);
    }
    const data = await res.json();
    return data.results !== undefined ? data.results : data;
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    return null;
  }
};

export const getProjects = () => fetchApi('/projects/').then(r => r || []);
export const getProjectBySlug = (slug: string) => fetchApi(`/projects/${slug}/`);
export const getProfile = () => fetchApi('/profile/').then(r => r || []);
export const getSkills = () => fetchApi('/skills/').then(r => r || []);
export const getExperience = () => fetchApi('/experience/').then(r => r || []);
export const getEducation = () => fetchApi('/education/').then(r => r || []);
export const getCertificates = () => fetchApi('/certificates/').then(r => r || []);
export const getSocialLinks = () => fetchApi('/social-links/').then(r => r || []);
""",

    'frontend/components/Navbar.tsx': """"use client";
import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { Moon, Sun, Menu } from "lucide-react";
import { Button } from "./ui/button";

export function Navbar() {
  const { setTheme, theme } = useTheme();
  const pathname = usePathname();
  
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
          <Link href="/" className="flex items-center space-x-2">
            <span className="font-bold sm:inline-block hidden">Rakshitha Gowda</span>
            <span className="font-bold sm:hidden">RG</span>
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
          <Button variant="outline" size="sm" className="hidden sm:inline-flex" asChild>
            <Link href="/resume">Resume</Link>
          </Button>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}
""",
    'frontend/components/Timeline.tsx': """import * as React from "react";

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
""",
    'frontend/components/EmptyState.tsx': """import * as React from "react";
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
""",
    'frontend/app/page.tsx': """import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ProjectCard } from "@/components/ProjectCard";
import { Timeline, TimelineItem } from "@/components/Timeline";
import { EmptyState } from "@/components/EmptyState";
import { getProjects, getProfile, getSkills, getExperience, getEducation } from "@/services/api";
import { ArrowRight, Terminal, BrainCircuit, Database, GraduationCap, Briefcase } from "lucide-react";
import Link from "next/link";

export default async function Home() {
  const projects = await getProjects();
  const profileData = await getProfile();
  const skills = await getSkills();
  const experience = await getExperience();
  const education = await getEducation();

  const profile = profileData.length > 0 ? profileData[0] : null;

  return (
    <div className="flex flex-col items-center">
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
                    <Link href="/projects">View Projects <ArrowRight className="ml-2 w-4 h-4" /></Link>
                </Button>
                <Button variant="outline" size="lg" asChild>
                    <a href="#contact">Contact Me</a>
                </Button>
            </div>
        </div>
      </section>

      <section className="w-full py-20 bg-[var(--secondary)]/30 border-b border-[var(--border)]">
        <div className="container mx-auto max-w-6xl px-4 md:px-8">
            <div className="flex justify-between items-end mb-10">
               <div className="flex items-center gap-2">
                   <BrainCircuit className="w-6 h-6 text-[var(--primary)]" />
                   <h2 className="text-3xl font-bold tracking-tight">Technical Arsenal</h2>
               </div>
               <Button variant="ghost" asChild>
                 <Link href="/skills">View All <ArrowRight className="ml-2 w-4 h-4" /></Link>
               </Button>
            </div>
            {skills.length > 0 ? (
                <div className="flex flex-wrap gap-3">
                    {skills.slice(0, 10).map((skill: any) => (
                        <Badge key={skill.id} variant="secondary" className="px-4 py-2 text-sm font-medium">
                            {skill.name} <span className="opacity-50 ml-2 text-xs">{skill.category}</span>
                        </Badge>
                    ))}
                </div>
            ) : (
                <EmptyState title="No Skills Found" message="Skill data is currently being populated." />
            )}
        </div>
      </section>

      <section className="w-full py-24 bg-[var(--background)] border-b border-[var(--border)]">
        <div className="container mx-auto max-w-6xl px-4 md:px-8">
            <div className="flex items-center justify-between mb-10">
                <div className="flex items-center gap-2">
                    <Database className="w-6 h-6 text-[var(--primary)]" />
                    <h2 className="text-3xl font-bold tracking-tight">Featured Work</h2>
                </div>
                <Button variant="ghost" asChild>
                    <Link href="/projects">View All Projects <ArrowRight className="ml-2 w-4 h-4" /></Link>
                </Button>
            </div>
            {projects.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {projects.slice(0, 3).map((project: any) => (
                        <ProjectCard key={project.id} project={project} />
                    ))}
                </div>
            ) : (
                <EmptyState title="No Projects Yet" message="Projects will appear here once they are added via the administration panel." />
            )}
        </div>
      </section>

      <section className="w-full py-24 bg-[var(--secondary)]/20 border-b border-[var(--border)]">
        <div className="container mx-auto max-w-6xl px-4 md:px-8 grid grid-cols-1 lg:grid-cols-2 gap-16">
            <div>
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-2">
                        <Briefcase className="w-6 h-6 text-[var(--primary)]" />
                        <h2 className="text-2xl font-bold tracking-tight">Experience</h2>
                    </div>
                    <Button variant="link" asChild>
                       <Link href="/experience">Full Experience</Link>
                    </Button>
                </div>
                {experience.length > 0 ? (
                    <Timeline>
                        {experience.slice(0, 3).map((exp: any) => (
                             <TimelineItem 
                                key={exp.id} 
                                title={exp.role} 
                                subtitle={exp.company} 
                                date={`${exp.start_date} - ${exp.end_date || 'Present'}`} 
                                description={exp.description} 
                             />
                        ))}
                    </Timeline>
                ) : (
                    <EmptyState title="Experience Unavailable" message="Experience data is currently being updated." />
                )}
            </div>
            <div>
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-2">
                        <GraduationCap className="w-6 h-6 text-[var(--primary)]" />
                        <h2 className="text-2xl font-bold tracking-tight">Education</h2>
                    </div>
                    <Button variant="link" asChild>
                       <Link href="/education">Full Education</Link>
                    </Button>
                </div>
                {education.length > 0 ? (
                    <div className="space-y-6">
                        {education.slice(0, 3).map((edu: any) => (
                            <div key={edu.id} className="p-6 rounded-xl border border-[var(--border)] bg-[var(--card)] shadow-sm">
                                <h3 className="font-bold text-lg mb-1">{edu.degree}</h3>
                                <div className="text-[var(--primary)] font-medium mb-2">{edu.institution}</div>
                                <div className="text-sm text-[var(--muted-foreground)] font-mono mb-4">{edu.start_date} - {edu.end_date || 'Present'}</div>
                                {edu.description && <p className="text-sm text-[var(--muted-foreground)]">{edu.description}</p>}
                            </div>
                        ))}
                    </div>
                ) : (
                    <EmptyState title="Education Unavailable" message="Academic background is currently being updated." />
                )}
            </div>
        </div>
      </section>

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
""",
    'frontend/app/about/page.tsx': """import { getProfile } from "@/services/api";
import { EmptyState } from "@/components/EmptyState";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About | Portfolio",
  description: "Learn more about my professional background and interests.",
};

export default async function AboutPage() {
  const profileData = await getProfile();
  const profile = profileData.length > 0 ? profileData[0] : null;

  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-8">About Me</h1>
      {profile ? (
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-xl text-[var(--muted-foreground)] leading-relaxed mb-8">
            {profile.bio}
          </p>
          <div className="grid md:grid-cols-2 gap-8">
              <div className="p-6 bg-[var(--secondary)] rounded-xl">
                  <h3 className="font-semibold text-lg mb-2">Professional Summary</h3>
                  <p className="text-[var(--muted-foreground)]">Driven software engineer with a strong foundation in machine learning and data science.</p>
              </div>
              <div className="p-6 bg-[var(--secondary)] rounded-xl">
                  <h3 className="font-semibold text-lg mb-2">Technical Focus</h3>
                  <p className="text-[var(--muted-foreground)]">Specializing in AI architectures, backend systems, and modern web applications.</p>
              </div>
          </div>
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
""",
    'frontend/app/skills/page.tsx': """import { getSkills } from "@/services/api";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/EmptyState";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Skills | Portfolio",
  description: "Technical skills and proficiencies.",
};

export default async function SkillsPage() {
  const skills = await getSkills();
  
  // Group skills by category
  const categorizedSkills = skills.reduce((acc: any, skill: any) => {
      const cat = skill.category || "Other";
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(skill);
      return acc;
  }, {});

  return (
    <div className="container mx-auto max-w-5xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-12">Technical Skills</h1>
      {skills.length > 0 ? (
        <div className="grid gap-10">
          {Object.entries(categorizedSkills).map(([category, items]: [string, any]) => (
              <div key={category}>
                  <h2 className="text-2xl font-bold mb-4 border-b border-[var(--border)] pb-2">{category}</h2>
                  <div className="flex flex-wrap gap-3">
                      {items.map((skill: any) => (
                          <Badge key={skill.id} variant="secondary" className="px-4 py-2 text-base">
                              {skill.name} {skill.proficiency && <span className="ml-2 opacity-50 text-xs">({skill.proficiency})</span>}
                          </Badge>
                      ))}
                  </div>
              </div>
          ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
""",
    'frontend/app/experience/page.tsx': """import { getExperience } from "@/services/api";
import { Timeline, TimelineItem } from "@/components/Timeline";
import { EmptyState } from "@/components/EmptyState";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Experience | Portfolio",
  description: "Professional work experience and roles.",
};

export default async function ExperiencePage() {
  const experience = await getExperience();

  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-12">Experience</h1>
      {experience.length > 0 ? (
        <Timeline>
            {experience.map((exp: any) => (
                <TimelineItem 
                    key={exp.id} 
                    title={exp.role} 
                    subtitle={exp.company} 
                    date={`${exp.start_date} - ${exp.end_date || 'Present'}`} 
                    description={exp.description} 
                />
            ))}
        </Timeline>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
""",
    'frontend/app/education/page.tsx': """import { getEducation } from "@/services/api";
import { EmptyState } from "@/components/EmptyState";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Education | Portfolio",
  description: "Academic background and degrees.",
};

export default async function EducationPage() {
  const education = await getEducation();

  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-12">Education</h1>
      {education.length > 0 ? (
        <div className="space-y-8">
            {education.map((edu: any) => (
                <div key={edu.id} className="p-8 rounded-2xl border border-[var(--border)] bg-[var(--card)] shadow-sm">
                    <h3 className="font-bold text-2xl mb-2">{edu.degree}</h3>
                    <div className="text-[var(--primary)] font-semibold text-lg mb-2">{edu.institution}</div>
                    <div className="text-sm text-[var(--muted-foreground)] font-mono mb-6 bg-[var(--muted)] inline-block px-3 py-1 rounded-full">
                        {edu.start_date} - {edu.end_date || 'Present'}
                    </div>
                    {edu.description && <p className="text-[var(--muted-foreground)] leading-relaxed">{edu.description}</p>}
                </div>
            ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
""",
    'frontend/app/certifications/page.tsx': """import { getCertificates } from "@/services/api";
import { EmptyState } from "@/components/EmptyState";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Metadata } from "next";
import { Award, ExternalLink } from "lucide-react";

export const metadata: Metadata = {
  title: "Certifications | Portfolio",
  description: "Professional certifications and awards.",
};

export default async function CertificationsPage() {
  const certificates = await getCertificates();

  return (
    <div className="container mx-auto max-w-5xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-12">Certifications</h1>
      {certificates.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {certificates.map((cert: any) => (
                <Card key={cert.id} className="hover:shadow-md transition-shadow">
                    <CardHeader className="pb-3">
                        <div className="flex justify-between items-start">
                            <CardTitle className="text-xl leading-tight">{cert.name}</CardTitle>
                            <Award className="text-[var(--primary)] h-6 w-6 shrink-0 ml-4" />
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="font-medium text-[var(--muted-foreground)] mb-2">{cert.issuer}</div>
                        <Badge variant="secondary" className="mb-4">{cert.issue_date}</Badge>
                        {cert.description && <p className="text-sm text-[var(--muted-foreground)] mb-4">{cert.description}</p>}
                        {cert.credential_url && (
                            <a href={cert.credential_url} target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-[var(--primary)] hover:underline inline-flex items-center">
                                View Credential <ExternalLink className="ml-1 h-3 w-3" />
                            </a>
                        )}
                    </CardContent>
                </Card>
            ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
""",
    'frontend/app/resume/page.tsx': """import { EmptyState } from "@/components/EmptyState";
import { Button } from "@/components/ui/button";
import type { Metadata } from "next";
import { FileDown } from "lucide-react";

export const metadata: Metadata = {
  title: "Resume | Portfolio",
  description: "Professional resume.",
};

export default function ResumePage() {
  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16 flex flex-col items-center">
      <h1 className="text-4xl font-extrabold tracking-tight mb-8">Resume</h1>
      
      <div className="w-full max-w-2xl">
          <EmptyState title="Resume Coming Soon" message="The resume document is currently being finalized and will be available for download shortly." />
          <div className="mt-8 flex justify-center">
              <Button disabled size="lg"><FileDown className="mr-2 h-4 w-4" /> Download Resume</Button>
          </div>
      </div>
    </div>
  );
}
""",
    'frontend/app/projects/page.tsx': """import { getProjects } from "@/services/api";
import { ProjectCard } from "@/components/ProjectCard";
import { EmptyState } from "@/components/EmptyState";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Projects | Portfolio",
  description: "Portfolio of software engineering and AI projects.",
};

export default async function ProjectsPage() {
  const projects = await getProjects();

  return (
    <div className="container mx-auto max-w-6xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-4">Projects</h1>
      <p className="text-lg text-[var(--muted-foreground)] mb-12 max-w-2xl">
          A showcase of my recent work in AI, Data Science, and Full-Stack Engineering.
      </p>
      
      {projects.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {projects.map((project: any) => (
                <ProjectCard key={project.id} project={project} />
            ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
""",
    'frontend/app/projects/[slug]/page.tsx': """import { getProjectBySlug, getProjects } from "@/services/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/EmptyState";
import { Code, ExternalLink, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";

export async function generateStaticParams() {
  const projects = await getProjects();
  return projects.map((p: any) => ({ slug: p.slug }));
}

export default async function ProjectDetailPage({ params }: { params: { slug: string } }) {
  const project = await getProjectBySlug(params.slug);
  
  if (!project) {
      notFound();
  }

  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-12">
      <Button variant="ghost" className="mb-8 -ml-4" asChild>
          <Link href="/projects"><ArrowLeft className="mr-2 h-4 w-4" /> Back to Projects</Link>
      </Button>

      <div className="space-y-8">
          <div>
              <div className="flex gap-2 mb-4">
                  {project.category && <Badge>{project.category}</Badge>}
                  {project.is_published && <Badge variant="outline">Published</Badge>}
              </div>
              <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">{project.title}</h1>
              <p className="text-xl text-[var(--muted-foreground)] leading-relaxed">
                  {project.short_description}
              </p>
          </div>

          <div className="flex flex-wrap gap-4">
              {project.github_url && (
                  <Button asChild>
                      <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                          <Code className="mr-2 h-4 w-4" /> View Source
                      </a>
                  </Button>
              )}
              {project.live_demo_url && (
                  <Button variant="outline" asChild>
                      <a href={project.live_demo_url} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="mr-2 h-4 w-4" /> Live Demo
                      </a>
                  </Button>
              )}
          </div>

          {project.project_image && (
              <div className="w-full aspect-video bg-[var(--muted)] rounded-xl overflow-hidden border border-[var(--border)]">
                  <img src={project.project_image} alt={project.title} className="w-full h-full object-cover" />
              </div>
          )}

          <div className="prose dark:prose-invert max-w-none pt-8 border-t border-[var(--border)]">
              <h2>Project Overview</h2>
              <div className="whitespace-pre-wrap">{project.full_description || "Detailed description is not available."}</div>
              
              {project.technologies && project.technologies.length > 0 && (
                  <>
                      <h3>Technology Stack</h3>
                      <div className="flex flex-wrap gap-2">
                          {project.technologies.map((tech: any) => (
                              <Badge key={tech.id} variant="secondary">{tech.name}</Badge>
                          ))}
                      </div>
                  </>
              )}

              {project.metrics && project.metrics.length > 0 && (
                  <>
                      <h3>Metrics & Results</h3>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 not-prose">
                          {project.metrics.map((metric: any) => (
                              <div key={metric.id} className="p-4 bg-[var(--secondary)] rounded-lg text-center">
                                  <div className="text-2xl font-bold text-[var(--foreground)]">{metric.value}</div>
                                  <div className="text-sm text-[var(--muted-foreground)]">{metric.name}</div>
                              </div>
                          ))}
                      </div>
                  </>
              )}
          </div>
      </div>
    </div>
  );
}
"""
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Created all dedicated pages and components.")
