"""
Test script to verify enhanced resume parsing with education, certifications, and achievements.
"""
import asyncio
import json
from app.services.gemini_service import gemini_service
from app.icons import CHECK_MARK, X_MARK, WARNING, CLIPBOARD, DOCUMENT, TOOLS, ROCKET, TROPHY, GEAR, CHART, CELEBRATION

# Sample resume text with comprehensive information
SAMPLE_RESUME = """
JOHN DOE
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe | github.com/johndoe
San Francisco, CA

PROFESSIONAL SUMMARY
Results-driven Software Engineer with 5+ years of experience in full-stack development. 
Proven expertise in building scalable web applications using modern technologies and cloud platforms.

EDUCATION

Bachelor of Science in Computer Science
Stanford University, Stanford, CA
August 2015 - May 2019
GPA: 3.8/4.0
Summa Cum Laude, Dean's List (All Semesters)

WORK EXPERIENCE

Senior Software Engineer | Tech Corp | San Francisco, CA
June 2021 - Present
• Architected and deployed microservices architecture serving 1M+ daily users
• Led team of 5 engineers in developing new feature that increased user engagement by 35%
• Implemented CI/CD pipeline reducing deployment time by 60%
• Mentored 3 junior developers and conducted technical interviews

Software Engineer | StartupXYZ | Palo Alto, CA
July 2019 - May 2021
• Developed RESTful APIs using Python FastAPI serving 100K+ requests daily
• Built React-based dashboard improving customer retention by 25%
• Optimized database queries reducing response time by 40%
• Collaborated with product team to define technical requirements

PROJECTS

E-Commerce Platform
• Built full-stack e-commerce platform using React, Node.js, and PostgreSQL
• Integrated Stripe payment processing and AWS S3 for image storage
• Implemented real-time inventory management using WebSockets
https://github.com/johndoe/ecommerce

AI Chatbot
• Developed intelligent chatbot using Python, TensorFlow, and NLP
• Achieved 85% accuracy in intent classification
• Deployed on AWS Lambda for serverless architecture
January 2023 - April 2023

CERTIFICATIONS

AWS Certified Solutions Architect - Associate
Amazon Web Services
Issued: March 2023
Credential ID: AWS-SA-123456
https://aws.amazon.com/verification/ABC123

Google Cloud Professional Cloud Architect
Google Cloud
Issued: January 2022
Expires: January 2025

Certified Kubernetes Administrator (CKA)
Cloud Native Computing Foundation
Issued: June 2021

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, Java, SQL
Frameworks: React, Node.js, Django, FastAPI, Express.js, Spring Boot
Databases: PostgreSQL, MongoDB, Redis, MySQL, DynamoDB
Cloud: AWS (EC2, S3, Lambda, RDS), Google Cloud Platform, Azure
DevOps: Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform
Tools: Git, JIRA, Postman, VS Code, Linux

ACHIEVEMENTS
• Winner, Best Innovation Award at Tech Corp Annual Hackathon (2023)
• Published research paper on "Optimizing ML Model Performance" in IEEE Journal (2022)
• Led company-wide initiative to adopt microservices, reducing infrastructure costs by $200K annually

AWARDS
• Employee of the Year, Tech Corp (2022)
• Academic Excellence Scholarship, Stanford University (2015-2019)
• First Place, Silicon Valley Startup Weekend (2020)

LANGUAGES
English (Native)
Spanish (Fluent)
Mandarin Chinese (Intermediate)
"""


