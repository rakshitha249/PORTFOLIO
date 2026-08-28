import { EmptyState } from "@/components/EmptyState";
import { Button } from "@/components/ui/button";
import type { Metadata } from "next";
import { FileDown } from "lucide-react";

export const metadata: Metadata = {
  title: "Resume | Portfolio",
  description: "Professional resume.",
};

export default function ResumePage() {
  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16 flex flex-col items-center">
      <h1 className="text-4xl font-extrabold tracking-tight mb-8">Resume</h1>
      
      <div className="w-full max-w-2xl">
          <EmptyState title="Resume Coming Soon" message="The resume document is currently being finalized and will be available for download shortly." />
          <div className="mt-8 flex justify-center">
              <Button disabled size="lg"><FileDown className="mr-2 h-4 w-4" /> Download Resume</Button>
          </div>
      </div>
    </div>
  );
}
