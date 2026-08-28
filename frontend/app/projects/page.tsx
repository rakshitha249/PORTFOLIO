import { getProjects } from "@/services/api";
import { ProjectCard } from "@/components/ProjectCard";
import { EmptyState } from "@/components/EmptyState";
import { ProjectsFilter } from "./ProjectsFilter";
import { AnalyticsTracker } from "@/components/AnalyticsTracker";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Projects | Portfolio",
  description: "Portfolio of software engineering and AI projects.",
};

export default async function ProjectsPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const resolvedParams = await searchParams;
  const search = typeof resolvedParams?.search === 'string' ? resolvedParams.search : undefined;
  const category = typeof resolvedParams?.category === 'string' ? resolvedParams.category : undefined;
  const sort = typeof resolvedParams?.sort === 'string' ? resolvedParams.sort : undefined;

  const projects = await getProjects(search, category, sort);

  return (
    <div className="container mx-auto max-w-6xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-4">Projects</h1>
      <p className="text-lg text-[var(--muted-foreground)] mb-8 max-w-2xl">
          A showcase of my recent work in AI, Data Science, and Full-Stack Engineering.
      </p>
      
      <AnalyticsTracker eventType="project_view" />
      <ProjectsFilter />
      
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
