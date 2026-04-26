# Deployment Guide

## Option 1: Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all project files.
3. Open https://share.streamlit.io/.
4. Choose repository `akanksha29122002/company_Resume_analysis`.
5. Choose branch `main`.
6. Set the entry file to `app.py`.
7. Click Deploy.

Recommended custom app URL:

```text
company-resume-analysis
```

The deployed app URL will be:

```text
https://company-resume-analysis.streamlit.app
```

If that custom URL is already taken, Streamlit will ask you to pick another one.

This deploys the recruiter dashboard. For Apps Script webhook intake, deploy `api.py` on Render or another platform that supports FastAPI.

## Option 2: Render

This repository includes `render.yaml`, so the easiest Render path is:

1. Open https://dashboard.render.com/.
2. Choose New -> Blueprint.
3. Connect repository `akanksha29122002/company_Resume_analysis`.
4. Render will detect `render.yaml`.
5. Deploy both services.

For manual dashboard deployment, use:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

For the intake webhook API, use:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

## Option 3: Local Demo

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Pinecone is optional. Without `PINECONE_API_KEY`, the dashboard uses local vector ranking.
- Pinecone stores two kinds of records in the same index: `candidate_resume` and `company_knowledge`.
- Candidate resumes and company documents are active for 183 days, approximately 6 months. Expired records are purged automatically when the app runs.
- Apps Script sends Google Form submissions to the `/ingest` endpoint and writes the generated candidate ID, ATS score, active-until date, and Pinecone sync status back to the Sheet.
- Company establishment, growth, department, technology, and requirement records can be added from the Company Growth tab and synced to Pinecone.

## Environment Variables

```text
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=resume-candidates
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
INTAKE_TOKEN=choose_a_secret_token
```

## Google Form Fields

Use these exact field names so `apps_script/Code.gs` can read responses:

- Name
- Email
- Phone
- Role Applied
- Resume Upload
- Resume Text

## Pinecone Record Design

Candidate resumes are stored with:

- `record_kind`: `candidate_resume`
- candidate name, email, phone, role applied
- upload date and expiry date
- latest score and active status
- resume preview metadata

Company documents and knowledge records are stored with:

- `record_kind`: `company_knowledge`
- company name
- record type such as Establishment, Growth, Department, Project, Technology, Requirement, Culture, or Financial
- title
- date or period
- detailed description
- tags
- expiry date and active status

This allows recruiters to search not only candidates, but also company documents and present requirements before shortlisting. The Auto Match tab combines both active datasets and returns candidate potential labels for the company.
