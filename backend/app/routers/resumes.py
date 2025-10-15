"""
Resume CRUD operations and matching endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from app.models import (
    User, Resume, ResumeResponse, MatchRequest, MatchResponse
)
from app.dependencies import get_current_user
from app.database import get_database
from app.services.enhanced_scoring import enhanced_resume_scorer
from app.services.storage import storage_service
from bson import ObjectId
from typing import List, Optional
import io

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])


@router.get("", response_model=List[ResumeResponse])
async def list_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    skills: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """
    List all resumes with pagination and optional filtering.
    
    Query parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to return (default: 50)
    - search: Text search in name, summary, skills
    - skills: Comma-separated skills to filter by
    
    Example request:
    ```
    GET /api/resumes?skip=0&limit=10&search=engineer&skills=Python,React
    ```
    
    Example response:
    ```json
    [
      {
        "id": "507f1f77bcf86cd799439011",
        "name": "John Doe",
        "contact": {...},
        "skills": ["Python", "React"],
        "experiences": [...],
        "education": [...],
        "parsed_at": "2024-01-15T10:30:00",
        "resume_hash": "abc123..."
      }
    ]
    ```
    """
    db = get_database()
    
    # Build query
    query = {}
    
    if search:
        query["$text"] = {"$search": search}
    
    if skills:
        skills_list = [s.strip() for s in skills.split(',')]
        query["skills"] = {"$in": skills_list}
    
    # Fetch resumes
    cursor = db.resumes.find(query).skip(skip).limit(limit).sort("parsed_at", -1)
    resumes = await cursor.to_list(length=limit)
    
    # Convert to response models
    response = []
    for resume in resumes:
        # Transform certifications if needed (backward compatibility)
        if "certifications" in resume and isinstance(resume["certifications"], list):
            transformed_certs = []
            for cert in resume["certifications"]:
                if isinstance(cert, str):
                    # Old format: convert string to object
                    transformed_certs.append({
                        "name": cert,
                        "issuing_organization": None,
                        "issue_date": None,
                        "expiry_date": None,
                        "credential_id": None,
                        "credential_url": None
                    })
                elif isinstance(cert, dict):
                    # New format: already an object
                    transformed_certs.append(cert)
            resume["certifications"] = transformed_certs
        
        # Transform projects if needed
        if "projects" not in resume:
            resume["projects"] = []
        
        # Add missing fields for backward compatibility
        if "achievements" not in resume:
            resume["achievements"] = []
        if "languages" not in resume:
            resume["languages"] = []
        if "awards" not in resume:
            resume["awards"] = []
        
        response.append(ResumeResponse(
            id=str(resume["_id"]),
            **{k: v for k, v in resume.items() if k != "_id"}
        ))
    
    return response


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get single resume by ID.
    
    Example request:
    ```
    GET /api/resumes/507f1f77bcf86cd799439011
    ```
    
    Example response:
    ```json
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "contact": {
        "email": "john@example.com",
        "phone": "(555) 123-4567",
        "linkedin": "linkedin.com/in/johndoe"
      },
      "summary": "Experienced software engineer...",
      "skills": ["Python", "JavaScript", "React", "AWS"],
      "experiences": [
        {
          "title": "Senior Software Engineer",
          "company": "Tech Corp",
          "start_date": "2021-01",
          "end_date": null,
          "location": "San Francisco, CA",
          "responsibilities": [
            "Led development of microservices",
            "Mentored junior developers"
          ],
          "bullet_impact_score": 0.8
        }
      ],
      "education": [
        {
          "degree": "BS Computer Science",
          "institution": "MIT",
          "start_date": "2014",
          "end_date": "2018"
        }
      ],
      "certifications": ["AWS Certified"],
      "parsed_at": "2024-01-15T10:30:00",
      "resume_hash": "abc123...",
      "source": "gemini",
      "file_id": "file123"
    }
    ```
    """
    db = get_database()
    
    try:
        resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID format"
        )
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Transform certifications if needed (backward compatibility)
    if "certifications" in resume and isinstance(resume["certifications"], list):
        transformed_certs = []
        for cert in resume["certifications"]:
            if isinstance(cert, str):
                # Convert string to object
                transformed_certs.append({
                    "name": cert,
                    "issuing_organization": None,
                    "issue_date": None,
                    "expiration_date": None,
                    "credential_id": None,
                    "credential_url": None
                })
            else:
                transformed_certs.append(cert)
        resume["certifications"] = transformed_certs
    
    # Ensure new fields exist (backward compatibility)
    resume.setdefault("projects", [])
    resume.setdefault("achievements", [])
    resume.setdefault("languages", [])
    resume.setdefault("awards", [])
    
    return ResumeResponse(
        id=str(resume["_id"]),
        **{k: v for k, v in resume.items() if k != "_id"}
    )


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    resume_data: Resume,
    current_user: User = Depends(get_current_user)
):
    """
    Update resume data.
    
    Example request:
    ```json
    {
      "name": "John Doe (Updated)",
      "contact": {...},
      "skills": ["Python", "JavaScript", "React", "Node.js"],
      "experiences": [...],
      "education": [...],
      "certifications": ["AWS Certified Solutions Architect"],
      "parsed_at": "2024-01-15T10:30:00",
      "resume_hash": "abc123...",
      "source": "gemini"
    }
    ```
    """
    db = get_database()
    
    try:
        object_id = ObjectId(resume_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID format"
        )
    
    # Check if resume exists
    existing = await db.resumes.find_one({"_id": object_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Update resume
    update_data = resume_data.dict(exclude={"id"}, exclude_unset=True)
    await db.resumes.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    # Fetch updated resume
    updated_resume = await db.resumes.find_one({"_id": object_id})
    
    # Transform certifications if needed (backward compatibility)
    if "certifications" in updated_resume and isinstance(updated_resume["certifications"], list):
        transformed_certs = []
        for cert in updated_resume["certifications"]:
            if isinstance(cert, str):
                # Convert string to object
                transformed_certs.append({
                    "name": cert,
                    "issuing_organization": None,
                    "issue_date": None,
                    "expiration_date": None,
                    "credential_id": None,
                    "credential_url": None
                })
            else:
                transformed_certs.append(cert)
        updated_resume["certifications"] = transformed_certs
    
    # Ensure new fields exist (backward compatibility)
    updated_resume.setdefault("projects", [])
    updated_resume.setdefault("achievements", [])
    updated_resume.setdefault("languages", [])
    updated_resume.setdefault("awards", [])
    
    return ResumeResponse(
        id=str(updated_resume["_id"]),
        **{k: v for k, v in updated_resume.items() if k != "_id"}
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete resume by ID.
    
    Example request:
    ```
    DELETE /api/resumes/507f1f77bcf86cd799439011
    ```
    """
    db = get_database()
    
    try:
        object_id = ObjectId(resume_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID format"
        )
    
    resume = await db.resumes.find_one({"_id": object_id})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Delete associated file if exists
    if resume.get("file_id"):
        await storage_service.delete_file(resume["file_id"])
    
    # Delete resume
    await db.resumes.delete_one({"_id": object_id})
    
    return None


@router.post("/match", response_model=MatchResponse)
async def match_resume(
    match_request: MatchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Match resume against job description and calculate score.
    
    Example request:
    ```json
    {
      "resume_id": "507f1f77bcf86cd799439011",
      "job_description": {
        "title": "Senior Software Engineer",
        "description": "Looking for experienced engineer with Python and React...",
        "required_skills": ["Python", "React", "AWS"],
        "preferred_skills": ["Docker", "Kubernetes"],
        "experience_years": 5
      }
    }
    ```
    
    Example response:
    ```json
    {
      "resume_id": "507f1f77bcf86cd799439011",
      "match_score": 85.5,
      "details": {
        "total_score": 85.5,
        "breakdown": {
          "skills_score": 90.0,
          "experience_score": 85.0,
          "education_score": 80.0,
          "semantic_score": 75.0
        },
        "matched_skills": ["python", "react", "aws"],
        "missing_skills": [],
        "experience_years": 6.0
      }
    }
    ```
    """
    db = get_database()
    
    # Fetch resume
    try:
        resume_doc = await db.resumes.find_one({"_id": ObjectId(match_request.resume_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID format"
        )
    
    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Convert to Resume model
    resume = Resume(**{k: v for k, v in resume_doc.items() if k != "_id"})
    
    # Calculate match score using enhanced AI-powered scoring
    match_details = enhanced_resume_scorer.calculate_match_score(
        resume,
        match_request.job_description
    )
    
    return MatchResponse(
        resume_id=match_request.resume_id,
        match_score=match_details["total_score"],
        details=match_details
    )


@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Download original resume file.
    
    Example request:
    ```
    GET /api/resumes/507f1f77bcf86cd799439011/download
    ```
    """
    db = get_database()
    
    try:
        resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID format"
        )
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    if not resume.get("file_id"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Original file not available"
        )
    
    # Retrieve file from GridFS
    file_data = await storage_service.retrieve_file(resume["file_id"])
    
    if not file_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in storage"
        )
    
    file_content, filename, content_type = file_data
    
    return StreamingResponse(
        io.BytesIO(file_content),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
