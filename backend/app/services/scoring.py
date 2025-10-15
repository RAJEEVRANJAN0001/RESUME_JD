"""
Scoring algorithm for matching resumes against job descriptions.
Combines skills overlap, experience matching, education matching, and semantic similarity.
"""
from app.models import Resume, JobDescription
from typing import Dict, List, Set
import re


class ResumeScorer:
    """Calculate match scores between resumes and job descriptions."""
    
    def calculate_match_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> Dict:
        """
        Calculate comprehensive match score (0-100).
        
        Components:
        - Skills overlap: 40%
        - Experience match: 30%
        - Education match: 20%
        - Semantic similarity: 10%
        """
        # Calculate individual scores
        skills_score = self._calculate_skills_score(resume, job_description)
        experience_score = self._calculate_experience_score(resume, job_description)
        education_score = self._calculate_education_score(resume, job_description)
        semantic_score = self._calculate_semantic_score(resume, job_description)
        
        # Weighted total
        total_score = (
            skills_score * 0.4 +
            experience_score * 0.3 +
            education_score * 0.2 +
            semantic_score * 0.1
        )
        
        return {
            "total_score": round(total_score, 2),
            "breakdown": {
                "skills_score": round(skills_score, 2),
                "experience_score": round(experience_score, 2),
                "education_score": round(education_score, 2),
                "semantic_score": round(semantic_score, 2)
            },
            "matched_skills": self._get_matched_skills(resume, job_description),
            "missing_skills": self._get_missing_skills(resume, job_description),
            "experience_years": self._calculate_total_experience_years(resume)
        }
    
    def _calculate_skills_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> float:
        """Calculate skills overlap score using Jaccard similarity."""
        resume_skills = set(skill.lower() for skill in resume.skills)
        required_skills = set(skill.lower() for skill in job_description.required_skills)
        preferred_skills = set(skill.lower() for skill in job_description.preferred_skills)
        
        # All job skills
        all_job_skills = required_skills.union(preferred_skills)
        
        if not all_job_skills:
            return 50.0  # No skills specified, neutral score
        
        # Jaccard similarity
        intersection = len(resume_skills.intersection(all_job_skills))
        union = len(resume_skills.union(all_job_skills))
        
        if union == 0:
            return 0.0
        
        jaccard = intersection / union
        
        # Boost score if required skills are met
        required_match = len(resume_skills.intersection(required_skills))
        required_ratio = required_match / len(required_skills) if required_skills else 1.0
        
        # Combined score (60% Jaccard, 40% required skills)
        score = (jaccard * 0.6 + required_ratio * 0.4) * 100
        
        return min(score, 100.0)
    
    def _calculate_experience_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> float:
        """Calculate experience match score."""
        total_years = self._calculate_total_experience_years(resume)
        required_years = job_description.experience_years or 0
        
        if required_years == 0:
            return 80.0  # No requirement, good score
        
        if total_years >= required_years:
            # Has enough experience
            excess_years = total_years - required_years
            score = 100.0 - (excess_years * 2)  # Slight penalty for being overqualified
            return max(score, 85.0)
        else:
            # Under-qualified
            ratio = total_years / required_years
            score = ratio * 70  # Max 70% if under-qualified
            return score
    
    def _calculate_education_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> float:
        """Calculate education match score."""
        if not resume.education:
            return 40.0  # No education listed
        
        # Simple heuristic: check for degree keywords
        education_text = " ".join([
            f"{edu.degree} {edu.institution}".lower()
            for edu in resume.education
        ])
        
        # Degree level scoring
        score = 50.0  # Base score
        
        if any(keyword in education_text for keyword in ['phd', 'doctorate']):
            score = 100.0
        elif any(keyword in education_text for keyword in ['master', 'mba', 'ms', 'ma']):
            score = 90.0
        elif any(keyword in education_text for keyword in ['bachelor', 'bs', 'ba', 'bsc']):
            score = 80.0
        elif any(keyword in education_text for keyword in ['associate', 'diploma']):
            score = 70.0
        
        return score
    
    def _calculate_semantic_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> float:
        """
        Calculate semantic similarity score.
        Simple keyword-based approach (can be enhanced with embeddings).
        """
        # Combine resume text
        resume_text = " ".join([
            resume.name,
            resume.summary or "",
            " ".join(resume.skills),
            " ".join([exp.title + " " + exp.company for exp in resume.experiences])
        ]).lower()
        
        # Job description text
        job_text = f"{job_description.title} {job_description.description}".lower()
        
        # Extract keywords from job description (simple tokenization)
        job_keywords = set(re.findall(r'\b\w{4,}\b', job_text))
        resume_keywords = set(re.findall(r'\b\w{4,}\b', resume_text))
        
        # Remove common words
        common_words = {
            'with', 'that', 'this', 'from', 'have', 'will', 'your',
            'about', 'other', 'which', 'their', 'there', 'would', 'could'
        }
        job_keywords -= common_words
        resume_keywords -= common_words
        
        if not job_keywords:
            return 50.0
        
        # Calculate overlap
        intersection = len(resume_keywords.intersection(job_keywords))
        score = (intersection / len(job_keywords)) * 100
        
        return min(score, 100.0)
    
    def _calculate_total_experience_years(self, resume: Resume) -> float:
        """Calculate total years of experience."""
        total_years = 0.0
        
        for exp in resume.experiences:
            try:
                # Parse start date
                start_year = int(exp.start_date.split('-')[0])
                
                # Parse end date or use current year
                if exp.end_date:
                    end_year = int(exp.end_date.split('-')[0])
                else:
                    from datetime import datetime
                    end_year = datetime.now().year
                
                years = end_year - start_year
                total_years += max(years, 0)
            except:
                continue
        
        return total_years
    
    def _get_matched_skills(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> List[str]:
        """Get list of matched skills."""
        resume_skills = set(skill.lower() for skill in resume.skills)
        required_skills = set(skill.lower() for skill in job_description.required_skills)
        preferred_skills = set(skill.lower() for skill in job_description.preferred_skills)
        
        all_job_skills = required_skills.union(preferred_skills)
        matched = resume_skills.intersection(all_job_skills)
        
        return sorted(list(matched))
    
    def _get_missing_skills(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> List[str]:
        """Get list of missing required skills."""
        resume_skills = set(skill.lower() for skill in resume.skills)
        required_skills = set(skill.lower() for skill in job_description.required_skills)
        
        missing = required_skills - resume_skills
        
        return sorted(list(missing))


# Global scorer instance
resume_scorer = ResumeScorer()
