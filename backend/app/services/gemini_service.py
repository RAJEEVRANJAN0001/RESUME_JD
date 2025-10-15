"""
Google Gemini LLM service for ENHANCED structured JSON extraction from resume text.
Includes improved prompts, retry logic, validation, and advanced fallback parsing.
"""
import google.generativeai as genai
from app.config import settings
from app.models import Resume
import json
import re
from typing import Optional, Dict, Any
from datetime import datetime
import hashlib


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Orchestrate Gemini API for resume parsing with enhanced accuracy."""
    
    def __init__(self):
        """Initialize Gemini model with optimal settings."""
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.generation_config = {
            "temperature": 0.05,  # Very low temperature for maximum determinism
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 8192,  # Increased for detailed resumes
        }
    
    def _create_prompt(self, resume_text: str, strict_mode: bool = False) -> str:
        """
        Create comprehensive structured prompt with detailed extraction rules.
        Strict mode adds additional constraints for retry attempts.
        """
        strict_instruction = ""
        if strict_mode:
            strict_instruction = """
🚨 CRITICAL - Previous response was INVALID. Follow these rules EXACTLY:
- Output ONLY valid JSON, absolutely NO markdown, NO code blocks, NO explanations
- All dates MUST be in YYYY-MM-DD or YYYY-MM format
- Every array MUST be properly closed with ]
- Every object MUST be properly closed with }}
- Email MUST be valid format with @
- Extract EVERY piece of information from the resume
- Do NOT skip ANY sections
"""
        
        prompt = f"""You are an EXPERT resume parser with 99%+ accuracy. Your task is to extract ALL structured information from the resume text below.

OUTPUT SCHEMA (output ONLY valid JSON):
{{
  "name": "string (extract full name from header/contact section)",
  "contact": {{
    "email": "string (extract email - look for @domain pattern)",
    "phone": "string (extract phone number - any format)",
    "linkedin": "string (extract LinkedIn URL or username)",
    "website": "string (extract GitHub, portfolio, or personal website)"
  }},
  "summary": "string (professional summary/objective - capture complete text)",
  "skills": ["skill1", "skill2", ... (extract ALL skills, technologies, languages, tools, frameworks - be comprehensive)],
  "experiences": [
    {{
      "title": "string (exact job title/position)",
      "company": "string (exact company/organization name)",
      "start_date": "string (YYYY-MM or YYYY-MM-DD)",
      "end_date": "string or null (null if 'Present', 'Current', or ongoing)",
      "location": "string (city, state/country)",
      "responsibilities": ["bullet1", "bullet2", ... (extract ALL bullets and achievements)],
      "bullet_impact_score": float (0.0-1.0: high=0.8-1.0 with metrics, medium=0.5-0.7, low=0.0-0.4)
    }}
  ],
  "education": [
    {{
      "degree": "string (full degree + major: 'Bachelor of Science in Computer Science')",
      "institution": "string (full school name)",
      "field_of_study": "string (major/specialization: 'Computer Science', 'Mechanical Engineering')",
      "start_date": "YYYY (year only)",
      "end_date": "YYYY (year only, or null if ongoing)",
      "gpa": "string (if mentioned: '3.5/4.0', '3.5', '3.5 GPA')",
      "location": "string (if available: 'Boston, MA', 'Cambridge, UK')",
      "honors": "string (if mentioned: 'Summa Cum Laude', 'Dean's List', 'With Honors')",
      "year": "string (graduation year for compatibility)"
    }}
  ],
  "projects": [
    {{
      "name": "string (project name)",
      "description": "string (project description)",
      "technologies": ["tech1", "tech2"],
      "url": "string (if available)",
      "start_date": "YYYY-MM (optional)",
      "end_date": "YYYY-MM (optional)"
    }}
  ],
  "certifications": [
    {{
      "name": "string (certification name: 'AWS Solutions Architect', 'PMP')",
      "issuing_organization": "string (issuer: 'Amazon Web Services', 'PMI')",
      "issue_date": "YYYY-MM or YYYY (when obtained)",
      "expiry_date": "YYYY-MM or YYYY (if applicable, null otherwise)",
      "credential_id": "string (if mentioned)",
      "credential_url": "string (verification URL if available)"
    }}
  ],
  "achievements": ["achievement1", "achievement2", ... (notable accomplishments)],
  "languages": ["language1", "language2", ... (spoken languages with proficiency if mentioned)],
  "awards": ["award1", "award2", ... (awards, honors, recognitions)]
}}

