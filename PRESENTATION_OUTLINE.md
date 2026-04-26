# PPT Outline: AI Resume Analyzer and Company Knowledge Bank

## Slide 1: Title

Company Resume Analysis and Ideal Match Finder

Presented by: Your Name

## Slide 2: Introduction

- Resume screening is an important step in recruitment.
- Many resumes fail due to missing keywords and poor structure.
- Companies upload requirement documents.
- Candidates upload resumes.
- Both remain active for 6 months.
- Company history and growth should influence hiring decisions.

## Slide 3: Problem Statement

- Students do not know how well their resume matches a job description.
- Manual resume review is slow.
- Companies need automatic matching when requirements arrive.
- Requirement matching should consider company establishment, growth, projects, and current direction.

## Slide 4: Objectives

- Companies upload requirement/company PDFs.
- Candidates upload resume PDFs.
- Receive resumes automatically from Google Forms.
- Store active candidates and company documents for 6 months.
- Store company establishment-to-current growth details in Pinecone.
- Rank candidates for new company roles.

## Slide 5: System Architecture

- Google Form sends resume data through Apps Script.
- FastAPI intake stores candidate records.
- Pinecone stores resume vectors and company document vectors.
- Automation compares both active datasets.
- Streamlit dashboard gives ideal match recommendations.

## Slide 6: Modules

- PDF text extraction
- Text cleaning
- Skill and section detection
- Candidate database
- Company growth knowledge base
- Company document upload
- Apps Script intake
- Pinecone vector search

## Slide 7: Pinecone Design

- `candidate_resume` records store resume vectors and candidate metadata.
- `company_knowledge` records store establishment, growth, project, technology, and requirement details.
- Role matching uses candidate data and retrieved company documents.
- Output shows Ideal Match, Strong Potential, Moderate Potential, or Low Match.

## Slide 8: RAG Flow

- Store company documents and resumes as vectors in Pinecone.
- Retrieve relevant company context for a new requirement.
- Augment the requirement with retrieved context.
- Retrieve and rank active candidate resumes.
- Generate an explainable recommendation for the company.

## Slide 9: Apps Script Automation

- Candidate form automatically sends resumes to the API.
- Company form automatically sends requirements to the API.
- Google Sheets menu calls `/rag-match`.
- Sheet receives best candidate, potential, score, and recommendation.

## Slide 10: Scoring Method

- Skill match: 30 percent
- Semantic similarity: 25 percent
- Section completeness: 20 percent
- Keyword overlap: 15 percent
- Contact and length quality: 10 percent

## Slide 11: User Interface

- Single resume analyzer
- Company candidate intake
- Company growth timeline
- Active candidate database
- Role matching dashboard
- CSV shortlist export

## Slide 12: Results

- ATS score out of 100
- Strengths and weaknesses
- Missing job skills
- Candidate expiry date
- Company requirement context
- Best-fit role shortlist
- Candidate potential and reason

## Slide 13: Deployment

- Dashboard deploys on Streamlit Cloud.
- Webhook API deploys on Render.
- Apps Script connects Google Form to API.
- Pinecone is optional with local fallback.

## Slide 14: Conclusion

- The project helps students and companies.
- It automates intake, scoring, and retrieval.
- It uses company growth history for better hiring decisions.
- It is deployable and presentation-ready.
