'use client';

import React, { useEffect, useState } from 'react';
import { getGithubRepositories } from '@/services/api';
import { GithubRepository } from '@/types/github';
import RepositoryCard from '@/components/github/RepositoryCard';

export default function GithubPage() {
  const [repositories, setRepositories] = useState<GithubRepository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [search, setSearch] = useState('');
  const [language, setLanguage] = useState('');
  const [sort, setSort] = useState('updated');

  const fetchRepositories = async () => {
    setLoading(true);
    setError(null);
    try {
      const repos = await getGithubRepositories({ search, language, sort });
      if (repos && Array.isArray(repos)) {
        setRepositories(repos);
      } else {
        setError('Failed to fetch repositories.');
      }
    } catch (err) {
      setError('An error occurred while fetching repositories.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRepositories();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sort]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchRepositories();
  };
  
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
        GitHub Repositories
      </h1>
      
      <form onSubmit={handleSearch} className="mb-8 flex flex-col md:flex-row gap-4">
        <input 
          type="text"
          placeholder="Search repositories..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-grow bg-gray-800 border border-gray-700 text-white rounded p-3 focus:outline-none focus:border-blue-500 transition-colors"
        />
        <select 
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="bg-gray-800 border border-gray-700 text-white rounded p-3 focus:outline-none focus:border-blue-500 transition-colors"
        >
          <option value="">All Languages</option>
          <option value="python">Python</option>
          <option value="typescript">TypeScript</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="html">HTML</option>
          <option value="go">Go</option>
          <option value="rust">Rust</option>
          <option value="c++">C++</option>
        </select>
        <select 
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="bg-gray-800 border border-gray-700 text-white rounded p-3 focus:outline-none focus:border-blue-500 transition-colors"
        >
          <option value="updated">Recently Updated</option>
          <option value="stars">Most Stars</option>
          <option value="alphabetical">Alphabetical</option>
        </select>
        <button type="submit" className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded transition-colors font-medium">
          Filter
        </button>
      </form>

      {loading ? (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : error ? (
        <div className="bg-red-900/50 border border-red-500 text-red-200 p-6 rounded-lg text-center shadow-lg">
          <p className="text-xl mb-2 font-bold">Oops! Something went wrong.</p>
          <p>{error}</p>
        </div>
      ) : repositories.length === 0 ? (
        <div className="text-center py-20 text-gray-400 bg-gray-800/50 rounded-lg border border-gray-700">
          <p className="text-xl">No repositories found matching your criteria.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {repositories.map(repo => (
            <RepositoryCard key={repo.id} repo={repo} />
          ))}
        </div>
      )}
    </div>
  );
}
