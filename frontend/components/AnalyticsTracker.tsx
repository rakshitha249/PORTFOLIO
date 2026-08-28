"use client";

import { useEffect, useRef } from "react";
import { trackEvent } from "@/services/api";

interface AnalyticsTrackerProps {
    eventType: string;
    projectSlug?: string;
}

export function AnalyticsTracker({ eventType, projectSlug }: AnalyticsTrackerProps) {
    const tracked = useRef(false);
    
    useEffect(() => {
        if (!tracked.current) {
            tracked.current = true;
            trackEvent(eventType, projectSlug, window.location.pathname);
        }
    }, [eventType, projectSlug]);
    
    return null;
}
