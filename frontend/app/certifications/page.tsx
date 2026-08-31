import { getCertificates } from "@/services/api";
import { EmptyState } from "@/components/EmptyState";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Metadata } from "next";
import { Award, ExternalLink } from "lucide-react";

export const metadata: Metadata = {
  title: "Certifications | Portfolio",
  description: "Professional certifications and awards.",
};

export default async function CertificationsPage() {
  const certificates = await getCertificates();

  return (
    <div className="container mx-auto max-w-5xl px-4 md:px-8 py-16">
      <h1 className="text-4xl font-extrabold tracking-tight mb-12">Certifications</h1>
      {certificates.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {certificates.map((cert: any) => (
                <Card key={cert.id} className="hover:shadow-md transition-shadow">
                    <CardHeader className="pb-3">
                        <div className="flex justify-between items-start">
                            <CardTitle className="text-xl leading-tight">{cert.name}</CardTitle>
                            <Award className="text-[var(--primary)] h-6 w-6 shrink-0 ml-4" />
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="font-medium text-[var(--muted-foreground)] mb-2">{cert.issuer}</div>
                        <Badge variant="secondary" className="mb-4">{cert.issue_date}</Badge>
                        {cert.description && <p className="text-sm text-[var(--muted-foreground)] mb-4">{cert.description}</p>}
                        {cert.credential_url && (
                            <a href={cert.credential_url} target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-[var(--primary)] hover:underline inline-flex items-center">
                                View Certificate <ExternalLink className="ml-1 h-3 w-3" />
                            </a>
                        )}
                    </CardContent>
                </Card>
            ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
