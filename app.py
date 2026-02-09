"""
Role Matrix - Resume Screening Application
"""
import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime

# Import utility modules
from utils.file_loader import extract_text_from_file
from utils.skill_extractor import extract_skills
from utils.jd_parser import parse_job_description
from utils.scoring import calculate_confidence_score
from utils.role_matcher import get_role_suggestions_for_candidate


# Set page config
st.set_page_config(
    page_title="Role Matrix - Resume Screening",
    page_icon="📋",
    layout="wide"
)

# Constants
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "outputs" / "profiles"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@st.cache_data
def load_skills_lexicon():
    """Load skills lexicon from JSON file."""
    lexicon_path = DATA_DIR / "skills_lexicon.json"
    try:
        with open(lexicon_path, 'r') as f:
            data = json.load(f)
            return data.get("skills", [])
    except Exception as e:
        st.error(f"Error loading skills lexicon: {e}")
        return []


@st.cache_data
def load_role_library():
    """Load role library from JSON file."""
    library_path = DATA_DIR / "role_library.json"
    try:
        with open(library_path, 'r') as f:
            data = json.load(f)
            return data.get("roles", [])
    except Exception as e:
        st.error(f"Error loading role library: {e}")
        return []


def save_candidate_profile(candidate_data: dict, filename: str):
    """Save candidate profile to JSON file."""
    try:
        # Create a safe filename
        safe_filename = filename.replace(" ", "_").replace(".pdf", "").replace(".docx", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"{safe_filename}_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(candidate_data, f, indent=2)
        
        return str(output_file)
    except Exception as e:
        st.error(f"Error saving candidate profile: {e}")
        return None


def process_resume(uploaded_file, skills_lexicon, jd_skills, roles_library):
    """Process a single resume file."""
    try:
        # Save uploaded file temporarily
        suffix = Path(uploaded_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Extract text
        file_ext = suffix.lstrip('.')
        raw_text = extract_text_from_file(tmp_path, file_ext)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        if not raw_text:
            return None
        
        # Extract skills
        resume_skills = extract_skills(raw_text, skills_lexicon)
        
        # Calculate confidence score
        scoring_result = calculate_confidence_score(resume_skills, jd_skills)
        
        # Get alternate role suggestions
        alternate_roles = get_role_suggestions_for_candidate(
            scoring_result["confidence"],
            resume_skills,
            roles_library
        )
        
        # Create candidate profile
        candidate_profile = {
            "candidate_id": f"candidate_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}",
            "filename": uploaded_file.name,
            "timestamp": datetime.now().isoformat(),
            "raw_text": raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text,  # Truncate for storage
            "raw_text_length": len(raw_text),
            "extracted_skills": resume_skills,
            "total_skills": len(resume_skills),
            "jd_match": scoring_result,
            "alternate_roles": alternate_roles
        }
        
        # Save profile
        save_candidate_profile(candidate_profile, uploaded_file.name)
        
        return candidate_profile
        
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {e}")
        return None


def main():
    """Main application function."""
    
    # Header
    st.title("📋 Role Matrix - Resume Screening Tool")
    st.markdown("Upload resumes and job descriptions to screen candidates efficiently.")
    
    # Load data
    with st.spinner("Loading skills lexicon and role library..."):
        skills_lexicon = load_skills_lexicon()
        roles_library = load_role_library()
    
    if not skills_lexicon:
        st.error("Failed to load skills lexicon. Please check data/skills_lexicon.json")
        return
    
    if not roles_library:
        st.error("Failed to load role library. Please check data/role_library.json")
        return
    
    st.success(f"✅ Loaded {len(skills_lexicon)} skills and {len(roles_library)} roles")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.write(f"**Skills in Lexicon:** {len(skills_lexicon)}")
        st.write(f"**Roles in Library:** {len(roles_library)}")
        st.markdown("---")
        st.write("**Confidence Thresholds:**")
        st.write("- ✅ Interview: ≥75%")
        st.write("- ⚠️ Maybe: 55-74%")
        st.write("- ❌ Not now: <55%")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload PDF or DOCX files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Select multiple resume files to process"
        )
    
    with col2:
        st.subheader("📝 Job Description")
        jd_text = st.text_area(
            "Paste job description here",
            height=200,
            placeholder="Enter the job description text..."
        )
    
    # Process button
    st.markdown("---")
    
    if st.button("🚀 Run Screening", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("⚠️ Please upload at least one resume file.")
            return
        
        if not jd_text.strip():
            st.warning("⚠️ Please provide a job description.")
            return
        
        # Parse job description
        with st.spinner("Parsing job description..."):
            jd_data = parse_job_description(jd_text, skills_lexicon)
            jd_skills = jd_data["jd_required_skills"]
        
        st.info(f"📊 Extracted {len(jd_skills)} skills from job description")
        
        if jd_skills:
            with st.expander("View JD Skills"):
                st.write(", ".join(jd_skills))
        
        # Process resumes
        st.markdown("---")
        st.subheader("🔍 Processing Resumes...")
        
        results = []
        progress_bar = st.progress(0)
        
        for idx, uploaded_file in enumerate(uploaded_files):
            with st.spinner(f"Processing {uploaded_file.name}..."):
                candidate_profile = process_resume(
                    uploaded_file,
                    skills_lexicon,
                    jd_skills,
                    roles_library
                )
                
                if candidate_profile:
                    results.append(candidate_profile)
                    
                    # Show preview
                    with st.expander(f"Preview: {uploaded_file.name}"):
                        st.write(f"**Text Preview:** {candidate_profile['raw_text'][:500]}...")
                        st.write(f"**Total Skills Found:** {len(candidate_profile['extracted_skills'])}")
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        st.success(f"✅ Processed {len(results)} out of {len(uploaded_files)} resumes")
        
        # Display results
        if results:
            st.markdown("---")
            st.subheader("📊 Screening Results")
            
            # Create results table
            table_data = []
            for candidate in results:
                jd_match = candidate["jd_match"]
                
                row = {
                    "Candidate": candidate["filename"],
                    "Confidence": f"{jd_match['confidence']}%",
                    "Recommendation": jd_match["recommendation"],
                    "Matched Skills": ", ".join(jd_match["matched_skills"][:5]) + ("..." if len(jd_match["matched_skills"]) > 5 else ""),
                    "Missing Skills": ", ".join(jd_match["missing_skills"][:3]) + ("..." if len(jd_match["missing_skills"]) > 3 else ""),
                    "Total Skills": candidate["total_skills"]
                }
                table_data.append(row)
            
            df = pd.DataFrame(table_data)
            
            # Color code by recommendation
            def highlight_recommendation(row):
                if row["Recommendation"] == "Interview":
                    return ['background-color: #d4edda'] * len(row)
                elif row["Recommendation"] == "Maybe":
                    return ['background-color: #fff3cd'] * len(row)
                else:
                    return ['background-color: #f8d7da'] * len(row)
            
            styled_df = df.style.apply(highlight_recommendation, axis=1)
            st.dataframe(styled_df, use_container_width=True)
            
            # Show detailed results
            st.markdown("---")
            st.subheader("📋 Detailed Candidate Profiles")
            
            for candidate in results:
                with st.expander(f"🔍 {candidate['filename']} - {candidate['jd_match']['recommendation']}"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.write("**Screening Results:**")
                        st.write(f"- Confidence: {candidate['jd_match']['confidence']}%")
                        st.write(f"- Recommendation: {candidate['jd_match']['recommendation']}")
                        st.write(f"- Matched Skills: {candidate['jd_match']['matched_count']}/{candidate['jd_match']['total_jd_skills']}")
                        
                        st.write("\n**Matched JD Skills:**")
                        st.write(", ".join(candidate['jd_match']['matched_skills']) if candidate['jd_match']['matched_skills'] else "None")
                        
                        st.write("\n**Missing JD Skills:**")
                        st.write(", ".join(candidate['jd_match']['missing_skills']) if candidate['jd_match']['missing_skills'] else "None")
                    
                    with col_b:
                        st.write("**All Extracted Skills:**")
                        st.write(", ".join(candidate['extracted_skills']) if candidate['extracted_skills'] else "None")
                        
                        if candidate['alternate_roles']:
                            st.write("\n**🎯 Alternate Role Suggestions:**")
                            for role in candidate['alternate_roles']:
                                st.write(f"- **{role['role_name']}** ({role['role_score']}% match)")
                                st.write(f"  Matched: {', '.join(role['matched_skills'][:5])}")


if __name__ == "__main__":
    main()
