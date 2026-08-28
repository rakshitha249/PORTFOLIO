import * as React from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { ExternalLink, Code } from "lucide-react";

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
                    <Code className="h-4 w-4" /> Code
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
