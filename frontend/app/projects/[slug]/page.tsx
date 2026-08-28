import { getProjectBySlug, getProjects } from "@/services/api";
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

export default async function ProjectDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;
  const project = await getProjectBySlug(resolvedParams.slug);
  
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
