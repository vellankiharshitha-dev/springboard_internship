# Resume Analyzer Project - Milestone 1

## Setup Steps Completed
- Python 3.11 installed
- Virtual environment created: venv
- Required libraries installed: streamlit, langchain, selenium, PyPDF2, python-docx, bcrypt, sqlite-utils
- Project folders created:
  - backend/
  - frontend/
  - utils/
  - data/
- app.py created
- _init_.py files added
- Environment ready for development

## Next Steps
Proceed to Task 2 (Database Schema Design)

## Database Design (SQLite)

- Database file: data/app.db

### Tables

1. users
   - id (INTEGER, PK, AUTOINCREMENT)
   - full_name (TEXT, NOT NULL)
   - email (TEXT, UNIQUE, NOT NULL)
   - password_hash (TEXT, NOT NULL)
   - registration_date (TEXT, NOT NULL)
   - resume_path (TEXT, NULL)

2. resume_analysis
   - id (INTEGER, PK, AUTOINCREMENT)
   - user_id (INTEGER, FK → users.id)
   - extracted_text (TEXT, NOT NULL)
   - analysis_scores (TEXT)
   - strengths (TEXT)
   - weaknesses (TEXT)
   - identified_skills (TEXT)
   - recommended_skills (TEXT)
   - analysis_timestamp (TEXT, NOT NULL)

3. job_recommendations
   - id (INTEGER, PK, AUTOINCREMENT)
   - user_id (INTEGER, FK → users.id)
   - job_title (TEXT)
   - company_name (TEXT)
   - location (TEXT)
   - job_description (TEXT)
   - job_url (TEXT)
   - match_percentage (REAL)
   - scraping_date (TEXT)