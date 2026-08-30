import { getProjectBySlug, getProjects } from "@/services/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/EmptyState";
import {
  Code,
  ExternalLink,
  ArrowLeft,
  Brain,
  Cpu,
  Database,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Compass,
  Activity,
  Layers
} from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";

export async function generateStaticParams() {
  const projects = await getProjects();
  return projects.map((p: any) => ({ slug: p.slug }));
}

export default async function ProjectDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;
  const project = await getProjectBySlug(resolvedParams.slug);
  
  if (!project) {
      notFound();
  }

  // Parse Applications from full_description if present (custom formatting)
  let overviewText = project.full_description || "";
  let applications: string[] = [];
  if (overviewText.includes("### Applications")) {
      const parts = overviewText.split("### Applications");
      overviewText = parts[0].trim();
      applications = parts[1]
          .split("\n")
          .map((line: string) => line.replace(/^-\s*/, "").trim())
          .filter((line: string) => line.length > 0);
  }

  return (
    <div className="min-h-screen bg-[var(--background)] text-[var(--foreground)] pb-20">
      {/* Top Navigation / Sticky Bar */}
      <div className="border-b border-[var(--border)] bg-[var(--background)]/50 backdrop-blur-md sticky top-0 z-10 py-4 mb-8">
        <div className="container mx-auto max-w-6xl px-4 md:px-8 flex justify-between items-center">
          <Link href="/projects" className="inline-flex items-center text-sm font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Projects
          </Link>
          <div className="flex gap-2">
            {project.category && <Badge variant="secondary">{project.category}</Badge>}
            {project.is_published && <Badge variant="outline">Case Study</Badge>}
          </div>
        </div>
      </div>

      <div className="container mx-auto max-w-6xl px-4 md:px-8">
        <div className="space-y-8">
          {/* Hero Section */}
          <div className="max-w-4xl">
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 bg-gradient-to-r from-[var(--foreground)] to-[var(--muted-foreground)] bg-clip-text text-transparent">
              {project.title}
            </h1>
            <p className="text-xl md:text-2xl text-[var(--muted-foreground)] leading-relaxed font-light mb-8">
              {project.short_description}
            </p>

            {/* Quick Actions */}
            <div className="flex flex-wrap gap-4">
              {project.github_url && (
                <Button asChild className="hover:scale-105 transition-transform duration-200">
                  <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                    <Code className="mr-2 h-4 w-4" /> View Source Code
                  </a>
                </Button>
              )}
              {project.live_demo_url && (
                <Button variant="outline" asChild className="hover:scale-105 transition-transform duration-200">
                  <a href={project.live_demo_url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="mr-2 h-4 w-4" /> Live Demo
                  </a>
                </Button>
              )}
            </div>
          </div>

          {/* Main Screenshot/Banner Image */}
          {project.project_image && (
            <div className="w-full aspect-[21/9] max-h-[480px] bg-[var(--secondary)] rounded-2xl overflow-hidden border border-[var(--border)] shadow-2xl relative group">
              <img
                src={project.project_image}
                alt={project.title}
                className="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-500 ease-out"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[var(--background)]/35 to-transparent pointer-events-none" />
            </div>
          )}

          {/* Grid Layout: Main Case Study vs Sidebar */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 pt-8">
            {/* Left Column: Case Study Main Sections */}
            <div className="lg:col-span-2 space-y-12">
              
              {/* Project Overview */}
              <section className="space-y-4">
                <div className="flex items-center gap-3">
                  <Cpu className="h-6 w-6 text-[var(--primary)]" />
                  <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Project Overview</h2>
                </div>
                <div className="text-[var(--muted-foreground)] leading-relaxed whitespace-pre-wrap text-lg bg-[var(--secondary)]/20 p-6 rounded-xl border border-[var(--border)]/50">
                  {overviewText || "Detailed description is not available."}
                </div>
              </section>

              {/* Challenge vs Solution Grid */}
              {(project.problem_statement || project.solution) && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {project.problem_statement && (
                    <div className="p-6 bg-[var(--secondary)]/30 rounded-xl border border-[var(--border)]/50 hover:border-red-500/20 transition-colors duration-300">
                      <div className="flex items-center gap-2 mb-4 text-red-400">
                        <AlertCircle className="h-5 w-5" />
                        <h3 className="text-xl font-bold">The Problem</h3>
                      </div>
                      <p className="text-[var(--muted-foreground)] leading-relaxed text-sm">
                        {project.problem_statement}
                      </p>
                    </div>
                  )}
                  {project.solution && (
                    <div className="p-6 bg-[var(--secondary)]/30 rounded-xl border border-[var(--border)]/50 hover:border-emerald-500/20 transition-colors duration-300">
                      <div className="flex items-center gap-2 mb-4 text-emerald-400">
                        <CheckCircle2 className="h-5 w-5" />
                        <h3 className="text-xl font-bold">The Solution</h3>
                      </div>
                      <p className="text-[var(--muted-foreground)] leading-relaxed text-sm">
                        {project.solution}
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* ML Model details */}
              {project.ml_models && (
                <section className="space-y-4">
                  <div className="flex items-center gap-3">
                    <Brain className="h-6 w-6 text-[var(--primary)]" />
                    <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Machine Learning Model</h2>
                  </div>
                  <div className="p-6 bg-[var(--secondary)]/30 rounded-xl border border-[var(--border)]/50">
                    <div className="text-[var(--muted-foreground)] leading-relaxed text-lg whitespace-pre-wrap">
                      {project.ml_models.split("\n\n").map((para: string, idx: number) => {
                        // Highlight YOLOv8, PyTorch, and Ultralytics
                        const highlighted = para
                          .replace(/YOLOv8/g, "<strong class='text-[var(--foreground)] font-semibold'>YOLOv8</strong>")
                          .replace(/PyTorch/g, "<strong class='text-[var(--foreground)] font-semibold'>PyTorch</strong>")
                          .replace(/Ultralytics/g, "<strong class='text-[var(--foreground)] font-semibold'>Ultralytics</strong>");
                        return (
                          <p key={idx} className="mb-4 last:mb-0" dangerouslySetInnerHTML={{ __html: highlighted }} />
                        );
                      })}
                    </div>
                  </div>
                </section>
              )}

              {/* Dataset & Preprocessing */}
              {project.dataset_info && (
                <section className="space-y-4">
                  <div className="flex items-center gap-3">
                    <Database className="h-6 w-6 text-[var(--primary)]" />
                    <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Dataset & Preprocessing</h2>
                  </div>
                  <div className="p-6 bg-[var(--secondary)]/30 rounded-xl border border-[var(--border)]/50">
                    <p className="text-[var(--muted-foreground)] leading-relaxed text-lg">
                      {project.dataset_info}
                    </p>
                  </div>
                </section>
              )}

              {/* Challenges */}
              {project.challenges && (
                <section className="space-y-4">
                  <div className="flex items-center gap-3">
                    <AlertTriangle className="h-6 w-6 text-[var(--primary)]" />
                    <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Challenges & Blockers</h2>
                  </div>
                  <div className="p-6 bg-[var(--secondary)]/30 rounded-xl border border-[var(--border)]/50">
                    <p className="text-[var(--muted-foreground)] leading-relaxed text-lg">
                      {project.challenges}
                    </p>
                  </div>
                </section>
              )}

              {/* Future Improvements */}
              {project.future_improvements && (
                <section className="space-y-4">
                  <div className="flex items-center gap-3">
                    <Lightbulb className="h-6 w-6 text-[var(--primary)]" />
                    <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Future Roadmap</h2>
                  </div>
                  <div className="p-6 bg-[var(--secondary)]/30 rounded-xl border border-[var(--border)]/50">
                    <p className="text-[var(--muted-foreground)] leading-relaxed text-lg">
                      {project.future_improvements}
                    </p>
                  </div>
                </section>
              )}

            </div>

            {/* Right Column: Sidebar (Metrics, Tech Stack, Applications) */}
            <div className="space-y-10">

              {/* Metrics & Performance */}
              {project.metrics && project.metrics.length > 0 && (
                <div className="p-6 bg-[var(--secondary)]/20 rounded-xl border border-[var(--border)]/50 space-y-6">
                  <div className="flex items-center gap-2 text-[var(--foreground)] font-bold text-xl border-b border-[var(--border)] pb-4">
                    <Activity className="h-5 w-5 text-[var(--primary)]" />
                    <h3>Results & Performance</h3>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    {project.metrics.map((metric: any) => (
                      <div key={metric.id} className="p-4 bg-[var(--secondary)]/50 rounded-lg border border-[var(--border)]/20 hover:scale-[1.02] transition-transform duration-200 text-center">
                        <div className="text-2xl font-extrabold text-[var(--foreground)] mb-1">{metric.value}</div>
                        <div className="text-xs text-[var(--muted-foreground)] font-medium tracking-wider uppercase">{metric.name}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Technology Stack */}
              {project.technologies && project.technologies.length > 0 && (
                <div className="p-6 bg-[var(--secondary)]/20 rounded-xl border border-[var(--border)]/50 space-y-6">
                  <div className="flex items-center gap-2 text-[var(--foreground)] font-bold text-xl border-b border-[var(--border)] pb-4">
                    <Layers className="h-5 w-5 text-[var(--primary)]" />
                    <h3>Technology Stack</h3>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {project.technologies.map((tech: any) => (
                      <Badge key={tech.id} variant="secondary" className="px-3 py-1 text-sm bg-[var(--secondary)] border border-[var(--border)] hover:bg-[var(--primary)]/10 hover:border-[var(--primary)]/30 transition-colors duration-200">
                        {tech.name}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {/* Applications & Use Cases */}
              {applications.length > 0 && (
                <div className="p-6 bg-[var(--secondary)]/20 rounded-xl border border-[var(--border)]/50 space-y-6">
                  <div className="flex items-center gap-2 text-[var(--foreground)] font-bold text-xl border-b border-[var(--border)] pb-4">
                    <Compass className="h-5 w-5 text-[var(--primary)]" />
                    <h3>Applications</h3>
                  </div>
                  <ul className="space-y-3">
                    {applications.map((app, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-sm text-[var(--muted-foreground)]">
                        <CheckCircle2 className="h-4 w-4 text-[var(--primary)] mt-0.5 shrink-0" />
                        <span>{app}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

            </div>

          </div>

          {/* Bottom Back Button */}
          <div className="border-t border-[var(--border)] pt-8 flex justify-center">
            <Button variant="outline" asChild className="px-8">
              <Link href="/projects"><ArrowLeft className="mr-2 h-4 w-4" /> Back to Projects</Link>
            </Button>
          </div>

        </div>
      </div>
    </div>
  );
}
