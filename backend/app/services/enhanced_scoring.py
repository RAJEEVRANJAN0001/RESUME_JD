"""
Enhanced scoring algorithm using Gemini API for accurate resume-to-JD matching.
"""
from app.models import Resume, JobDescription
from typing import Dict, List
import google.generativeai as genai
import os
import json
import re
from datetime import datetime

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


class EnhancedResumeScorer:
    """Calculate match scores using AI-powered analysis."""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
    
    def calculate_match_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> Dict:
        """
        Calculate comprehensive match score using Gemini API.
        Falls back to rule-based scoring if API fails.
        """
        try:
            # Try AI-powered scoring first
            return self._calculate_ai_score(resume, job_description)
        except Exception as e:
            print(f"AI scoring failed, using fallback: {e}")
            # Fallback to rule-based scoring
            return self._calculate_fallback_score(resume, job_description)
    
    def _calculate_ai_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> Dict:
        """Use Gemini API to calculate match score."""
        
        # Prepare resume data
        resume_data = {
            "name": resume.name,
            "email": resume.contact.email if resume.contact else None,
            "summary": resume.summary or "",
            "skills": resume.skills,
            "experiences": [
                {
                    "title": exp.title,
                    "company": exp.company,
                    "duration": f"{exp.start_date} to {exp.end_date or 'Present'}",
                    "description": exp.description
                }
                for exp in resume.experiences
            ],
            "education": [
                {
                    "degree": edu.degree,
                    "institution": edu.institution,
                    "year": edu.year
                }
                for edu in resume.education
            ],
            "certifications": resume.certifications
        }
        
        # Prepare job description data
        jd_data = {
            "title": job_description.title,
            "description": job_description.description,
            "required_skills": job_description.required_skills,
            "preferred_skills": job_description.preferred_skills,
            "experience_years": job_description.experience_years or 0
        }
        
        # Create prompt for Gemini
        prompt = f"""You are an expert HR professional analyzing resume-job fit. Analyze this resume against the job description and provide accurate matching scores.

**RESUME:**
```json
{json.dumps(resume_data, indent=2)}
```

**JOB DESCRIPTION:**
```json
{json.dumps(jd_data, indent=2)}
```

**INSTRUCTIONS:**
Analyze the resume against the job description and provide scores for:

1. **Skills Match (0-100)**: 
   - How well do the candidate's skills align with required and preferred skills?
   - Consider both technical and soft skills
   - Give 0 if no relevant skills match

2. **Experience Match (0-100)**:
   - CRITICAL: If the resume has NO work experience listed, score MUST be 0
   - If experience exists, evaluate:
     * Years of experience vs requirement
     * Relevance of past roles to the job
     * Progression and growth
   - Don't give high scores if experience is missing or irrelevant

3. **Education Match (0-100)**:
   - How well does education align with job requirements?
   - Consider degree level, field of study, institution
   - Give reasonable score even if education is not explicitly required

4. **Semantic Match (0-100)**:
   - Overall contextual fit based on job description keywords
   - Industry alignment, domain knowledge indicators
   - Cultural and role fit signals

**RESPONSE FORMAT (JSON only, no other text):**
```json
{{
  "skills_score": <number 0-100>,
  "experience_score": <number 0-100>,
  "education_score": <number 0-100>,
  "semantic_score": <number 0-100>,
  "reasoning": {{
    "skills": "<brief explanation>",
    "experience": "<brief explanation - mention if NO experience found>",
    "education": "<brief explanation>",
    "semantic": "<brief explanation>"
  }},
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "gaps": ["<gap 1>", "<gap 2>", ...],
  "matched_skills": ["<skill 1>", "<skill 2>", ...],
  "missing_skills": ["<skill 1>", "<skill 2>", ...]
}}
```

**IMPORTANT RULES:**
- Be realistic and accurate
- Experience score MUST be 0 if no work experience is listed
- Don't be overly generous - match scores should reflect actual fit
- Provide actionable reasoning
- Focus on job-relevance, not just presence of information
"""
        
        # Call Gemini API
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,  # Low temperature for consistent scoring
                max_output_tokens=2048,
            )
        )
        
        # Parse response
        response_text = response.text.strip()
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        elif "```" in response_text:
            json_match = re.search(r'```\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        
        ai_result = json.loads(response_text)
        
        # Calculate weighted total score
        skills_score = float(ai_result.get("skills_score", 0))
        experience_score = float(ai_result.get("experience_score", 0))
        education_score = float(ai_result.get("education_score", 0))
        semantic_score = float(ai_result.get("semantic_score", 0))
        
        # Weighted total (40% skills, 30% experience, 20% education, 10% semantic)
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
            "matched_skills": ai_result.get("matched_skills", []),
            "missing_skills": ai_result.get("missing_skills", []),
            "strengths": ai_result.get("strengths", []),
            "gaps": ai_result.get("gaps", []),
            "reasoning": ai_result.get("reasoning", {}),
            "experience_years": self._calculate_total_experience_years(resume),
            "ai_powered": True
        }
    
    def _calculate_fallback_score(
        self,
        resume: Resume,
        job_description: JobDescription
    ) -> Dict:
        """Fallback rule-based scoring if AI fails."""
        
        skills_score = self._calculate_skills_score(resume, job_description)
        experience_score = self._calculate_experience_score(resume, job_description)
        education_score = self._calculate_education_score(resume, job_description)
        semantic_score = self._calculate_semantic_score(resume, job_description)
        
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
            "experience_years": self._calculate_total_experience_years(resume),
            "ai_powered": False
        }
    
    def _calculate_skills_score(self, resume: Resume, job_description: JobDescription) -> float:
        """Calculate skills overlap score."""
        resume_skills = set(skill.lower().strip() for skill in resume.skills if skill)
        required_skills = set(skill.lower().strip() for skill in job_description.required_skills if skill)
        preferred_skills = set(skill.lower().strip() for skill in job_description.preferred_skills if skill)
        
        all_job_skills = required_skills.union(preferred_skills)
        
        if not all_job_skills:
            return 50.0
        
        if not resume_skills:
            return 0.0
        
        # Calculate matches
        required_matches = resume_skills.intersection(required_skills)
        preferred_matches = resume_skills.intersection(preferred_skills)
        
        # Scoring
        required_ratio = len(required_matches) / len(required_skills) if required_skills else 1.0
        preferred_ratio = len(preferred_matches) / len(preferred_skills) if preferred_skills else 0.5
        
        # Weight required skills more heavily
        score = (required_ratio * 0.7 + preferred_ratio * 0.3) * 100
        
        return min(score, 100.0)
    
    def _calculate_experience_score(self, resume: Resume, job_description: JobDescription) -> float:
        """Calculate experience match score - returns 0 if no experience."""
        
        # CRITICAL FIX: Return 0 if no experience
        if not resume.experiences or len(resume.experiences) == 0:
            return 0.0
        
        total_years = self._calculate_total_experience_years(resume)
        
        # If still 0 years after calculation, return 0
        if total_years == 0:
            return 0.0
        
        required_years = job_description.experience_years or 0
        
        if required_years == 0:
            # No specific requirement, but has experience
            return 70.0
        
        if total_years >= required_years:
            # Meets or exceeds requirement
            if total_years <= required_years * 1.5:
                return 100.0
            else:
                # Overqualified - slight penalty
                excess = total_years - required_years
                score = 100.0 - (excess * 1.5)
                return max(score, 85.0)
        else:
            # Under-qualified
            ratio = total_years / required_years
            score = ratio * 70
            return max(score, 10.0)  # Minimum score if has some experience
    
    def _calculate_education_score(self, resume: Resume, job_description: JobDescription) -> float:
        """Calculate education match score."""
        if not resume.education or len(resume.education) == 0:
            return 30.0
        
        education_text = " ".join([
            f"{edu.degree} {edu.institution} {edu.field_of_study or ''}".lower()
            for edu in resume.education
        ])
        
        score = 50.0
        
        if any(keyword in education_text for keyword in ['phd', 'doctorate', 'doctoral']):
            score = 100.0
        elif any(keyword in education_text for keyword in ['master', 'mba', 'msc', 'ma', 'ms']):
            score = 90.0
        elif any(keyword in education_text for keyword in ['bachelor', 'bsc', 'ba', 'bs', 'btech', 'be']):
            score = 80.0
        elif any(keyword in education_text for keyword in ['associate', 'diploma', 'certificate']):
            score = 70.0
        
        return score
    
    def _calculate_semantic_score(self, resume: Resume, job_description: JobDescription) -> float:
        """Calculate semantic similarity."""
        resume_text = " ".join([
            resume.name or "",
            resume.summary or "",
            " ".join(resume.skills),
            " ".join([exp.title + " " + exp.company + " " + (exp.description or "") for exp in resume.experiences])
        ]).lower()
        
        job_text = f"{job_description.title} {job_description.description}".lower()
        
        job_keywords = set(re.findall(r'\b\w{4,}\b', job_text))
        resume_keywords = set(re.findall(r'\b\w{4,}\b', resume_text))
        
        common_words = {
            'with', 'that', 'this', 'from', 'have', 'will', 'your', 'about',
            'other', 'which', 'their', 'there', 'would', 'could', 'should',
            'experience', 'work', 'working', 'years', 'knowledge'
        }
        job_keywords -= common_words
        resume_keywords -= common_words
        
        if not job_keywords:
            return 50.0
        
        intersection = len(resume_keywords.intersection(job_keywords))
        score = (intersection / len(job_keywords)) * 100
        
        return min(score, 100.0)
    
    def _calculate_total_experience_years(self, resume: Resume) -> float:
        """Calculate total years of experience."""
        if not resume.experiences:
            return 0.0
        
        total_years = 0.0
        current_year = datetime.now().year
        
        for exp in resume.experiences:
            try:
                # Parse start date
                if exp.start_date:
                    start_parts = exp.start_date.split('-')
                    start_year = int(start_parts[0])
                else:
                    continue
                
                # Parse end date or use current year
                if exp.end_date and exp.end_date.lower() not in ['present', 'current', '']:
                    end_parts = exp.end_date.split('-')
                    end_year = int(end_parts[0])
                else:
                    end_year = current_year
                
                years = max(end_year - start_year, 0)
                total_years += years
            except Exception as e:
                print(f"Error calculating experience years: {e}")
                continue
        
        return round(total_years, 1)
    
    def _get_matched_skills(self, resume: Resume, job_description: JobDescription) -> List[str]:
        """Get list of matched skills."""
        resume_skills = set(skill.lower().strip() for skill in resume.skills if skill)
        required_skills = set(skill.lower().strip() for skill in job_description.required_skills if skill)
        preferred_skills = set(skill.lower().strip() for skill in job_description.preferred_skills if skill)
        
        all_job_skills = required_skills.union(preferred_skills)
        matched = resume_skills.intersection(all_job_skills)
        
        return sorted(list(matched))
    
    def _get_missing_skills(self, resume: Resume, job_description: JobDescription) -> List[str]:
        """Get list of missing required skills."""
        resume_skills = set(skill.lower().strip() for skill in resume.skills if skill)
        required_skills = set(skill.lower().strip() for skill in job_description.required_skills if skill)
        
        missing = required_skills - resume_skills
        
        return sorted(list(missing))


# Global enhanced scorer instance
enhanced_resume_scorer = EnhancedResumeScorer()
