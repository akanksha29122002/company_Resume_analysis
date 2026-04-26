import base64
import os
from io import BytesIO

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from candidate_store import add_candidate, purge_expired
from resume_analyzer import analyze_resume, extract_pdf_text
from vector_store import upsert_candidate_to_pinecone


app = FastAPI(title="Resume Intake API")


class CandidateIngest(BaseModel):
    name: str
    email: str
    phone: str = ""
    role_applied: str = ""
    resume_text: str = ""
    resume_pdf_base64: str = ""
    job_description: str = ""
    source: str = "google-form"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest_candidate(payload: CandidateIngest, x_intake_token: str = Header(default="")):
    expected_token = os.getenv("INTAKE_TOKEN", "")
    if expected_token and x_intake_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid intake token")

    resume_text = payload.resume_text.strip()
    if not resume_text and payload.resume_pdf_base64:
        try:
            pdf_bytes = base64.b64decode(payload.resume_pdf_base64)
            resume_text = extract_pdf_text(BytesIO(pdf_bytes))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Could not parse PDF: {exc}") from exc

    if not resume_text:
        raise HTTPException(status_code=400, detail="resume_text or resume_pdf_base64 is required")

    analysis = analyze_resume(resume_text, payload.job_description or payload.role_applied)
    candidate = add_candidate(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        role_applied=payload.role_applied,
        resume_text=resume_text,
        source=payload.source,
        latest_score=analysis["ats_score"],
        latest_role=payload.role_applied,
    )
    pinecone_synced = upsert_candidate_to_pinecone(candidate)
    purge_expired()

    return {
        "candidate_id": candidate["candidate_id"],
        "ats_score": analysis["ats_score"],
        "expires_at": candidate["expires_at"],
        "pinecone_synced": pinecone_synced,
    }
