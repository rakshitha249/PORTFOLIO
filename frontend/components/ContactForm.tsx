"use client";

import { useState } from "react";
import { submitContact } from "@/services/api";

export function ContactForm() {
  const [formData, setFormData] = useState({ name: "", email: "", subject: "", message: "", website: "" });
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");
    
    try {
      await submitContact(formData);
      setStatus("success");
      setFormData({ name: "", email: "", subject: "", message: "", website: "" });
    } catch (err) {
      setStatus("error");
      setErrorMsg(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    }
  };

  return (
    <div className="bg-card p-8 rounded-xl border border-border">
      {status === "success" ? (
        <div className="text-center py-12">
          <div className="text-4xl mb-4">✅</div>
          <h3 className="text-xl font-bold mb-2">Message Sent</h3>
          <p className="text-[var(--muted-foreground)]">Thank you. Your message has been received.</p>
          <button 
             onClick={() => setStatus("idle")}
             className="mt-6 px-4 py-2 border border-border rounded-md hover:bg-muted"
          >
             Send another message
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Honeypot field - visually hidden but accessible to bots */}
          <div className="hidden">
             <label htmlFor="website">Website</label>
             <input type="text" id="website" name="website" value={formData.website} onChange={e => setFormData({...formData, website: e.target.value})} tabIndex={-1} autoComplete="off" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label htmlFor="name" className="text-sm font-medium">Name</label>
                <input 
                  type="text" 
                  id="name" 
                  required
                  className="w-full bg-background border border-input rounded-md px-4 py-2 text-white"
                  value={formData.name}
                  onChange={e => setFormData({...formData, name: e.target.value})}
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">Email</label>
                <input 
                  type="email" 
                  id="email" 
                  required
                  className="w-full bg-background border border-input rounded-md px-4 py-2 text-white"
                  value={formData.email}
                  onChange={e => setFormData({...formData, email: e.target.value})}
                />
              </div>
          </div>
          
          <div className="space-y-2">
            <label htmlFor="subject" className="text-sm font-medium">Subject</label>
            <input 
              type="text" 
              id="subject" 
              required
              className="w-full bg-background border border-input rounded-md px-4 py-2 text-white"
              value={formData.subject}
              onChange={e => setFormData({...formData, subject: e.target.value})}
            />
          </div>
          
          <div className="space-y-2">
            <label htmlFor="message" className="text-sm font-medium">Message</label>
            <textarea 
              id="message" 
              required
              rows={5}
              className="w-full bg-background border border-input rounded-md px-4 py-2 resize-y text-white"
              value={formData.message}
              onChange={e => setFormData({...formData, message: e.target.value})}
            ></textarea>
          </div>
          
          {status === "error" && (
              <div className="text-red-400 text-sm bg-red-400/10 p-3 rounded-md">
                  {errorMsg}
              </div>
          )}
          
          <button 
            type="submit" 
            disabled={status === "loading"}
            className="w-full bg-primary text-primary-foreground font-medium py-3 rounded-md hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {status === "loading" ? "Sending..." : "Send Message"}
          </button>
        </form>
      )}
    </div>
  );
}
