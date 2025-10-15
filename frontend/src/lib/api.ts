/**
 * API client for communicating with the backend.
 * Handles authentication, error handling, and request/response formatting.
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import { getAuthToken, removeAuthToken } from './auth';
import type {
  LoginCredentials,
  RegisterData,
  AuthToken,
  Resume,
  UploadResponse,
  JobDescription,
  MatchDetails,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      removeAuthToken();
      if (typeof window !== 'undefined') {
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthToken> => {
    const response = await apiClient.post<AuthToken>('/api/auth/login', credentials);
    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthToken> => {
    const response = await apiClient.post<AuthToken>('/api/auth/register', data);
    return response.data;
  },
};

// Resume API
export const resumeApi = {
  list: async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    skills?: string;
  }): Promise<Resume[]> => {
    const response = await apiClient.get<Resume[]>('/api/resumes', { params });
    return response.data;
  },

  get: async (id: string): Promise<Resume> => {
    const response = await apiClient.get<Resume>(`/api/resumes/${id}`);
    return response.data;
  },

  update: async (id: string, data: Resume): Promise<Resume> => {
    const response = await apiClient.put<Resume>(`/api/resumes/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/resumes/${id}`);
  },

  match: async (resumeId: string, jobDescription: JobDescription): Promise<{ match_score: number; details: MatchDetails }> => {
    const response = await apiClient.post('/api/resumes/match', {
      resume_id: resumeId,
      job_description: jobDescription,
    });
    return response.data;
  },

  download: async (id: string): Promise<Blob> => {
    const response = await apiClient.get(`/api/resumes/${id}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Upload API
export const uploadApi = {
  uploadResume: async (
    file: File,
    jobDescription?: string,
    requiredSkills?: string
  ): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (jobDescription) {
      formData.append('job_description', jobDescription);
    }
    if (requiredSkills) {
      formData.append('required_skills', requiredSkills);
    }

    const response = await apiClient.post<UploadResponse>('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

// Settings API
export const settingsApi = {
  getProfile: async () => {
    const response = await apiClient.get('/api/settings/profile');
    return response.data;
  },

  updateProfile: async (data: { full_name?: string; company_name?: string }) => {
    const response = await apiClient.put('/api/settings/profile', data);
    return response.data;
  },

  updatePreferences: async (data: {
    email_notifications?: boolean;
    auto_process_resumes?: boolean;
    match_score_threshold?: number;
    company_name?: string;
  }) => {
    const response = await apiClient.put('/api/settings/preferences', data);
    return response.data;
  },

  changePassword: async (data: { current_password: string; new_password: string }) => {
    const response = await apiClient.post('/api/settings/change-password', data);
    return response.data;
  },

  exportData: async () => {
    const response = await apiClient.post('/api/settings/export-data');
    return response.data;
  },

  deleteAllData: async () => {
    const response = await apiClient.delete('/api/settings/delete-all-data');
    return response.data;
  },
};

export default apiClient;
