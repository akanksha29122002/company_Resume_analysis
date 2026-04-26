# AI Resume Analyzer and Company Knowledge Bank

AI Resume Analyzer is a Streamlit web app where companies upload requirement/company documents and candidates upload resumes. Both types of data are stored as active records for about 6 months. The system automatically compares active resumes with active company requirements and tells the company which candidates are ideal matches, including their potential and recommendation reason.

HR can receive resumes through a Google Form, Apps Script can forward candidate data to the intake API, and Pinecone can store both candidate resume vectors and company document vectors such as establishment details, growth milestones, departments, projects, technologies, culture, and requirement history.

## Features

- Upload resume as PDF
- Extract and preview resume text
- Detect important resume sections
- Identify technical and soft skills
- Compare resume keywords with job description
- Generate ATS score, strengths, weaknesses, and suggestions
- Store company candidate records for 6 months
- Store company documents and requirements for 6 months
- Rank active candidates for new company requirements
- Show candidate potential: Ideal Match, Strong Potential, Moderate Potential, or Low Match
- Store company establishment and growth records
- Search company requirements and historical context
- Include company knowledge while ranking candidates
- Optional Pinecone vector database integration
- RAG-style retrieval from company documents and candidate resumes
- FastAPI endpoints for resume intake, company document intake, and ideal-match calculation
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
- Candidate Upload: candidates or HR upload resumes.
- Company Documents: companies upload requirement PDFs or paste company details.
- Auto Match: automatically shortlist ideal candidates and show their potential.
- Stored Data: view active candidate resumes and company documents.
- Apps Script Setup: instructions for automatic Google Form intake and automatic RAG match calculation.

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

These records can be synced to Pinecone with metadata type `company_knowledge`. During role matching, the app retrieves relevant company context, augments the requirement, retrieves matching resumes, and generates an explainable recommendation. This is the project RAG flow.

## Google Apps Script Intake

1. Create a Candidate Google Form with fields: `Name`, `Email`, `Phone`, `Role Applied`, `Resume Upload`, `Resume Text`, and `Job Description`.
2. Create a Company Google Form with fields: `Company Name`, `Record Type`, `Title`, `Date or Period`, `Details`, `Tags`, and `Company Document Upload`.
3. Open Extensions -> Apps Script.
4. Paste the code from `apps_script/Code.gs`.
5. Replace `API_BASE_URL` and `INTAKE_TOKEN`.
6. Add installable triggers for `onCandidateFormSubmit` and `onCompanyFormSubmit`.
7. Use the Google Sheet menu `Resume RAG -> Calculate ideal matches` for automatic match calculation.

## Deployment

The dashboard can be deployed on Streamlit Community Cloud. The intake webhook API can be deployed on Render or another platform that supports FastAPI.

More deployment notes are available in `docs/DEPLOYMENT.md`.

## Future Scope

- Add transformer embeddings for deeper semantic similarity.
- Export analysis reports as PDF.
- Add resume bullet rewriting suggestions.
- Add email alerts when a strong candidate matches a new requirement.
