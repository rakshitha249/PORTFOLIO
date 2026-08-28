"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export function ProjectsFilter() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [search, setSearch] = useState(searchParams.get("search") || "");
  const [category, setCategory] = useState(searchParams.get("category") || "All");
  const [sort, setSort] = useState(searchParams.get("sort") || "-created_at");

  const updateFilters = (newSearch: string, newCategory: string, newSort: string) => {
    const params = new URLSearchParams();
    if (newSearch) params.set("search", newSearch);
    if (newCategory !== "All") params.set("category", newCategory);
    if (newSort) params.set("sort", newSort);
    router.push(`/projects?${params.toString()}`);
  };

  return (
    <div className="flex flex-col md:flex-row gap-4 mb-8 bg-black/20 p-4 rounded-lg border border-white/5">
      <input
        type="text"
        placeholder="Search projects..."
        className="flex-1 bg-black/50 border border-white/10 rounded-md px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary"
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
          // Optional: debounce this in a real app
        }}
        onKeyDown={(e) => {
            if (e.key === 'Enter') {
                updateFilters(search, category, sort);
            }
        }}
      />
      <div className="flex gap-4">
          <select
            className="bg-black/50 border border-white/10 rounded-md px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary appearance-none min-w-[150px]"
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              updateFilters(search, e.target.value, sort);
            }}
          >
            <option value="All">All Categories</option>
            <option value="AI">AI / ML</option>
            <option value="Web">Web Dev</option>
            <option value="Data">Data Science</option>
          </select>
          <select
            className="bg-black/50 border border-white/10 rounded-md px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary appearance-none min-w-[150px]"
            value={sort}
            onChange={(e) => {
              setSort(e.target.value);
              updateFilters(search, category, e.target.value);
            }}
          >
            <option value="-created_at">Newest First</option>
            <option value="created_at">Oldest First</option>
            <option value="title">Alphabetical (A-Z)</option>
            <option value="-title">Alphabetical (Z-A)</option>
          </select>
          <button 
             onClick={() => updateFilters(search, category, sort)}
             className="bg-primary/20 hover:bg-primary/40 border border-primary/50 text-primary-foreground px-4 py-2 rounded-md transition-colors"
          >
              Search
          </button>
      </div>
    </div>
  );
}
