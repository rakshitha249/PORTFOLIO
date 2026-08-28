import { getProfile } from "@/services/api";
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
