'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';
import { resumeApi } from '@/lib/api';
import type { Resume, JobDescription } from '@/types';
import { Search, Filter, TrendingUp } from 'lucide-react';

export default function SearchPage() {
  const router = useRouter();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [filteredResumes, setFilteredResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [requiredSkills, setRequiredSkills] = useState('');
  const [minExperience, setMinExperience] = useState('');
  const [scores, setScores] = useState<{ [key: string]: number }>({});

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
      setFilteredResumes(data);
    } catch (error) {
      console.error('Failed to load resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!jobDescription && !requiredSkills) {
      setFilteredResumes(resumes);
      setScores({});
      return;
    }

    setLoading(true);
    const newScores: { [key: string]: number } = {};

    try {
      const jobDesc: JobDescription = {
        title: jobTitle || 'Position',
        description: jobDescription,
        required_skills: requiredSkills ? requiredSkills.split(',').map(s => s.trim()) : [],
        preferred_skills: [],
        experience_years: minExperience ? parseInt(minExperience) : undefined,
      };

      // Calculate scores for all resumes
      for (const resume of resumes) {
        try {
          const result = await resumeApi.match(resume.id, jobDesc);
          newScores[resume.id] = result.match_score;
        } catch (error) {
          console.error(`Failed to match resume ${resume.id}:`, error);
        }
      }

      setScores(newScores);

      // Sort by score
      const sorted = [...resumes].sort((a, b) => {
        return (newScores[b.id] || 0) - (newScores[a.id] || 0);
      });

      setFilteredResumes(sorted);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-black mb-2">Search & Shortlist</h1>
          <p className="text-gray-600">Match resumes against job requirements</p>
        </div>

        {/* Search Criteria */}
        <div className="card p-6 mb-6">
          <div className="flex items-center mb-4">
            <Filter className="mr-2" size={20} />
            <h2 className="text-lg font-bold text-black">Job Requirements</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Software Engineer"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Minimum Experience (years)
              </label>
              <input
                type="number"
                value={minExperience}
                onChange={(e) => setMinExperience(e.target.value)}
                placeholder="e.g. 5"
                className="input-field"
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Description</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Describe the role, responsibilities, and requirements..."
              className="textarea-field"
              rows={4}
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Required Skills (comma separated)
            </label>
            <input
              type="text"
              value={requiredSkills}
              onChange={(e) => setRequiredSkills(e.target.value)}
              placeholder="Python, React, AWS, Docker"
              className="input-field"
            />
          </div>

          <button
            onClick={handleSearch}
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Search className="mr-2" size={18} />
                Calculate Match Scores
              </>
            )}
          </button>
        </div>

        {/* Results */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-black">
              Results ({filteredResumes.length} candidates)
            </h2>
            <TrendingUp size={20} />
          </div>

          {filteredResumes.length === 0 ? (
            <p className="text-center text-gray-600 py-8">No resumes available</p>
          ) : (
            <div className="space-y-3">
              {filteredResumes.map((resume) => (
                <div
                  key={resume.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => router.push(`/resumes/${resume.id}`)}
                >
                  <div className="flex-1">
                    <h3 className="font-bold text-black">{resume.name}</h3>
                    <p className="text-sm text-gray-600">{resume.contact?.email}</p>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {resume.skills.slice(0, 5).map((skill, idx) => (
                        <span key={idx} className="text-xs badge">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {scores[resume.id] !== undefined && (
                    <div className={`ml-4 px-4 py-2 rounded border font-bold ${getScoreColor(scores[resume.id])}`}>
                      {scores[resume.id].toFixed(1)}%
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
