"""
Job Description parser utility.
"""
from typing import List
from .skill_extractor import extract_skills


def parse_job_description(jd_text: str, skills_lexicon: List[str]) -> dict:
    """
    Parse job description and extract required skills.
    
    Args:
        jd_text: Job description text
        skills_lexicon: List of skills to match against
        
    Returns:
        Dictionary with extracted JD information
    """
    jd_skills = extract_skills(jd_text, skills_lexicon)
    
    return {
        "jd_text": jd_text,
        "jd_required_skills": jd_skills,
        "total_jd_skills": len(jd_skills)
    }
