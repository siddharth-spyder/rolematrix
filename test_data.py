"""
Test script to verify data files and basic functionality.
"""
import json
from pathlib import Path

def test_skills_lexicon():
    """Test loading skills lexicon."""
    print("Testing skills_lexicon.json...")
    try:
        with open('data/skills_lexicon.json', 'r') as f:
            data = json.load(f)
            skills = data.get('skills', [])
            print(f"✅ Loaded {len(skills)} skills")
            print(f"Sample skills: {', '.join(skills[:10])}")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_role_library():
    """Test loading role library."""
    print("\nTesting role_library.json...")
    try:
        with open('data/role_library.json', 'r') as f:
            data = json.load(f)
            roles = data.get('roles', [])
            print(f"✅ Loaded {len(roles)} roles")
            for role in roles[:3]:
                print(f"  - {role['role_name']}: {len(role['required_skills'])} required, {len(role['preferred_skills'])} preferred")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_skill_extraction():
    """Test skill extraction logic."""
    print("\nTesting skill extraction...")
    try:
        from utils.skill_extractor import extract_skills
        
        with open('data/skills_lexicon.json', 'r') as f:
            skills_lexicon = json.load(f)['skills']
        
        test_text = """
        I am a software engineer with 5 years of experience in Python, JavaScript, and React.
        I have worked with AWS, Docker, and Kubernetes. I'm proficient in SQL and MongoDB.
        My skills include Machine Learning, TensorFlow, and Data Analysis.
        """
        
        extracted = extract_skills(test_text, skills_lexicon)
        print(f"✅ Extracted {len(extracted)} skills from test text")
        print(f"Skills found: {', '.join(extracted)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scoring():
    """Test confidence scoring."""
    print("\nTesting confidence scoring...")
    try:
        from utils.scoring import calculate_confidence_score
        
        resume_skills = ["Python", "JavaScript", "React", "SQL", "Git"]
        jd_skills = ["Python", "JavaScript", "React", "Docker", "AWS"]
        
        result = calculate_confidence_score(resume_skills, jd_skills)
        print(f"✅ Confidence: {result['confidence']}%")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Matched: {', '.join(result['matched_skills'])}")
        print(f"Missing: {', '.join(result['missing_skills'])}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_role_matching():
    """Test alternate role matching."""
    print("\nTesting alternate role matching...")
    try:
        from utils.role_matcher import find_alternate_roles
        
        with open('data/role_library.json', 'r') as f:
            roles = json.load(f)['roles']
        
        resume_skills = ["Python", "SQL", "Machine Learning", "Pandas", "NumPy", "TensorFlow"]
        
        matches = find_alternate_roles(resume_skills, roles, min_score=0.5, top_n=3)
        print(f"✅ Found {len(matches)} matching roles")
        for match in matches:
            print(f"  - {match['role_name']}: {match['role_score']}% match")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("ROLE MATRIX - DATA VALIDATION TEST")
    print("=" * 60)
    
    tests = [
        test_skills_lexicon,
        test_role_library,
        test_skill_extraction,
        test_scoring,
        test_role_matching
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ All tests passed! The application is ready to use.")
        print("\nTo run the application:")
        print("  streamlit run app.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