📋 EXTRACTION RULES:

1. **NAME** - Look at resume header/top. Extract full name (first + last).

2. **CONTACT INFORMATION**:
   - Email: Search entire resume for patterns with @
   - Phone: Accept all formats: (xxx) xxx-xxxx, xxx-xxx-xxxx, +x xxx-xxx-xxxx
   - LinkedIn: Full URL or username from linkedin.com/in/
   - Website: GitHub links, portfolios, personal domains

3. **SUMMARY** - Extract from sections labeled:
   - Summary, Professional Summary, Objective, Career Objective
   - About, About Me, Profile, Overview, Executive Summary
   - Include COMPLETE text, not truncated

4. **SKILLS** - Be COMPREHENSIVE. Extract from:
   - Dedicated Skills/Technical Skills section
   - Technologies mentioned in experience bullets
   - Programming languages, frameworks, databases, tools
   - Cloud platforms (AWS, Azure, GCP)
   - Soft skills if explicitly listed
   - Extract individual items (separate "Python, Java" into ["Python", "Java"])

5. **WORK EXPERIENCE** - For EACH role:
   - Title: Exact job title as written
   - Company: Full company name
   - Dates: Convert to YYYY-MM format
     * "Jan 2020" → "2020-01"
     * "January 2020" → "2020-01"
     * "01/2020" → "2020-01"
     * "Present", "Current", "Now" → null for end_date
   - Location: City, State or City, Country
   - Responsibilities: Extract EVERY bullet point
   - Impact Score: 
     * 0.9-1.0: Bullets with numbers/metrics and strong impact
     * 0.7-0.8: Bullets with action verbs and clear outcomes
     * 0.5-0.6: Descriptive bullets with moderate detail
     * 0.3-0.4: Basic responsibility descriptions
     * 0.0-0.2: Very basic/vague duties

6. **EDUCATION** - For EACH degree:
   - Degree: Full degree name (e.g., "Bachelor of Science", "Master of Business Administration")
   - Field of Study: Major/specialization (e.g., "Computer Science", "Mechanical Engineering")
   - Institution: Full school/university name
   - Dates: YYYY format for start/end year
   - GPA: Extract if mentioned (e.g., "3.8/4.0", "3.8 GPA", "3.8")
   - Location: City, State/Country if available
   - Honors: Include if mentioned (e.g., "Summa Cum Laude", "Dean's List", "With Honors")
   - Year: Graduation year (for backward compatibility)

7. **PROJECTS** - For EACH project:
   - Name: Project title/name
   - Description: Brief description of the project
   - Technologies: List of technologies/tools used
   - URL: GitHub, live demo, or portfolio link if available
   - Dates: Start and end dates if mentioned

8. **CERTIFICATIONS** - For EACH certification, extract as structured object:
   - Name: Full certification name (e.g., "AWS Certified Solutions Architect", "PMP")
   - Issuing Organization: Who issued it (e.g., "Amazon Web Services", "PMI", "Google")
   - Issue Date: When obtained (YYYY-MM or YYYY format)
   - Expiry Date: When it expires (if applicable, null otherwise)
   - Credential ID: Certificate/credential number if mentioned
   - Credential URL: Verification URL if available

9. **ACHIEVEMENTS** - Extract notable accomplishments:
   - Significant achievements not covered in experience bullets
   - Competition wins, hackathon prizes
   - Publications, patents, research contributions
   - Notable projects or initiatives led

10. **LANGUAGES** - Extract spoken/written languages:
    - Include language name and proficiency if mentioned
    - Examples: "English (Native)", "Spanish (Fluent)", "French (Intermediate)"

