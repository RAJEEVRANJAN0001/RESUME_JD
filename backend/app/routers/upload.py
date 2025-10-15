"""
Upload router for resume file upload and parsing.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from app.models import User, UploadResponse, ResumeResponse, JobDescription
from app.dependencies import get_current_user
from app.database import get_database
from app.services.azure_parser import azure_parser
from app.services.gemini_service import gemini_service
from app.services.storage import storage_service
from app.services.enhanced_scoring import enhanced_resume_scorer
from typing import Optional
import hashlib

router = APIRouter(prefix="/api", tags=["Upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    required_skills: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """
    Upload and parse resume file (PDF or DOCX).
    Optionally match against job description.
    
    Example request (multipart/form-data):
    - file: resume.pdf
    - job_description: "Senior Software Engineer with 5+ years experience..."
    - required_skills: "Python,JavaScript,React,AWS"
    
    Example response:
    ```json
    {
      "message": "Resume uploaded and parsed successfully",
      "resume_id": "507f1f77bcf86cd799439011",
      "resume_data": {
        "id": "507f1f77bcf86cd799439011",
        "name": "John Doe",
        "contact": {
          "email": "john@example.com",
          "phone": "(555) 123-4567"
        },
        "skills": ["Python", "JavaScript", "React"],
        "experiences": [...],
        "education": [...],
        "parsed_at": "2024-01-15T10:30:00",
        "resume_hash": "abc123..."
      },
      "match_score": 85.5,
      "match_details": {
        "total_score": 85.5,
        "breakdown": {
          "skills_score": 90.0,
          "experience_score": 85.0,
          "education_score": 80.0,
          "semantic_score": 75.0
        },
        "matched_skills": ["python", "javascript", "react"],
        "missing_skills": ["aws"],
        "experience_years": 6.0
      }
    }
    ```
    """
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Store file in GridFS first
        file_id = await storage_service.store_file(
            file_content,
            file.filename,
            file.content_type or "application/octet-stream"
        )
        
        # Parse document with Azure
        print(f"📄 Parsing document: {file.filename}")
        text_content = await azure_parser.parse_document(file_content, file.filename)
        
        # Calculate text hash for duplicate detection
        text_hash = hashlib.sha256(text_content.encode()).hexdigest()
        db = get_database()
        
        # Check for duplicate using text content hash (same as what Gemini will generate)
        existing_resume = await db.resumes.find_one({"resume_hash": text_hash})
        if existing_resume:
            # If duplicate found, delete the newly uploaded file and return existing resume
            print(f"⚠️  Duplicate resume detected (hash: {text_hash}). Using existing resume ID: {existing_resume['_id']}")
            
            # Delete the duplicate file we just uploaded
            await storage_service.delete_file(file_id)
            
            # If job description provided, re-calculate match score
            match_score = None
            match_details = None
            
            if job_description:
                from app.models import Resume
                resume_obj = Resume(**existing_resume)
                
                jd = JobDescription(
                    description=job_description,
                    required_skills=required_skills.split(",") if required_skills else []
                )
                
                match_result = enhanced_resume_scorer.calculate_match_score(
                    resume=resume_obj,
                    job_description=jd
                )
                match_score = match_result["total_score"]
                match_details = match_result
            
            # Convert MongoDB document to ResumeResponse
            resume_response = ResumeResponse(
                id=str(existing_resume["_id"]),
                **{k: v for k, v in existing_resume.items() if k != "_id"}
            )
            
            return UploadResponse(
                message="Resume already exists. Returning existing data.",
                resume_id=str(existing_resume["_id"]),
                resume_data=resume_response,
                match_score=match_score,
                match_details=match_details
            )
        
        # Extract structured data with Gemini (will generate same hash we already calculated)
        print(f"🤖 Extracting structured data with Gemini...")
        resume = await gemini_service.parse_resume(text_content)
        
        # Add file ID
        resume.file_id = file_id
        
        # Insert to database
        resume_dict = resume.dict(by_alias=True, exclude={"id"})
        result = await db.resumes.insert_one(resume_dict)
        resume_id = str(result.inserted_id)
        
        # Prepare response
        resume_response = ResumeResponse(
            id=resume_id,
            **resume.dict(exclude={"id"})
        )
        
        response = UploadResponse(
            message="Resume uploaded and parsed successfully",
            resume_id=resume_id,
            resume_data=resume_response
        )
        
        # Calculate match score if job description provided
        if job_description:
            skills_list = []
            if required_skills:
                skills_list = [s.strip() for s in required_skills.split(',')]
            
            job_desc = JobDescription(
                description=job_description,
                required_skills=skills_list,
                preferred_skills=[],
                experience_years=None
            )
            
            match_details = enhanced_resume_scorer.calculate_match_score(resume, job_desc)
            response.match_score = match_details["total_score"]
            response.match_details = match_details
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume: {str(e)}"
        )
