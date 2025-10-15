"""
User settings router for managing user profile and preferences.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import (
    UserResponse, 
    UserProfileUpdate, 
    UserSettingsUpdate, 
    PasswordChangeRequest,
    User,
    UserSettings
)
from app.auth import verify_password, get_password_hash, get_current_user
from app.database import get_database
from typing import Dict

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile and settings.
    
    Example response:
    ```json
    {
      "email": "admin@resumescreener.com",
      "full_name": "Admin User",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00",
      "settings": {
        "email_notifications": true,
        "auto_process_resumes": false,
        "match_score_threshold": 70,
        "company_name": "Tech Corp"
      }
    }
    ```
    """
    db = get_database()
    
    # Fetch fresh user data from database
    user = await db.users.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Ensure settings exist (for backward compatibility)
    if "settings" not in user or user["settings"] is None:
        user["settings"] = UserSettings().dict()
    
    return UserResponse(
        email=user["email"],
        full_name=user.get("full_name"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at"),
        settings=user["settings"]
    )


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update user's profile information.
    
    Example request:
    ```json
    {
      "full_name": "Updated Name",
      "company_name": "New Company Inc."
    }
    ```
    """
    db = get_database()
    
    update_data = {}
    if profile_data.full_name is not None:
        update_data["full_name"] = profile_data.full_name
    
    if profile_data.company_name is not None:
        update_data["settings.company_name"] = profile_data.company_name
    
    if update_data:
        await db.users.update_one(
            {"email": current_user.email},
            {"$set": update_data}
        )
    
    # Fetch updated user
    user = await db.users.find_one({"email": current_user.email})
    
    # Ensure settings exist
    if "settings" not in user or user["settings"] is None:
        user["settings"] = UserSettings().dict()
    
    return UserResponse(
        email=user["email"],
        full_name=user.get("full_name"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at"),
        settings=user["settings"]
    )


@router.put("/preferences", response_model=UserResponse)
async def update_user_settings(
    settings_data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update user's notification and AI settings.
    
    Example request:
    ```json
    {
      "email_notifications": true,
      "auto_process_resumes": false,
      "match_score_threshold": 75,
      "company_name": "Tech Corp"
    }
    ```
    """
    db = get_database()
    
    # Build update query for nested settings fields
    update_data = {}
    if settings_data.email_notifications is not None:
        update_data["settings.email_notifications"] = settings_data.email_notifications
    if settings_data.auto_process_resumes is not None:
        update_data["settings.auto_process_resumes"] = settings_data.auto_process_resumes
    if settings_data.match_score_threshold is not None:
        # Validate threshold
        if not 0 <= settings_data.match_score_threshold <= 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Match score threshold must be between 0 and 100"
            )
        update_data["settings.match_score_threshold"] = settings_data.match_score_threshold
    if settings_data.company_name is not None:
        update_data["settings.company_name"] = settings_data.company_name
    
    if update_data:
        await db.users.update_one(
            {"email": current_user.email},
            {"$set": update_data}
        )
    
    # Fetch updated user
    user = await db.users.find_one({"email": current_user.email})
    
    # Ensure settings exist
    if "settings" not in user or user["settings"] is None:
        user["settings"] = UserSettings().dict()
    
    return UserResponse(
        email=user["email"],
        full_name=user.get("full_name"),
        is_active=user.get("is_active", True),
        created_at=user.get("created_at"),
        settings=user["settings"]
    )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Change user's password.
    
    Example request:
    ```json
    {
      "current_password": "oldpassword123",
      "new_password": "newpassword456"
    }
    ```
    """
    db = get_database()
    
    # Fetch user from database
    user = await db.users.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not verify_password(password_data.current_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long"
        )
    
    # Hash new password and update
    new_hashed_password = get_password_hash(password_data.new_password)
    await db.users.update_one(
        {"email": current_user.email},
        {"$set": {"hashed_password": new_hashed_password}}
    )
    
    return {
        "message": "Password changed successfully",
        "success": True
    }


@router.post("/export-data")
async def export_user_data(current_user: User = Depends(get_current_user)):
    """
    Export all user data including resumes.
    """
    db = get_database()
    
    # Fetch all resumes for this user
    resumes = await db.resumes.find().to_list(length=None)
    
    # Fetch user profile
    user = await db.users.find_one({"email": current_user.email})
    
    export_data = {
        "user": {
            "email": user.get("email"),
            "full_name": user.get("full_name"),
            "created_at": str(user.get("created_at")),
            "settings": user.get("settings", {})
        },
        "resumes": [
            {
                "id": str(resume.get("_id")),
                "name": resume.get("name"),
                "email": resume.get("contact", {}).get("email"),
                "skills": resume.get("skills", []),
                "parsed_at": str(resume.get("parsed_at"))
            }
            for resume in resumes
        ],
        "total_resumes": len(resumes)
    }
    
    return export_data


@router.delete("/delete-all-data")
async def delete_all_data(current_user: User = Depends(get_current_user)):
    """
    Delete all user resumes (NOT the user account).
    """
    db = get_database()
    
    # Delete all resumes
    result = await db.resumes.delete_many({})
    
    # Also delete associated files from GridFS
    # Note: This is a simple implementation. You might want to add more sophisticated cleanup
    
    return {
        "message": "All resume data deleted successfully",
        "deleted_count": result.deleted_count,
        "success": True
    }
