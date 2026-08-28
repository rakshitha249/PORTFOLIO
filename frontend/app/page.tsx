import { Button } from "@/components/ui/button";
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
