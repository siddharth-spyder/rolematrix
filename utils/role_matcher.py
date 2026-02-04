"""
Alternate role matcher utility.
"""
from typing import List, Dict
from .skill_extractor import get_matched_skills


def find_alternate_roles(
    resume_skills: List[str],
    roles_library: List[dict],
    min_score: float = 0.5,
    top_n: int = 3
) -> List[dict]:
    """
    Find alternate role suggestions based on resume skills.
    
    Args:
        resume_skills: List of skills extracted from resume
        roles_library: List of role definitions from role_library.json
        min_score: Minimum score threshold (default: 0.5)
        top_n: Number of top roles to return (default: 3)
        
    Returns:
        List of suggested roles with scores and matched skills
    """
    if not resume_skills or not roles_library:
        return []
    
    role_matches = []
    
    for role in roles_library:
        required_skills = role.get("required_skills", [])
        
        if not required_skills:
            continue
        
        # Calculate match score
        matched_req = get_matched_skills(resume_skills, required_skills)
        role_score = len(matched_req) / len(required_skills)
        
        # Only include roles meeting minimum threshold
        if role_score >= min_score:
            role_matches.append({
                "role_id": role.get("role_id", ""),
                "role_name": role.get("role_name", ""),
                "role_score": round(role_score * 100),
                "matched_skills": matched_req,
                "matched_count": len(matched_req),
                "total_required": len(required_skills),
                "coverage": round(role_score, 2)
            })
    
    # Sort by role_score descending
    role_matches.sort(key=lambda x: x["role_score"], reverse=True)
    
    # Return top N roles
    return role_matches[:top_n]


def get_role_suggestions_for_candidate(
    confidence: int,
    resume_skills: List[str],
    roles_library: List[dict]
) -> List[dict]:
    """
    Get role suggestions if confidence is below threshold.
    
    Args:
        confidence: Interview confidence score
        resume_skills: List of skills extracted from resume
        roles_library: List of role definitions
        
    Returns:
        List of suggested roles (empty if confidence >= 55)
    """
    if confidence >= 55:
        return []
    
    return find_alternate_roles(resume_skills, roles_library)
