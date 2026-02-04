"""
Skill extractor utility using dictionary matching.
"""
from typing import List, Set
import re


def extract_skills(text: str, skills_lexicon: List[str]) -> List[str]:
    """
    Extract skills from text using case-insensitive dictionary matching.
    
    Args:
        text: Input text (resume or job description)
        skills_lexicon: List of skills to match against
        
    Returns:
        List of unique matched skills
    """
    if not text or not skills_lexicon:
        return []
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Set to store unique matched skills
    matched_skills = set()
    
    for skill in skills_lexicon:
        skill_lower = skill.lower()
        
        # Create a regex pattern for word boundary matching
        # This ensures we match whole words/phrases, not substrings
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        
        if re.search(pattern, text_lower):
            matched_skills.add(skill)  # Add original case from lexicon
    
    # Return sorted list for consistency
    return sorted(list(matched_skills))


def get_skill_match_count(resume_skills: List[str], target_skills: List[str]) -> int:
    """
    Count how many skills from target_skills are present in resume_skills.
    
    Args:
        resume_skills: List of skills extracted from resume
        target_skills: List of target skills to match
        
    Returns:
        Number of matched skills
    """
    resume_skills_set = set(s.lower() for s in resume_skills)
    target_skills_set = set(s.lower() for s in target_skills)
    
    matched = resume_skills_set.intersection(target_skills_set)
    return len(matched)


def get_matched_skills(resume_skills: List[str], target_skills: List[str]) -> List[str]:
    """
    Get the list of skills that match between resume and target.
    
    Args:
        resume_skills: List of skills extracted from resume
        target_skills: List of target skills to match
        
    Returns:
        List of matched skills (in original case from resume)
    """
    resume_skills_lower = {s.lower(): s for s in resume_skills}
    target_skills_lower = set(s.lower() for s in target_skills)
    
    matched = []
    for skill_lower in target_skills_lower:
        if skill_lower in resume_skills_lower:
            matched.append(resume_skills_lower[skill_lower])
    
    return sorted(matched)


def get_missing_skills(resume_skills: List[str], target_skills: List[str]) -> List[str]:
    """
    Get the list of target skills that are missing from resume.
    
    Args:
        resume_skills: List of skills extracted from resume
        target_skills: List of target skills to match
        
    Returns:
        List of missing skills
    """
    resume_skills_lower = set(s.lower() for s in resume_skills)
    
    missing = []
    for skill in target_skills:
        if skill.lower() not in resume_skills_lower:
            missing.append(skill)
    
    return sorted(missing)
