import { Button } from "@/components/ui/button";
import type { Metadata } from "next";
import { FileDown, ExternalLink } from "lucide-react";

export const metadata: Metadata = {
  title: "Resume | Portfolio",
  description: "Professional resume.",
};

export default function ResumePage() {
  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16 flex flex-col items-center">
      <h1 className="text-4xl font-extrabold tracking-tight mb-8">Resume</h1>
      
      <div className="w-full flex flex-col items-center">
          <div className="flex flex-row gap-4 mb-8">
              <Button asChild size="lg">
                  <a href="/resume.pdf" target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="mr-2 h-4 w-4" /> View Resume
                  </a>
              </Button>
              <Button asChild size="lg" variant="outline">
                  <a href="/resume.pdf" download="Rakshitha_S_S_Resume.pdf">
                      <FileDown className="mr-2 h-4 w-4" /> Download Resume
                  </a>
              </Button>
          </div>
          
          <div className="w-full h-[80vh] min-h-[600px] border rounded-lg overflow-hidden shadow-sm">
              <iframe 
                  src="/resume.pdf" 
                  className="w-full h-full"
                  title="Resume PDF"
              />
          </div>
      </div>
    </div>
  );
}
