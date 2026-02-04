# Role Matrix - Resume Screening Application

An intelligent resume screening tool that matches candidate skills against job descriptions and provides interview recommendations.

## Features

✅ **Multi-file Resume Upload** - Process multiple PDF/DOCX resumes at once

✅ **Skill Extraction** - Automatically extracts 300+ technical and soft skills

✅ **Job Description Parsing** - Analyzes JD requirements

✅ **Confidence Scoring** - Calculates match percentage

✅ **Interview Recommendations** - Auto-categorizes: Interview, Maybe, Not now

✅ **Alternate Role Suggestions** - Suggests better-fitting roles for low-match candidates

✅ **Candidate Profiles** - Exports structured JSON profiles

✅ **Visual Dashboard** - Color-coded results table

## Setup Instructions

### 1. Navigate to Project Directory
```bash
cd /Users/dhanushmathivanan/dhanush_gwu/gwu_venture_competition/role-matrix/rolematrix
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
rolematrix/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   ├── skills_lexicon.json        # 300+ skills database
│   └── role_library.json          # 15 role definitions
├── utils/
│   ├── __init__.py
│   ├── file_loader.py             # PDF/DOCX text extraction
│   ├── skill_extractor.py         # Dictionary-based skill matching
│   ├── jd_parser.py               # Job description parser
│   ├── scoring.py                 # Confidence calculation
│   └── role_matcher.py            # Alternate role suggestions
├── outputs/
│   └── profiles/                  # Saved candidate JSON profiles
└── venv/                          # Virtual environment
```

## How It Works

### 1. Upload Resumes
- Supports PDF and DOCX formats
- Upload multiple files at once
- Automatic text extraction

### 2. Enter Job Description
- Paste JD text in the text area
- System extracts required skills automatically

### 3. Run Screening
- Click "Run Screening" button
- View real-time processing progress
- See text preview for each resume

### 4. Review Results

**Results Table:**
- 🟢 Green = Interview (≥75% match)
- 🟡 Yellow = Maybe (55-74% match)
- 🔴 Red = Not now (<55% match)

**Detailed Profiles:**
- Matched skills
- Missing skills
- Total skills found
- Alternate role suggestions (for low matches)

### 5. Export Profiles
Candidate profiles are automatically saved to `outputs/profiles/` as JSON files.

## Skills Lexicon

The application includes 300+ skills across:
- **Programming Languages:** Python, Java, JavaScript, C++, Go, Rust, etc.
- **Frameworks:** React, Angular, Django, Flask, Spring Boot, etc.
- **Cloud Platforms:** AWS, Azure, GCP
- **Databases:** MySQL, PostgreSQL, MongoDB, Redis, etc.
- **DevOps Tools:** Docker, Kubernetes, Jenkins, Terraform, etc.
- **Data Science:** Machine Learning, TensorFlow, PyTorch, Pandas, etc.
- **Soft Skills:** Leadership, Communication, Problem Solving, etc.

## Role Library

Pre-configured roles:
1. Full Stack Developer
2. Data Scientist
3. DevOps Engineer
4. Frontend Developer
5. Backend Developer
6. Cloud Architect
7. Data Engineer
8. Machine Learning Engineer
9. Product Manager
10. UI/UX Designer
11. QA Engineer
12. Mobile Developer
13. Cybersecurity Analyst
14. Business Analyst
15. Site Reliability Engineer

## Confidence Scoring

**Formula:**
```
confidence = (matched_skills / total_jd_skills) × 100
```

**Recommendations:**
- **≥75%** → Interview (Strong match)
- **55-74%** → Maybe (Moderate match)
- **<55%** → Not now (Low match, suggests alternate roles)

## Alternate Role Matching

For candidates scoring <55%:
- Checks match against all 15 roles in library
- Requires ≥50% match on required skills
- Returns top 3 best-fit roles
- Shows matched skills for explainability

## Technologies Used

- **Streamlit** - Web interface
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX text extraction
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations
- **Python 3.x** - Core language

## Future Enhancements

- [ ] Natural Language Processing for better skill extraction
- [ ] Weighted scoring (required vs. preferred skills)
- [ ] Resume ranking/sorting
- [ ] Batch export to CSV/Excel
- [ ] Email integration for candidate notifications
- [ ] ATS integration
- [ ] Custom role creation UI
- [ ] Skills synonym matching
- [ ] Experience level detection
- [ ] Education requirement matching

## Troubleshooting

### App won't start
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### JSON loading errors
- Verify `data/skills_lexicon.json` exists
- Verify `data/role_library.json` exists
- Check JSON syntax is valid

### File extraction errors
- Ensure PDF is not password-protected
- Ensure DOCX is not corrupted
- Check file permissions

## License

MIT License - See LICENSE file for details

## Author

- **Siddharth Saravanan**
- **Dhanush Mathivanan**
- **Aswin Balaji Thippa Ramesh**
- **Gowri Sriram Lakshmanan**
- **Barathkumar Anantharaj**

GWU Venture Competition 2026
