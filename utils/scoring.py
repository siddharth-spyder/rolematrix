"""
Scoring utility for interview confidence calculation.
"""
from typing import List, Tuple
from .skill_extractor import get_matched_skills, get_missing_skills


def calculate_confidence_score(resume_skills: List[str], jd_skills: List[str]) -> dict:
    """
    Calculate interview confidence score based on skill matching.
    
    Args:
        resume_skills: List of skills extracted from resume
        jd_skills: List of required skills from job description
        
    Returns:
        Dictionary with confidence score and recommendation
    """
    if not jd_skills:
        return {
            "confidence": 0,
            "recommendation": "Not now",
            "matched_skills": [],
            "missing_skills": [],
            "coverage": 0.0
        }
    
    matched = get_matched_skills(resume_skills, jd_skills)
    missing = get_missing_skills(resume_skills, jd_skills)
    
    # Calculate coverage
    coverage = len(matched) / len(jd_skills)
    confidence = round(coverage * 100)
    
    # Determine recommendation
    if confidence >= 75:
        recommendation = "Interview"
    elif confidence >= 55:
        recommendation = "Maybe"
    else:
        recommendation = "Not now"
    
    return {
        "confidence": confidence,
        "recommendation": recommendation,
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage": round(coverage, 2),
        "matched_count": len(matched),
        "total_jd_skills": len(jd_skills)
    }
