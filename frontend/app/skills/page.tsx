import { getSkills } from "@/services/api";
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
