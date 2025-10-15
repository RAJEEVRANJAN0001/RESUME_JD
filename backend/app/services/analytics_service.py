"""
Analytics Service for Resume Screening Metrics and Insights
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app.database import get_database
from bson import ObjectId
import statistics
from collections import Counter, defaultdict


class AnalyticsService:
    """Comprehensive analytics for resume screening process."""
    
    async def get_dashboard_stats(
        self, 
        days: int = 30,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive dashboard statistics.
        
        Args:
            days: Number of days to look back (default 30)
            user_id: Optional user ID to filter by user
            
        Returns:
            Dictionary with comprehensive analytics
        """
        db = get_database()
        
        # Calculate date range
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query - make it flexible to handle resumes without parsed_at
        query = {}
        if user_id:
            query["user_id"] = user_id
        
        # Try to filter by date if parsed_at exists, otherwise get all
        resumes_with_date = await db.resumes.find({
            **query,
            "parsed_at": {"$gte": start_date}
        }).to_list(length=10000)
        
        # If no resumes with date filter, try without date filter (for resumes without parsed_at)
        if not resumes_with_date:
            resumes = await db.resumes.find(query).to_list(length=10000)
        else:
            resumes = resumes_with_date
        
        if not resumes:
            return self._empty_stats()
        
        # Calculate metrics
        total_resumes = len(resumes)
        
        # Match scores analysis
        match_scores = [r.get("match_score", 0) for r in resumes if r.get("match_score")]
        avg_match_score = statistics.mean(match_scores) if match_scores else 0
        median_match_score = statistics.median(match_scores) if match_scores else 0
        
        # Skills analysis
        all_skills = []
        for resume in resumes:
            all_skills.extend(resume.get("skills", []))
        
        skill_counter = Counter(all_skills)
        top_skills = [
            {"skill": skill, "count": count, "percentage": (count / total_resumes) * 100}
            for skill, count in skill_counter.most_common(20)
        ]
        
        # Experience analysis
        experience_years = []
        for resume in resumes:
            years = self._calculate_total_experience(resume.get("experiences", []))
            if years > 0:
                experience_years.append(years)
        
        avg_experience = statistics.mean(experience_years) if experience_years else 0
        
        # Education analysis
        education_levels = []
        for resume in resumes:
            for edu in resume.get("education", []):
                degree = edu.get("degree", "").lower()
                if "phd" in degree or "doctorate" in degree:
                    education_levels.append("PhD")
                elif "master" in degree:
                    education_levels.append("Master's")
                elif "bachelor" in degree:
                    education_levels.append("Bachelor's")
                else:
                    education_levels.append("Other")
        
        education_distribution = dict(Counter(education_levels))
        
        # Processing time analysis (if available)
        processing_times = [
            r.get("processing_time_ms", 0) for r in resumes 
            if r.get("processing_time_ms")
        ]
        avg_processing_time = statistics.mean(processing_times) if processing_times else 0
        
        # Time series data (daily resume uploads)
        daily_uploads = defaultdict(int)
        for resume in resumes:
            # Only add to time series if parsed_at exists
            if "parsed_at" in resume and resume["parsed_at"]:
                date_key = resume["parsed_at"].strftime("%Y-%m-%d")
                daily_uploads[date_key] += 1
        
        time_series = sorted([
            {"date": date, "count": count}
            for date, count in daily_uploads.items()
        ], key=lambda x: x["date"])
        
        # Match score distribution
        score_ranges = {
            "0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0
        }
        for score in match_scores:
            if score < 20:
                score_ranges["0-20"] += 1
            elif score < 40:
                score_ranges["20-40"] += 1
            elif score < 60:
                score_ranges["40-60"] += 1
            elif score < 80:
                score_ranges["60-80"] += 1
            else:
                score_ranges["80-100"] += 1
        
        # All candidates (sorted by match score if available, otherwise by name)
        # Include ALL resumes, even without match scores
        all_candidates_sorted = sorted(
            resumes,
            key=lambda x: (x.get("match_score") or 0, x.get("name", "")),
            reverse=True
        )
        
        top_candidates_data = [
            {
                "id": str(r["_id"]),
                "name": r.get("name", "Unknown"),
                "match_score": r.get("match_score", 0),  # Default to 0 if no match score
                "skills": r.get("skills", [])[:5],
                "experience_years": self._calculate_total_experience(r.get("experiences", []))
            }
            for r in all_candidates_sorted  # Return ALL candidates, not just top 10
        ]
        
        # Certification analysis
        all_certifications = []
        for resume in resumes:
            certs = resume.get("certifications", [])
            if isinstance(certs, list):
                for cert in certs:
                    if isinstance(cert, dict):
                        all_certifications.append(cert.get("name", "Unknown"))
                    elif isinstance(cert, str):
                        all_certifications.append(cert)
        
        cert_counter = Counter(all_certifications)
        top_certifications = [
            {"name": cert, "count": count}
            for cert, count in cert_counter.most_common(10)
        ]
        
        # Success rate (resumes with match score > 70)
        successful_matches = len([s for s in match_scores if s >= 70])
        success_rate = (successful_matches / len(match_scores) * 100) if match_scores else 0
        
        return {
            "overview": {
                "total_resumes": total_resumes,
                "avg_match_score": round(avg_match_score, 2),
                "median_match_score": round(median_match_score, 2),
                "success_rate": round(success_rate, 2),
                "avg_experience_years": round(avg_experience, 1),
                "avg_processing_time_ms": round(avg_processing_time, 0),
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": datetime.utcnow().isoformat(),
                    "days": days
                }
            },
            "skills": {
                "top_skills": top_skills,
                "total_unique_skills": len(skill_counter),
                "avg_skills_per_resume": round(len(all_skills) / total_resumes, 1) if total_resumes else 0
            },
            "education": {
                "distribution": education_distribution,
                "total_candidates": len(education_levels)
            },
            "certifications": {
                "top_certifications": top_certifications,
                "total_certified_candidates": len([r for r in resumes if r.get("certifications")])
            },
            "match_scores": {
                "distribution": score_ranges,
                "scores": match_scores[:100],  # Limit for performance
                "quartiles": {
                    "q1": round(statistics.quantiles(match_scores, n=4)[0], 2) if len(match_scores) >= 4 else 0,
                    "q2": round(median_match_score, 2),
                    "q3": round(statistics.quantiles(match_scores, n=4)[2], 2) if len(match_scores) >= 4 else 0
                } if match_scores else {"q1": 0, "q2": 0, "q3": 0}
            },
            "time_series": time_series,
            "top_candidates": top_candidates_data,
            "experience_distribution": self._get_experience_distribution(experience_years)
        }
    
    async def get_skill_trends(self, days: int = 90) -> Dict[str, Any]:
        """Get trending skills over time."""
        db = get_database()
        
        # Get resumes from different time periods
        now = datetime.utcnow()
        periods = {
            "current": (now - timedelta(days=30), now),
            "previous": (now - timedelta(days=60), now - timedelta(days=30)),
            "older": (now - timedelta(days=90), now - timedelta(days=60))
        }
        
        trends = {}
        for period_name, (start, end) in periods.items():
            resumes = await db.resumes.find({
                "parsed_at": {"$gte": start, "$lt": end}
            }).to_list(length=10000)
            
            skills = []
            for resume in resumes:
                skills.extend(resume.get("skills", []))
            
            skill_counts = Counter(skills)
            trends[period_name] = dict(skill_counts.most_common(20))
        
        # Calculate trending (increasing skills)
        trending_up = []
        if trends.get("current") and trends.get("previous"):
            for skill in trends["current"]:
                current_count = trends["current"][skill]
                previous_count = trends["previous"].get(skill, 0)
                if previous_count > 0:
                    growth = ((current_count - previous_count) / previous_count) * 100
                    if growth > 20:  # 20% growth threshold
                        trending_up.append({
                            "skill": skill,
                            "current_count": current_count,
                            "previous_count": previous_count,
                            "growth_percentage": round(growth, 1)
                        })
        
        trending_up.sort(key=lambda x: x["growth_percentage"], reverse=True)
        
        return {
            "trends": trends,
            "trending_up": trending_up[:10],
            "analysis_period_days": days
        }
    
    async def get_matching_insights(self) -> Dict[str, Any]:
        """Get insights on matching algorithm performance."""
        db = get_database()
        
        # Get all resumes with match scores
        resumes = await db.resumes.find({
            "match_score": {"$exists": True}
        }).to_list(length=10000)
        
        if not resumes:
            return {
                "total_matches": 0,
                "insights": []
            }
        
        # Analyze match quality
        high_quality = [r for r in resumes if r.get("match_score", 0) >= 80]
        medium_quality = [r for r in resumes if 60 <= r.get("match_score", 0) < 80]
        low_quality = [r for r in resumes if r.get("match_score", 0) < 60]
        
        insights = []
        
        # Skills matching effectiveness
        skills_matched_avg = []
        for resume in resumes:
            details = resume.get("match_details", {})
            if details.get("matched_skills"):
                skills_matched_avg.append(len(details["matched_skills"]))
        
        if skills_matched_avg:
            insights.append({
                "metric": "Skills Matching",
                "average_matched": round(statistics.mean(skills_matched_avg), 1),
                "effectiveness": "High" if statistics.mean(skills_matched_avg) > 5 else "Medium"
            })
        
        # Experience matching
        exp_scores = [r.get("match_details", {}).get("breakdown", {}).get("experience_score", 0) for r in resumes]
        exp_scores = [s for s in exp_scores if s > 0]
        
        if exp_scores:
            insights.append({
                "metric": "Experience Matching",
                "average_score": round(statistics.mean(exp_scores), 1),
                "effectiveness": "High" if statistics.mean(exp_scores) > 70 else "Medium"
            })
        
        return {
            "total_matches": len(resumes),
            "quality_distribution": {
                "high_quality": len(high_quality),
                "medium_quality": len(medium_quality),
                "low_quality": len(low_quality)
            },
            "quality_percentages": {
                "high": round(len(high_quality) / len(resumes) * 100, 1),
                "medium": round(len(medium_quality) / len(resumes) * 100, 1),
                "low": round(len(low_quality) / len(resumes) * 100, 1)
            },
            "insights": insights
        }
    
    async def export_analytics_report(self, format: str = "json") -> Dict[str, Any]:
        """Export comprehensive analytics report."""
        dashboard = await self.get_dashboard_stats(days=90)
        trends = await self.get_skill_trends(days=90)
        insights = await self.get_matching_insights()
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "report_period": "Last 90 Days",
            "dashboard_metrics": dashboard,
            "skill_trends": trends,
            "matching_insights": insights,
            "summary": {
                "total_resumes_analyzed": dashboard["overview"]["total_resumes"],
                "average_match_score": dashboard["overview"]["avg_match_score"],
                "top_skill": dashboard["skills"]["top_skills"][0]["skill"] if dashboard["skills"]["top_skills"] else "N/A",
                "success_rate": dashboard["overview"]["success_rate"]
            }
        }
        
        return report
    
    def _calculate_total_experience(self, experiences: List[Dict]) -> float:
        """Calculate total years of experience from experience list."""
        if not experiences:
            return 0.0
        
        total_months = 0
        for exp in experiences:
            start = exp.get("start_date", "")
            end = exp.get("end_date", "") or "Present"
            
            # Simple calculation (can be enhanced)
            if start:
                # Assume each job is ~2 years if dates unclear
                total_months += 24
        
        return round(total_months / 12, 1)
    
    def _get_experience_distribution(self, experience_years: List[float]) -> Dict[str, int]:
        """Get distribution of experience levels."""
        distribution = {
            "0-2 years": 0,
            "2-5 years": 0,
            "5-10 years": 0,
            "10+ years": 0
        }
        
        for years in experience_years:
            if years < 2:
                distribution["0-2 years"] += 1
            elif years < 5:
                distribution["2-5 years"] += 1
            elif years < 10:
                distribution["5-10 years"] += 1
            else:
                distribution["10+ years"] += 1
        
        return distribution
    
    def _empty_stats(self) -> Dict[str, Any]:
        """Return empty stats structure."""
        return {
            "overview": {
                "total_resumes": 0,
                "avg_match_score": 0,
                "median_match_score": 0,
                "success_rate": 0,
                "avg_experience_years": 0,
                "avg_processing_time_ms": 0
            },
            "skills": {"top_skills": [], "total_unique_skills": 0, "avg_skills_per_resume": 0},
            "education": {"distribution": {}, "total_candidates": 0},
            "certifications": {"top_certifications": [], "total_certified_candidates": 0},
            "match_scores": {"distribution": {}, "scores": [], "quartiles": {"q1": 0, "q2": 0, "q3": 0}},
            "time_series": [],
            "top_candidates": [],
            "experience_distribution": {}
        }
    
    async def match_all_resumes_with_jd(
        self,
        job_description: str,
        required_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Match ALL resumes in the database against a specific job description.
        
        Args:
            job_description: The job description text
            required_skills: List of required skills for the job
            
        Returns:
            Dictionary with matched candidates ranked by score
        """
        from app.models import Resume, JobDescription
        from app.services.enhanced_scoring import enhanced_resume_scorer
        
        db = get_database()
        
        # Get ALL resumes from database
        all_resumes = await db.resumes.find({}).to_list(length=10000)
        
        if not all_resumes:
            return {
                "matched_candidates": [],
                "best_match": None,
                "worst_match": None,
                "average_score": 0,
                "total_analyzed": 0
            }
        
        print(f"🎯 Matching {len(all_resumes)} resumes with job description...")
        
        # Create JobDescription object
        jd = JobDescription(
            description=job_description,
            required_skills=required_skills,
            preferred_skills=[],
            experience_years=None
        )
        
        # Calculate match score for each resume
        matched_results = []
        for resume_doc in all_resumes:
            try:
                # Convert MongoDB document to Resume object
                resume = Resume(**resume_doc)
                
                # Calculate match score using enhanced_resume_scorer
                match_result = enhanced_resume_scorer.calculate_match_score(
                    resume=resume,
                    job_description=jd
                )
                
                matched_results.append({
                    "id": str(resume_doc["_id"]),
                    "name": resume.name,
                    "match_score": match_result["total_score"],
                    "skills": resume.skills[:5],  # Top 5 skills
                    "experience_years": self._calculate_total_experience(resume.experiences),
                    "match_details": match_result  # Full match breakdown
                })
                
                print(f"  ✓ {resume.name}: {match_result['total_score']:.1f}%")
                
            except Exception as e:
                print(f"  ❌ Error matching resume {resume_doc.get('name', 'Unknown')}: {e}")
                continue
        
        # Sort by match score (highest to lowest)
        matched_results.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Calculate statistics
        scores = [r["match_score"] for r in matched_results]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        best_match = matched_results[0] if matched_results else None
        worst_match = matched_results[-1] if matched_results else None
        
        print(f"✅ Matching complete! Best: {best_match['name'] if best_match else 'N/A'} ({best_match['match_score']:.1f}%), Worst: {worst_match['name'] if worst_match else 'N/A'} ({worst_match['match_score']:.1f}%)")
        
        return {
            "matched_candidates": matched_results,
            "best_match": best_match,
            "worst_match": worst_match,
            "average_score": round(avg_score, 2),
            "total_analyzed": len(matched_results)
        }


# Global analytics service instance
analytics_service = AnalyticsService()
