// TypeScript type definitions for the application

export interface Contact {
  email?: string;
  phone?: string;
  linkedin?: string;
  website?: string;
}

export interface Experience {
  title: string;
  company: string;
  start_date: string;
  end_date?: string | null;
  location?: string;
  responsibilities: string[];
  bullet_impact_score?: number;
}

export interface Education {
  degree: string;
  institution: string;
  start_date?: string;
  end_date?: string | null;
  gpa?: number | null;
  honors?: string | null;
  location?: string | null;
}

export interface Certification {
  name: string;
  issuing_organization?: string | null;
  issue_date?: string | null;
  expiration_date?: string | null;
  credential_id?: string | null;
  credential_url?: string | null;
}

export interface Project {
  name: string;
  description?: string | null;
  technologies?: string[];
  start_date?: string | null;
  end_date?: string | null;
  url?: string | null;
}

export interface Resume {
  id: string;
  name: string;
  contact?: Contact;
  summary?: string;
  skills: string[];
  experiences: Experience[];
  education: Education[];
  certifications: (string | Certification)[]; // Support both old and new formats
  projects?: Project[];
  achievements?: string[];
  languages?: string[];
  awards?: string[];
  parsed_at: string;
  resume_hash: string;
  source?: string;
  file_id?: string;
}

export interface JobDescription {
  title: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_years?: number;
}

export interface MatchDetails {
  total_score: number;
  breakdown: {
    skills_score: number;
    experience_score: number;
    education_score: number;
    semantic_score: number;
  };
  matched_skills: string[];
  missing_skills: string[];
  experience_years: number;
}

export interface UploadResponse {
  message: string;
  resume_id: string;
  resume_data: Resume;
  match_score?: number;
  match_details?: MatchDetails;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  username?: string;
  full_name?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface User {
  email: string;
  full_name?: string;
}
