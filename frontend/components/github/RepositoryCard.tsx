import React from 'react';
import { GithubRepository } from '@/types/github';

export default function RepositoryCard({ repo }: { repo: GithubRepository }) {
  return (
    <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors border border-gray-700 flex flex-col h-full">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-bold text-blue-400">
          <a href={repo.html_url} target="_blank" rel="noopener noreferrer" className="hover:underline">
            {repo.name}
          </a>
        </h3>
        <span className="bg-gray-900 text-xs px-2 py-1 rounded text-gray-300 border border-gray-600 ml-2 whitespace-nowrap">
          {repo.language || 'Unknown'}
        </span>
      </div>
      <p className="text-gray-300 text-sm mb-4 line-clamp-2 flex-grow min-h-[40px]">
        {repo.description || 'No description provided.'}
      </p>
      
      {repo.topics && repo.topics.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {repo.topics.slice(0, 3).map(topic => (
            <span key={topic} className="bg-blue-900/30 text-blue-300 text-xs px-2 py-1 rounded-full">
              {topic}
            </span>
          ))}
          {repo.topics.length > 3 && (
            <span className="text-gray-500 text-xs py-1">+{repo.topics.length - 3}</span>
          )}
        </div>
      )}

      <div className="flex justify-between items-center text-sm text-gray-400 mt-auto pt-4 border-t border-gray-700">
        <div className="flex gap-4">
          <span className="flex items-center gap-1">
            ⭐ {repo.stargazers_count}
          </span>
          <span className="flex items-center gap-1">
            🍴 {repo.forks_count}
          </span>
        </div>
        <span>{new Date(repo.updated_at).toLocaleDateString()}</span>
      </div>
      <div className="mt-4 flex gap-2 w-full">
        <a 
          href={repo.html_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-1 bg-gray-700 hover:bg-gray-600 text-center py-2 rounded text-sm transition-colors text-white"
        >
          View Code
        </a>
        {repo.homepage && (
          <a 
            href={repo.homepage}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 bg-blue-600 hover:bg-blue-500 text-center py-2 rounded text-sm transition-colors text-white"
          >
            Live Demo
          </a>
        )}
      </div>
    </div>
  );
}
