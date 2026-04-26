# AI Resume Analyzer and Company Knowledge Bank

AI Resume Analyzer is a Streamlit web app that reads resume PDFs, compares them with job descriptions, and generates ATS-style feedback. The upgraded version also works as a company resume bank and company knowledge base.

HR can receive resumes through a Google Form, Apps Script can forward candidate data to the intake API, active resumes are maintained for 6 months, and recruiters can rank the best candidates for each new role. Pinecone can store both candidate resume vectors and company knowledge records such as establishment details, growth milestones, departments, projects, technologies, culture, and requirement history.

## Features

- Upload resume as PDF
- Extract and preview resume text
- Detect important resume sections
- Identify technical and soft skills
- Compare resume keywords with job description
- Generate ATS score, strengths, weaknesses, and suggestions
- Store company candidate records for 6 months
- Rank active candidates for new company requirements
- Store company establishment and growth records
- Search company requirements and historical context
- Include company knowledge while ranking candidates
- Optional Pinecone vector database integration
- Google Apps Script template for automatic form-based resume intake
- Runs with local fallback when Pinecone is not configured

## Project Structure

```text
.
|-- app.py
|-- api.py
|-- candidate_store.py
|-- company_store.py
|-- resume_analyzer.py
|-- vector_store.py
|-- requirements.txt
|-- sample_job_description.txt
|-- apps_script/
|   `-- Code.gs
|-- README.md
|-- REPORT.md
|-- PRESENTATION_OUTLINE.md
|-- docs/
|   `-- DEPLOYMENT.md
`-- scripts/
    `-- generate_pptx.py
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dashboard Modules

- Single Resume: analyze one candidate resume against a job description.
- Company Intake: add candidates manually or through HR upload.
- Company Growth: store company establishment, milestones, projects, technologies, and requirements.
- Role Matching: shortlist active candidates for a new company requirement.
- Candidate Database: view and export active candidate records.
- Apps Script Setup: instructions for automatic Google Form intake.

## Pinecone Setup

Set these environment variables in your deployment platform:

```text
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=resume-candidates
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
INTAKE_TOKEN=choose_a_secret_token
```

If Pinecone is not configured, the app automatically uses local ranking so the demo still works.

## Company Knowledge Base

The Company Growth tab stores records such as:

- Establishment and founder background
- Year-wise growth milestones
- Departments and teams
- Products, services, and projects
- Technology stack
- Past and current requirements
- Culture and working style

These records can be synced to Pinecone with metadata type `company_knowledge`. During role matching, the app can combine the new requirement with company context so shortlisted candidates fit both the role and the company's direction.

## Google Apps Script Intake

1. Create a Google Form with fields: `Name`, `Email`, `Phone`, `Role Applied`, `Resume Upload`, and optionally `Resume Text`.
2. Link the form to a Google Sheet.
3. Open Extensions -> Apps Script.
4. Paste the code from `apps_script/Code.gs`.
5. Replace `INTAKE_API_URL` and `INTAKE_TOKEN`.
6. Add an installable trigger for `onFormSubmit`.

## Deployment

The dashboard can be deployed on Streamlit Community Cloud. The intake webhook API can be deployed on Render or another platform that supports FastAPI.

More deployment notes are available in `docs/DEPLOYMENT.md`.

## Future Scope

- Add transformer embeddings for deeper semantic similarity.
- Export analysis reports as PDF.
- Add resume bullet rewriting suggestions.
- Add email alerts when a strong candidate matches a new requirement.
