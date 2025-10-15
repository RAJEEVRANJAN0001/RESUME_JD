"""
Analytics Router - Comprehensive metrics and insights
"""
from fastapi import APIRouter, Depends, Query, Body
from app.models import User, JobDescription
from app.dependencies import get_current_user
from app.services.analytics_service import analytics_service
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class MatchAllRequest(BaseModel):
    job_description: str
    required_skills: list[str] = []


@router.get("/dashboard")
async def get_analytics_dashboard(
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive analytics dashboard.
    
    **Returns:**
    - Overview metrics (total resumes, avg match score, success rate)
    - Top skills analysis
    - Education distribution
    - Certification trends
    - Match score distribution
    - Time series data (daily uploads)
    - Top candidates
    - Experience distribution
    
    **Query Parameters:**
    - days: Number of days to look back (default: 30, max: 365)
    """
    stats = await analytics_service.get_dashboard_stats(days=days)
    return stats


@router.get("/skills/trends")
async def get_skill_trends(
    days: int = Query(90, description="Analysis period in days", ge=30, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Get trending skills analysis.
    
    **Returns:**
    - Skills trends across different time periods
    - Trending up skills (showing growth)
    - Skill frequency by period
    
    **Query Parameters:**
    - days: Analysis period in days (default: 90)
    """
    trends = await analytics_service.get_skill_trends(days=days)
    return trends


@router.get("/matching/insights")
async def get_matching_insights(
    current_user: User = Depends(get_current_user)
):
    """
    Get matching algorithm performance insights.
    
    **Returns:**
    - Total matches analyzed
    - Quality distribution (high/medium/low)
    - Matching effectiveness metrics
    - Skills and experience matching insights
    """
    insights = await analytics_service.get_matching_insights()
    return insights


@router.get("/export/report")
async def export_analytics_report(
    format: str = Query("json", description="Export format (json, csv)"),
    current_user: User = Depends(get_current_user)
):
    """
    Export comprehensive analytics report.
    
    **Returns:**
    - Complete analytics report with all metrics
    - Dashboard metrics
    - Skill trends
    - Matching insights
    - Executive summary
    
    **Query Parameters:**
    - format: Export format (default: json)
    """
    report = await analytics_service.export_analytics_report(format=format)
    return {
        "success": True,
        "report": report,
        "download_ready": True
    }


@router.get("/metrics/overview")
async def get_metrics_overview(
    current_user: User = Depends(get_current_user)
):
    """
    Get quick metrics overview for dashboard cards.
    
    **Returns:**
    - Total analyzed resumes
    - Average match score
    - Top 5 skills
    - Average processing time
    """
    stats = await analytics_service.get_dashboard_stats(days=30)
    
    return {
        "total_analyzed": stats["overview"]["total_resumes"],
        "average_match": stats["overview"]["avg_match_score"],
        "top_skills": stats["skills"]["top_skills"][:5],
        "processing_time": stats["overview"]["avg_processing_time_ms"],
        "success_rate": stats["overview"]["success_rate"]
    }


@router.post("/match-all")
async def match_all_resumes_with_jd(
    request: MatchAllRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Match ALL resumes in database against a specific job description.
    
    **Request Body:**
    - job_description: The job description text
    - required_skills: List of required skills
    
    **Returns:**
    - matched_candidates: List of all resumes with match scores ranked highest to lowest
    - best_match: Highest scoring candidate
    - worst_match: Lowest scoring candidate
    - average_score: Average match score across all resumes
    """
    result = await analytics_service.match_all_resumes_with_jd(
        job_description=request.job_description,
        required_skills=request.required_skills
    )
    return result
