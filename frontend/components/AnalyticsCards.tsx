"use client";

import { useEffect, useState } from "react";
import { getAnalyticsSummary } from "@/services/api";

export function AnalyticsCards() {
    const [summary, setSummary] = useState<Record<string, number> | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getAnalyticsSummary().then(data => {
            setSummary(data);
            setLoading(false);
        });
    }, []);

    if (loading || !summary) return null;

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">
            <div className="bg-card p-6 rounded-xl border border-border text-center">
                <div className="text-3xl font-bold text-primary mb-2">{summary.total_project_views || 0}</div>
                <div className="text-sm text-[var(--muted-foreground)] uppercase tracking-wider">Project Views</div>
            </div>
            <div className="bg-card p-6 rounded-xl border border-border text-center">
                <div className="text-3xl font-bold text-primary mb-2">{summary.total_github_views || 0}</div>
                <div className="text-sm text-[var(--muted-foreground)] uppercase tracking-wider">GitHub Views</div>
            </div>
            <div className="bg-card p-6 rounded-xl border border-border text-center">
                <div className="text-3xl font-bold text-primary mb-2">{summary.total_contacts || 0}</div>
                <div className="text-sm text-[var(--muted-foreground)] uppercase tracking-wider">Messages Received</div>
            </div>
        </div>
    );
}
