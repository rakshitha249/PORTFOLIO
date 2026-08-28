import { ContactForm } from "@/components/ContactForm";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact | Portfolio",
  description: "Get in touch with me.",
};

export default function ContactPage() {
  return (
    <div className="container mx-auto max-w-4xl px-4 md:px-8 py-16">
      <div className="mb-12">
        <h1 className="text-4xl font-extrabold tracking-tight mb-4">Contact Me</h1>
        <p className="text-lg text-[var(--muted-foreground)]">
          Have a project in mind or want to discuss a potential opportunity? 
          Fill out the form below and I'll get back to you as soon as possible.
        </p>
      </div>
      
      <ContactForm />
    </div>
  );
}
