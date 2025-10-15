'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';
import { resumeApi } from '@/lib/api';
import React from 'react';
import type { Resume } from '@/types';
import { Search, Eye, Trash2, Download } from 'lucide-react';

export default function ResumesPage() {
  const router = useRouter();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [skillsFilter, setSkillsFilter] = useState('');

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/');
      return;
    }
    loadResumes();
  }, [router]);

  const loadResumes = async () => {
    try {
      const data = await resumeApi.list({ limit: 100 });
      setResumes(data);
    } catch (error) {
      console.error('Failed to load resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await resumeApi.list({
        search: searchTerm || undefined,
        skills: skillsFilter || undefined,
        limit: 100,
      });
      setResumes(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this resume?')) {
      try {
        await resumeApi.delete(id);
        setResumes(resumes.filter(r => r.id !== id));
      } catch (error) {
        console.error('Delete failed:', error);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-black mb-2">All Resumes</h1>
          <p className="text-gray-600">Browse and manage uploaded resumes</p>
        </div>

        {/* Search Filters */}
        <div className="card p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name, summary..."
              className="input-field"
            />
            <input
              type="text"
              value={skillsFilter}
              onChange={(e) => setSkillsFilter(e.target.value)}
              placeholder="Filter by skills (comma separated)"
              className="input-field"
            />
            <button onClick={handleSearch} className="btn-primary flex items-center justify-center">
              <Search className="mr-2" size={18} />
              Search
            </button>
          </div>
        </div>

        {/* Resumes List */}
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin" />
          </div>
        ) : resumes.length === 0 ? (
          <div className="card p-12 text-center">
            <p className="text-gray-600 text-lg">No resumes found. Upload your first resume!</p>
            <button onClick={() => router.push('/upload')} className="btn-primary mt-4">
              Upload Resume
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {resumes.map((resume) => (
              <div key={resume.id} className="card p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-black mb-2">{resume.name}</h3>
                    {resume.contact?.email && (
                      <p className="text-sm text-gray-600 mb-2">{resume.contact.email}</p>
                    )}
                    <div className="flex flex-wrap gap-2 mb-3">
                      {resume.skills.slice(0, 6).map((skill, idx) => (
                        <span key={idx} className="badge">
                          {skill}
                        </span>
                      ))}
                      {resume.skills.length > 6 && (
                        <span className="badge">+{resume.skills.length - 6} more</span>
                      )}
                    </div>
                    <p className="text-sm text-gray-500">
                      {resume.experiences.length} experience(s) • {resume.education.length} education(s)
                    </p>
                  </div>
                  
                  <div className="flex space-x-2 ml-4">
                    <button
                      onClick={() => router.push(`/resumes/${resume.id}`)}
                      className="p-2 hover:bg-gray-100 rounded transition-colors"
                      title="View Details"
                    >
                      <Eye size={20} />
                    </button>
                    <button
                      onClick={() => handleDelete(resume.id)}
                      className="p-2 hover:bg-red-50 text-red-600 rounded transition-colors"
                      title="Delete"
                    >
                      <Trash2 size={20} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