async def test_parsing():
    """Test the enhanced parsing functionality."""
    print("=" * 80)
    print("TESTING ENHANCED RESUME PARSING")
    print("=" * 80)
    
    try:
        # Parse the sample resume
        print(f"\n[🔍] Parsing sample resume...\n")
        resume = await gemini_service.parse_resume(SAMPLE_RESUME)
        
        # Convert to dict for pretty printing
        resume_dict = resume.model_dump()
        
        print("\n" + "=" * 80)
        print("PARSING RESULTS")
        print("=" * 80)
        
        # Print basic info
        print(f"\n{CLIPBOARD} BASIC INFORMATION:")
        print(f"   Name: {resume.name}")
        print(f"   Email: {resume.contact.email if resume.contact else 'N/A'}")
        print(f"   Phone: {resume.contact.phone if resume.contact else 'N/A'}")
        print(f"   LinkedIn: {resume.contact.linkedin if resume.contact else 'N/A'}")
        
        # Print summary
        print(f"\n{DOCUMENT} SUMMARY:")
        print(f"   {resume.summary[:100]}..." if resume.summary else "   N/A")
        
        # Print skills
        print(f"\n{TOOLS} SKILLS ({len(resume.skills)}):")
        print(f"   {', '.join(resume.skills[:10])}{'...' if len(resume.skills) > 10 else ''}")
        
        # Print education - ENHANCED
        print(f"\n🎓 EDUCATION ({len(resume.education)}):")
        for i, edu in enumerate(resume.education, 1):
            print(f"   {i}. {edu.degree}")
            print(f"      Institution: {edu.institution}")
            if edu.field_of_study:
                print(f"      Field of Study: {edu.field_of_study}")
            if edu.gpa:
                print(f"      GPA: {edu.gpa}")
            if edu.location:
                print(f"      Location: {edu.location}")
            if edu.honors:
                print(f"      Honors: {edu.honors}")
            print(f"      Years: {edu.start_date} - {edu.end_date}")
        
        # Print certifications - ENHANCED
        print(f"\n📜 CERTIFICATIONS ({len(resume.certifications)}):")
        for i, cert in enumerate(resume.certifications, 1):
            print(f"   {i}. {cert.name}")
            if cert.issuing_organization:
                print(f"      Issuer: {cert.issuing_organization}")
            if cert.issue_date:
                print(f"      Issued: {cert.issue_date}")
            if cert.expiry_date:
                print(f"      Expires: {cert.expiry_date}")
            if cert.credential_id:
                print(f"      Credential ID: {cert.credential_id}")
        
        # Print projects - ENHANCED
        print(f"\n{ROCKET} PROJECTS ({len(resume.projects)}):")
        for i, proj in enumerate(resume.projects, 1):
            print(f"   {i}. {proj.name}")
            if proj.description:
                print(f"      {proj.description[:80]}...")
            if proj.technologies:
                print(f"      Technologies: {', '.join(proj.technologies[:5])}")
            if proj.url:
                print(f"      URL: {proj.url}")
        
        # Print experience
        print(f"\n💼 WORK EXPERIENCE ({len(resume.experiences)}):")
        for i, exp in enumerate(resume.experiences, 1):
            print(f"   {i}. {exp.title} at {exp.company}")
            print(f"      {exp.start_date} - {exp.end_date or 'Present'}")
            print(f"      {len(exp.responsibilities)} responsibilities")
        
        # Print achievements - NEW
        print(f"\n{TROPHY} ACHIEVEMENTS ({len(resume.achievements)}):")
        for i, achievement in enumerate(resume.achievements, 1):
            print(f"   {i}. {achievement}")
        
        # Print awards - NEW
        print(f"\n[🥇] AWARDS ({len(resume.awards)}):")
        for i, award in enumerate(resume.awards, 1):
            print(f"   {i}. {award}")
        
        # Print languages - NEW
        print(f"\n🌐 LANGUAGES ({len(resume.languages)}):")
        for i, lang in enumerate(resume.languages, 1):
            print(f"   {i}. {lang}")
        
        # Print metadata
        print(f"\n{GEAR} METADATA:")
        print(f"   Source: {resume.source}")
        print(f"   Parsed At: {resume.parsed_at}")
        
        # Save full JSON for inspection
        output_file = "test_parsing_output.json"
        with open(output_file, 'w') as f:
            json.dump(resume_dict, f, indent=2, default=str)
        
        print(f"\n{CHECK_MARK} Full parsing results saved to: {output_file}")
        
        # Validation summary
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        checks = {
            "Name extracted": bool(resume.name and resume.name != "Unknown Candidate"),
            "Contact info extracted": bool(resume.contact and resume.contact.email),
            "Skills extracted": len(resume.skills) > 0,
            "Education extracted with GPA": any(edu.gpa for edu in resume.education),
            "Education extracted with location": any(edu.location for edu in resume.education),
            "Education extracted with honors": any(edu.honors for edu in resume.education),
            "Certifications structured": all(hasattr(cert, 'issuing_organization') for cert in resume.certifications),
            "Certifications have issuer": any(cert.issuing_organization for cert in resume.certifications),
            "Projects extracted": len(resume.projects) > 0,
            "Projects have technologies": any(proj.technologies for proj in resume.projects),
            "Achievements extracted": len(resume.achievements) > 0,
            "Awards extracted": len(resume.awards) > 0,
            "Languages extracted": len(resume.languages) > 0,
        }
        
        for check, passed in checks.items():
            icon = CHECK_MARK if passed else X_MARK
            print(f"{icon} {check}")
        
        passed_count = sum(checks.values())
        total_count = len(checks)
        
        print(f"\n{CHART} Score: {passed_count}/{total_count} checks passed ({passed_count/total_count*100:.1f}%)")
        
        if passed_count == total_count:
            print(f"\n{CELEBRATION} ALL CHECKS PASSED! Enhanced parsing is working correctly!")
        elif passed_count >= total_count * 0.8:
            print(f"\n{WARNING} Most checks passed, but some enhancements may need review.")
        else:
            print(f"\n{X_MARK} Several checks failed. Please review the parsing implementation.")
        
    except Exception as e:
        print(f"\n{X_MARK} ERROR during parsing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_parsing())
    exit(0 if success else 1)
