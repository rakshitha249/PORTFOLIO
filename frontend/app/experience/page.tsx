import { getExperience } from "@/services/api";
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
