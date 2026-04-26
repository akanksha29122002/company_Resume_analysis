# Final Year Project Report

## Title

AI Resume Analyzer and Company Knowledge Bank

## Abstract

The AI Resume Analyzer is a web application that evaluates candidate resumes against target job descriptions. The system extracts text from PDF resumes, cleans the extracted text, detects key resume sections, identifies skills, compares resume keywords with job requirements, and generates ATS-style scores with strengths, weaknesses, and improvement suggestions.

The upgraded company version supports automatic resume intake using Google Apps Script, stores candidates for 6 months, syncs resume vectors to Pinecone, maintains a company knowledge base from establishment to current growth, and ranks the best active candidates whenever a new company requirement is entered.

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
12. Pinecone searches company knowledge and can enrich the job requirement before candidate ranking.
13. Recruiters paste a new role requirement and the system ranks active resumes by match score.

## Pinecone Usage

The system stores two types of vectors in Pinecone:

- `candidate_resume`: candidate resume vectors with name, contact, role, upload date, expiry date, score, and active status.
- `company_knowledge`: company establishment, growth, departments, projects, technology stack, culture, and requirement records.

This allows the system to search both resumes and company knowledge. When a new requirement arrives, the app can combine the role description with company context and find candidates who match the actual direction of the company.

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
- Searchable company timeline and requirement knowledge base
- Best candidate shortlist for each role
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
