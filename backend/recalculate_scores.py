#!/usr/bin/env python3
"""
Script to recalculate match scores for existing resumes in the database.
This fixes resumes that were uploaded before the scoring bug was fixed.
"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import Resume, JobDescription
from app.services.enhanced_scoring import EnhancedResumeScorer
from app.icons import CHECK_MARK, X_MARK, INFO, CHART, CELEBRATION, ROCKET, TARGET, CLIPBOARD
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_database():
    """Get database connection."""
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    return client.resume_screener

async def get_default_job_description():
    """Get or create a default job description for scoring."""
    return JobDescription(
        title="Software Developer",
        company="Tech Company",
        description="We are looking for a skilled software developer to join our team.",
        requirements=[
            "Bachelor's degree in Computer Science or related field",
            "3+ years of programming experience",
            "Strong problem-solving skills"
        ],
        required_skills=[
            "Python", "JavaScript", "SQL", "Git", "REST APIs",
            "HTML", "CSS", "React", "Node.js", "MongoDB"
        ],
        preferred_skills=[
            "Java", "C++", "Docker", "AWS", "Machine Learning",
            "Data Science", "DevOps", "Agile", "Testing"
        ],
        experience_level="Mid-level",
        location="Remote",
        employment_type="Full-time",
        salary_range="$70,000 - $120,000",
        benefits=["Health insurance", "401k", "Remote work"],
        application_deadline=None,
        is_active=True
    )

async def recalculate_resume_scores():
    """Recalculate match scores for all resumes."""
    try:
        # Get database connection
        db = await get_database()
        scorer = EnhancedResumeScorer()
        job_desc = await get_default_job_description()
        
        logger.info(f"[🔍] Finding all resumes for score recalculation...")
        
        # Find ALL resumes to recalculate scores
        resumes_cursor = db.resumes.find({})
        
        resumes = await resumes_cursor.to_list(length=1000)
        
        if not resumes:
            logger.info(f"{CHECK_MARK} No resumes found in database.")
            return True
        
        logger.info(f"{CLIPBOARD} Found {len(resumes)} resumes to process")
        
        updated_count = 0
        failed_count = 0
        
        for resume_doc in resumes:
            try:
                logger.info(f"🔄 Processing: {resume_doc.get('name', 'Unknown')}")
                
                # Convert to Resume model
                resume = Resume(**resume_doc)
                
                # Calculate new match score
                match_result = scorer.calculate_match_score(resume, job_desc)
                new_score = match_result["total_score"]
                
                # Update in database
                await db.resumes.update_one(
                    {"_id": resume_doc["_id"]},
                    {
                        "$set": {
                            "match_score": new_score,
                            "match_details": match_result,
                            "score_updated_at": "2025-10-15T22:30:00"
                        }
                    }
                )
                
                updated_count += 1
                logger.info(f"{CHECK_MARK} Updated {resume_doc.get('name', 'Unknown')}: {new_score}%")
                
            except Exception as e:
                failed_count += 1
                logger.error(f"{X_MARK} Failed to update {resume_doc.get('name', 'Unknown')}: {e}")
                continue
        
        logger.info(f"\n{CELEBRATION} Score recalculation complete!")
        logger.info(f"{CHECK_MARK} Successfully updated: {updated_count} resumes")
        logger.info(f"{X_MARK} Failed to update: {failed_count} resumes")
        
    except Exception as e:
        logger.error(f"[💥] Fatal error during score recalculation: {e}")
        return False
    
    return True

async def main():
    """Main function."""
    logger.info(f"{ROCKET} Starting resume score recalculation...")
    
    success = await recalculate_resume_scores()
    
    if success:
        logger.info(f"{TARGET} All done! Your analytics should now show correct scores.")
    else:
        logger.error("[💥] Recalculation failed. Please check the logs.")
        sys.exit(1)

if __name__ == "__main__":
    # Add the parent directory to sys.path so we can import app modules
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Run the script
    asyncio.run(main())