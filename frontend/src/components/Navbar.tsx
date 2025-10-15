'use client';

import { useRouter } from 'next/navigation';
import { FileUp, Search, Users, LogOut } from 'lucide-react';
import { removeAuthToken } from '@/lib/auth';

export default function Navbar() {
  const router = useRouter();

  const handleLogout = () => {
    removeAuthToken();
    router.push('/');
  };

  return (
    <nav className="bg-black text-white border-b border-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-8">
            <button
              onClick={() => router.push('/dashboard')}
              className="text-xl font-bold hover:text-gray-300 transition-colors"
            >
              📄 Resume Screener
            </button>

            {/* Navigation Links */}
            <div className="hidden md:flex space-x-1">
              <button
                onClick={() => router.push('/dashboard')}
                className="px-4 py-2 rounded hover:bg-gray-800 transition-colors flex items-center space-x-2"
              >
                <Users size={18} />
                <span>Dashboard</span>
              </button>
              <button
                onClick={() => router.push('/upload')}
                className="px-4 py-2 rounded hover:bg-gray-800 transition-colors flex items-center space-x-2"
              >
                <FileUp size={18} />
                <span>Upload</span>
              </button>
              <button
                onClick={() => router.push('/resumes')}
                className="px-4 py-2 rounded hover:bg-gray-800 transition-colors flex items-center space-x-2"
              >
                <Search size={18} />
                <span>All Resumes</span>
              </button>
              <button
                onClick={() => router.push('/search')}
                className="px-4 py-2 rounded hover:bg-gray-800 transition-colors flex items-center space-x-2"
              >
                <Search size={18} />
                <span>Search</span>
              </button>
            </div>
          </div>

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="flex items-center space-x-2 px-4 py-2 rounded hover:bg-gray-800 transition-colors"
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
