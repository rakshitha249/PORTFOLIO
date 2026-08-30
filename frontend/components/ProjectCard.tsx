import * as React from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { ExternalLink, Code, ArrowRight } from "lucide-react";
import Link from "next/link";

export function ProjectCard({ project }: { project: any }) {
  return (
    <Card className="flex flex-col h-full overflow-hidden transition-all hover:shadow-md hover:border-[var(--primary)]/30 group">
      <div className="h-48 bg-[var(--muted)] flex items-center justify-center border-b border-[var(--border)] overflow-hidden relative">
        {project.project_image ? (
          <Link href={`/projects/${project.slug}`} className="w-full h-full">
            <img
              src={project.project_image}
              alt={project.title}
              className="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-300"
            />
          </Link>
        ) : (
          <Link href={`/projects/${project.slug}`} className="w-full h-full flex items-center justify-center hover:bg-[var(--secondary)] transition-colors">
            <div className="font-mono text-[var(--muted-foreground)] text-4xl opacity-20">No Image</div>
          </Link>
        )}
      </div>
      <CardHeader>
        <div className="flex justify-between items-start gap-2">
          <CardTitle className="text-xl group-hover:text-[var(--primary)] transition-colors">
            <Link href={`/projects/${project.slug}`}>{project.title}</Link>
          </CardTitle>
          {project.category && <Badge variant="secondary" className="shrink-0">{project.category}</Badge>}
        </div>
      </CardHeader>
      <CardContent className="flex-1">
        <p className="text-sm text-[var(--muted-foreground)] mb-4 line-clamp-3">{project.short_description}</p>
        <div className="flex flex-wrap gap-2">
          {project.technologies?.map((tech: any) => (
            <Badge key={tech.id} variant="outline" className="text-[10px] py-0">{tech.name}</Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="gap-2">
        <Button variant="ghost" size="sm" className="flex-1 gap-1 text-xs hover:bg-[var(--primary)]/10 hover:text-[var(--primary)]" asChild>
          <Link href={`/projects/${project.slug}`}>
            Details <ArrowRight className="h-3 w-3" />
          </Link>
        </Button>
        {project.github_url && (
          <Button variant="outline" size="sm" className="flex-1 gap-1 text-xs" asChild>
            <a href={project.github_url} target="_blank" rel="noopener noreferrer">
              <Code className="h-3.5 w-3.5" /> Code
            </a>
          </Button>
        )}
        {project.live_demo_url && (
          <Button variant="default" size="sm" className="flex-1 gap-1 text-xs" asChild>
            <a href={project.live_demo_url} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-3.5 w-3.5" /> Demo
            </a>
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
