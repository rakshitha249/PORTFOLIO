import { getEducation } from "@/services/api";
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