11. **AWARDS** - Extract awards, honors, and recognitions:
    - Academic awards (Dean's List, scholarships)
    - Professional awards and recognitions
    - Industry honors and distinctions
    - Include year if mentioned

{strict_instruction}

NOW PARSE THIS RESUME:
---
{resume_text}
---

OUTPUT (JSON only - no markdown, no code blocks, no text before/after):"""
        
        return prompt
    
    async def parse_resume(self, resume_text: str) -> Resume:
        """
        Parse resume text into structured Resume object with multiple retries.
        """
        # Attempt 1: Standard parsing
        try:
            print("🔍 Attempt 1: Standard Gemini parsing...")
            result = await self._call_gemini(resume_text, strict_mode=False)
            if result:
                print("✅ Successfully parsed with Gemini (standard mode)")
                return result
        except Exception as e:
            print(f"⚠️  Attempt 1 failed: {str(e)[:100]}")
        
        # Attempt 2: Strict mode parsing
        try:
            print("🔍 Attempt 2: Strict mode Gemini parsing...")
            result = await self._call_gemini(resume_text, strict_mode=True)
            if result:
                print("✅ Successfully parsed with Gemini (strict mode)")
                return result
        except Exception as e:
            print(f"⚠️  Attempt 2 failed: {str(e)[:100]}")
        
        # Attempt 3: Enhanced fallback parsing
        print("🔧 Falling back to enhanced rule-based parsing...")
        return self._enhanced_fallback_parse(resume_text)
    
    async def _call_gemini(self, resume_text: str, strict_mode: bool) -> Optional[Resume]:
        """Call Gemini API with enhanced error handling."""
        prompt = self._create_prompt(resume_text, strict_mode)
        
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )
        
        # Extract and clean JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks
        response_text = re.sub(r'^```json\s*', '', response_text, flags=re.MULTILINE)
        response_text = re.sub(r'^```\s*', '', response_text, flags=re.MULTILINE)
        response_text = re.sub(r'\s*```$', '', response_text, flags=re.MULTILINE)
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            # Try to fix common JSON issues
            print(f"⚠️  JSON parse error: {e}")
            # Remove any text before first { and after last }
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                response_text = match.group(0)
                data = json.loads(response_text)
            else:
                raise
        
        # Transform certifications from strings to objects if needed
        if 'certifications' in data and isinstance(data['certifications'], list):
            transformed_certs = []
            for cert in data['certifications']:
                if isinstance(cert, str):
                    # Convert string to object
                    transformed_certs.append({
                        'name': cert,
                        'issuing_organization': None,
                        'issue_date': None,
                        'expiry_date': None,
                        'credential_id': None,
                        'credential_url': None
                    })
                elif isinstance(cert, dict):
                    # Already an object, keep it
                    transformed_certs.append(cert)
            data['certifications'] = transformed_certs
        
        # Transform projects from strings/simple objects if needed
        if 'projects' in data and isinstance(data['projects'], list):
            transformed_projects = []
            for proj in data['projects']:
                if isinstance(proj, str):
                    transformed_projects.append({
                        'name': proj,
                        'description': None,
                        'technologies': [],
                        'url': None,
                        'start_date': None,
                        'end_date': None
                    })
                elif isinstance(proj, dict):
                    # Ensure all required fields exist
                    proj.setdefault('name', 'Unnamed Project')
                    proj.setdefault('description', None)
                    proj.setdefault('technologies', [])
                    proj.setdefault('url', None)
                    proj.setdefault('start_date', None)
                    proj.setdefault('end_date', None)
                    transformed_projects.append(proj)
            data['projects'] = transformed_projects
        
        # Add metadata fields
        data['parsed_at'] = datetime.utcnow()
        data['resume_hash'] = hashlib.sha256(resume_text.encode()).hexdigest()
        data['source'] = 'gemini-enhanced'
        
        # Validate with Pydantic
        resume = Resume(**data)
        return resume
    
    def _enhanced_fallback_parse(self, resume_text: str) -> Resume:
        """
        Enhanced rule-based fallback parser with improved extraction.
        Used when LLM fails completely.
        """
        lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
        text_lower = resume_text.lower()
        
        # Extract name (first substantial line, usually at top)
        name = "Unknown Candidate"
        for line in lines[:5]:  # Check first 5 lines
            # Skip lines that look like contact info
            if '@' not in line and 'http' not in line.lower() and len(line.split()) <= 4:
                if not any(char.isdigit() for char in line):  # Avoid phone numbers
                    name = line
                    break
        
        # Extract email (improved pattern)
        email = None
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, resume_text)
        if email_match:
            email = email_match.group(0)
        
        # Extract phone (improved pattern)
        phone = None
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # International + US
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, resume_text)
            if phone_match:
                phone = phone_match.group(0)
                break
        
        # Extract LinkedIn
        linkedin = None
        linkedin_patterns = [
            r'linkedin\.com/in/[\w-]+',
            r'linkedin\.com/pub/[\w-]+',
        ]
        for pattern in linkedin_patterns:
            linkedin_match = re.search(pattern, resume_text, re.IGNORECASE)
            if linkedin_match:
                linkedin = linkedin_match.group(0)
                break
        
        # Extract website/GitHub
        website = None
        website_patterns = [
            r'github\.com/[\w-]+',
            r'portfolio\.[a-zA-Z0-9.-]+\.[a-z]{2,}',
            r'https?://[a-zA-Z0-9.-]+\.[a-z]{2,}',
        ]
        for pattern in website_patterns:
            website_match = re.search(pattern, resume_text, re.IGNORECASE)
            if website_match:
                website = website_match.group(0)
                if 'linkedin' not in website.lower():  # Skip if it's LinkedIn
                    break
        
        # Extract skills (comprehensive list)
        skill_database = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
            'go', 'golang', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
            # Web Frameworks
            'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'django', 'flask',
            'fastapi', 'express', 'node.js', 'spring boot', 'asp.net', 'laravel',
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
            'dynamodb', 'oracle', 'sql server', 'sqlite', 'neo4j',
            # Cloud & DevOps
            'aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'terraform', 'ansible', 'ci/cd', 'gitlab', 'github actions',
            # Data & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'data science', 'data analysis', 'spark', 'hadoop',
            # Other Tools
            'git', 'jira', 'confluence', 'slack', 'postman', 'graphql', 'rest api',
            'microservices', 'agile', 'scrum', 'linux', 'bash',
            # Marketing Skills
            'seo', 'sem', 'google analytics', 'content marketing', 'social media',
            'email marketing', 'hubspot', 'mailchimp', 'a/b testing',
        ]
        
        skills = []
        for skill in skill_database:
            if skill in text_lower:
                # Capitalize properly
                skills.append(skill.title())
        
        # Remove duplicates and sort
        skills = sorted(list(set(skills)))
        
        # Extract summary (look for summary section)
        summary = "Parsed with enhanced fallback method - please review and update as needed"
        summary_keywords = ['summary', 'objective', 'profile', 'about']
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                # Get next few lines as summary
                summary_lines = []
                for j in range(i+1, min(i+6, len(lines))):
                    if lines[j] and not lines[j].isupper():
                        summary_lines.append(lines[j])
                    else:
                        break
                if summary_lines:
                    summary = ' '.join(summary_lines)
                break
        
        # Try to extract basic experience info
        experiences = []
        experience_keywords = ['experience', 'employment', 'work history', 'professional experience']
        in_experience_section = False
        current_exp = None
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if we're entering experience section
            if any(keyword in line_lower for keyword in experience_keywords) and len(line.split()) < 5:
                in_experience_section = True
                continue
            
            # Stop if we hit education section
            if 'education' in line_lower and len(line.split()) < 3:
                in_experience_section = False
            
            if in_experience_section:
                # Try to identify job title/company lines (usually have | or - separators)
                if '|' in line or ' - ' in line or ' – ' in line:
                    parts = re.split(r'\s+[-–|]\s+', line)
                    if len(parts) >= 2:
                        if current_exp:
                            experiences.append(current_exp)
                        current_exp = {
                            'title': parts[0] if parts[0] else 'Position',
                            'company': parts[1] if len(parts) > 1 else 'Company',
                            'start_date': 'Unknown',  # Required field, default to 'Unknown'
                            'end_date': None,
                            'location': parts[2] if len(parts) > 2 else None,
                            'responsibilities': [],
                            'bullet_impact_score': 0.3
                        }
        
        if current_exp and current_exp not in experiences:
            experiences.append(current_exp)
        
        # Create resume object with enhanced fallback data
        resume = Resume(
            name=name,
            contact={
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
                "website": website
            },
            summary=summary,
            skills=skills if skills else ["Manual review required - no skills auto-detected"],
            experiences=experiences,
            education=[],
            projects=[],
            certifications=[],
            achievements=[],
            languages=[],
            awards=[],
            parsed_at=datetime.utcnow(),
            resume_hash=hashlib.sha256(resume_text.encode()).hexdigest(),
            source="enhanced-fallback"
        )
        
        print(f"✅ Fallback parsing complete: {len(skills)} skills, {len(experiences)} experiences")
        return resume


# Global Gemini service instance
gemini_service = GeminiService()
