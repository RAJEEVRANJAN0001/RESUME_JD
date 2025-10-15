"""
Pydantic models for request/response validation and MongoDB documents.
Canonical schema for resume data structure.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import List, Optional, Any
from datetime import datetime
from bson import ObjectId


# Custom ObjectId type for MongoDB compatible with Pydantic v2
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ],
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x)
        ))

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> JsonSchemaValue:
        return {"type": "string"}


# Contact Information
class Contact(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None


# Work Experience
class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None  # Job description/summary
    responsibilities: List[str] = []
    bullet_impact_score: Optional[float] = 0.0


# Education
class Education(BaseModel):
    degree: str
    institution: str
    field_of_study: Optional[str] = None  # Major/Field of study
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None  # GPA score
    location: Optional[str] = None  # University location
    honors: Optional[str] = None  # Honors, Dean's List, etc.
    year: Optional[str] = None  # Graduation year (for backward compatibility)


# Certification/Award
class Certification(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


# Project
class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = []
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


# Main Resume Schema (Canonical)
class Resume(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    name: str
    contact: Optional[Contact] = None
    summary: Optional[str] = None
    skills: List[str] = []
    experiences: List[Experience] = []
    education: List[Education] = []
    projects: List[Project] = []
    certifications: List[Certification] = []
    achievements: List[str] = []  # General achievements/accomplishments
    languages: List[str] = []
    awards: List[str] = []  # Awards and honors
    parsed_at: datetime = Field(default_factory=datetime.utcnow)
    resume_hash: str
    source: Optional[str] = "upload"
    file_id: Optional[str] = None  # GridFS file ID


# Resume stored in MongoDB (includes _id)
class ResumeInDB(Resume):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")


# Resume response (converts _id to id)
class ResumeResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    name: str
    contact: Optional[Contact] = None
    summary: Optional[str] = None
    skills: List[str] = []
    experiences: List[Experience] = []
    education: List[Education] = []
    projects: List[Project] = []
    certifications: List[Certification] = []  # Updated to use Certification model
    achievements: List[str] = []
    languages: List[str] = []
    awards: List[str] = []
    parsed_at: datetime
    resume_hash: str
    source: Optional[str] = "upload"
    file_id: Optional[str] = None
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


# Upload response with match score
class UploadResponse(BaseModel):
    message: str
    resume_id: str
    resume_data: ResumeResponse
    match_score: Optional[float] = None
    match_details: Optional[dict] = None


# Job description for matching
class JobDescription(BaseModel):
    title: Optional[str] = "Job Position"
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_years: Optional[int] = None


# Match request
class MatchRequest(BaseModel):
    resume_id: str
    job_description: JobDescription


# Match response
class MatchResponse(BaseModel):
    resume_id: str
    match_score: float
    details: dict


# User Settings model
class UserSettings(BaseModel):
    email_notifications: bool = True
    auto_process_resumes: bool = False
    match_score_threshold: int = 70
    company_name: Optional[str] = None


# User model for authentication
class User(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    settings: UserSettings = Field(default_factory=UserSettings)


class UserInDB(User):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")


# User update schemas
class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None


class UserSettingsUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    auto_process_resumes: Optional[bool] = None
    match_score_threshold: Optional[int] = None
    company_name: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    settings: UserSettings


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
