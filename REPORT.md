# Final Year Project Report

## Title

AI Resume Analyzer and Company Knowledge Bank

## Abstract

The AI Resume Analyzer and Company Knowledge Bank is a web application where companies upload requirement or company documents and candidates upload resumes. Both company documents and candidate resumes are stored as active records for approximately 6 months. The system extracts text, stores vectors, compares active resumes with company requirements, and automatically reports which candidates are ideal matches for the company.

The upgraded company version supports automatic resume intake using Google Apps Script, stores candidates and company documents for 6 months, syncs both resume vectors and company-document vectors to Pinecone, maintains a company knowledge base from establishment to current growth, and ranks the best active candidates whenever a new company requirement is entered.

## Problem Statement

Students and job seekers often submit resumes without knowing whether their resume matches a specific job description. Companies also receive many resumes and need a fast way to shortlist the best candidates for changing role requirements. Normal matching only looks at the job description, but real hiring should also consider company history, growth direction, technology stack, departments, culture, and current business needs.

## Objectives

- Build a web app for resume PDF upload and analysis.
- Extract readable text from PDF files.
- Detect important sections such as Education, Experience, Projects, Skills, and Certifications.
- Compare the resume with a target job description.
- Generate ATS score, strengths, weaknesses, and suggestions.
- Receive resumes automatically through Google Form and Apps Script.
- Store each candidate as active for 6 months.
- Store company documents and requirements as active for 6 months.
- Use Pinecone vector search to retrieve the best-fit resumes for new roles.
- Store company establishment, growth, projects, technologies, and requirement history in Pinecone.
- Use company context while shortlisting candidates.

## Technology Stack

- Python
- Streamlit
- FastAPI
- pypdf
- Pandas and NumPy
- Regular expressions
- Tokenization and cosine similarity
- Google Apps Script
- Pinecone vector database
- RAG-style retrieval and recommendation flow
- Local JSON storage for demo candidate and company records

## Methodology

1. The user uploads a resume PDF.
2. The app extracts text using `pypdf`.
3. The text is cleaned by removing extra spaces and unwanted page markers.
4. Resume sections are detected using predefined NLP patterns.
5. Skills are matched from a curated skill bank.
6. The job description is tokenized and compared with resume text.
7. The system calculates semantic match, keyword match, section completeness, contact quality, and resume length.
8. A final ATS score is generated.
9. For company intake, candidate records are stored with upload date and expiry date.
10. Candidate resume vectors are synced to Pinecone when API keys are configured.
11. Company growth and requirement records are stored in the Company Growth module.
12. Pinecone searches company knowledge and enriches the job requirement before candidate ranking.
13. Recruiters paste a new role requirement or use stored company documents.
14. The system ranks active resumes by match score and labels candidate potential.
15. The company receives a clear recommendation such as Ideal Match or Strong Potential.
16. Apps Script can call the RAG endpoint and write automatic calculations back to Google Sheets.

## Pinecone Usage

The system stores two types of vectors in Pinecone:

- `candidate_resume`: candidate resume vectors with name, contact, role, upload date, expiry date, score, and active status.
- `company_knowledge`: company establishment, growth, departments, projects, technology stack, culture, uploaded requirement documents, and active status.

This allows the system to search both resumes and company knowledge. When a new requirement arrives, the app retrieves relevant company context, augments the role description, retrieves matching candidate resumes, and generates an explainable recommendation. This retrieval-augmented flow is the RAG system used in the project.

## Scoring Logic

The final score is calculated from:

- Skill match: 30 percent
- Semantic similarity: 25 percent
- Section completeness: 20 percent
- Keyword overlap: 15 percent
- Contact details: 5 percent
- Resume length quality: 5 percent

## Results

The system provides a dashboard where users can view:

- ATS score out of 100
- Semantic match percentage
- Keyword match percentage
- Resume word count
- Detected resume sections
- Skills found in the resume
- Missing job-related skills
- Strengths and weaknesses
- Active candidate database
- Candidate expiry date after 6 months
- Company document expiry date after 6 months
- Searchable company timeline and requirement knowledge base
- Best candidate shortlist for each role
- Candidate potential and recommendation reason
- CSV export of shortlisted candidates

## Advantages

- Easy to use
- Deployable on Streamlit Cloud
- Supports automatic intake through Google Apps Script
- Supports Pinecone vector search
- Maintains active candidate records for 6 months
- Uses company history and growth context for better hiring decisions
- Gives clear and actionable feedback
- Includes local fallback for demonstration without Pinecone keys

## Limitations

- Scoring is heuristic and may not match every company ATS system exactly.
- Image-only PDF resumes may not extract text correctly.
- The skill bank is predefined and can be expanded.
- Pinecone needs environment variables and internet access in production.
- The default embedding method is lightweight for deployment; transformer embeddings can improve semantic quality.

## Future Scope

- Add transformer-based embeddings for more accurate vector search.
- Add resume improvement generation.
- Export feedback as PDF.
- Support DOCX resumes.
- Add email alerts when new requirements match existing candidates.
- Add company analytics dashboards for hiring trends and growth requirements.

## Conclusion

The AI Resume Analyzer and Company Knowledge Bank converts the notebook idea into a deployable final-year project. It combines resume parsing, NLP-based scoring, automatic candidate intake, Pinecone vector search, 6-month active candidate management, and company growth knowledge to support smarter hiring decisions.
