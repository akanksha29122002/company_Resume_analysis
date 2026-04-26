import base64
import os
from io import BytesIO

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from candidate_store import add_candidate, purge_expired
from company_store import add_company_record, purge_expired_company_records
from resume_analyzer import analyze_resume, extract_pdf_text
from vector_store import rag_match_report, upsert_candidate_to_pinecone, upsert_company_records_to_pinecone


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


class CompanyIngest(BaseModel):
    company_name: str
    record_type: str = "Requirement"
    title: str = ""
    date_or_period: str = ""
    details: str = ""
    tags: str = ""
    document_pdf_base64: str = ""
    source: str = "google-form"


class MatchRequest(BaseModel):
    requirement: str
    limit: int = 10
    use_pinecone: bool = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest_candidate(payload: CandidateIngest, x_intake_token: str = Header(default="")):
    _validate_token(x_intake_token)

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


@app.post("/company-ingest")
def ingest_company_document(payload: CompanyIngest, x_intake_token: str = Header(default="")):
    _validate_token(x_intake_token)

    document_text = payload.details.strip()
    if payload.document_pdf_base64:
        try:
            pdf_bytes = base64.b64decode(payload.document_pdf_base64)
            extracted = extract_pdf_text(BytesIO(pdf_bytes))
            document_text = "\n\n".join([part for part in [extracted, document_text] if part])
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Could not parse company PDF: {exc}") from exc

    if not document_text:
        raise HTTPException(status_code=400, detail="details or document_pdf_base64 is required")

    record = add_company_record(
        company_name=payload.company_name,
        record_type=payload.record_type,
        title=payload.title,
        date_or_period=payload.date_or_period,
        details=document_text,
        tags=payload.tags,
    )
    pinecone_count = upsert_company_records_to_pinecone([record])
    purge_expired_company_records()

    return {
        "record_id": record["record_id"],
        "expires_at": record["expires_at"],
        "pinecone_synced": pinecone_count == 1,
    }


@app.post("/rag-match")
def match_candidates(payload: MatchRequest, x_intake_token: str = Header(default="")):
    _validate_token(x_intake_token)
    if not payload.requirement.strip():
        raise HTTPException(status_code=400, detail="requirement is required")
    report = rag_match_report(
        requirement=payload.requirement,
        limit=max(1, min(payload.limit, 25)),
        use_pinecone=payload.use_pinecone,
    )
    best = report.get("best_candidate") or {}
    return {
        "answer": report["answer"],
        "best_candidate": best,
        "ranked_candidates": report["ranked_candidates"],
        "retrieved_company_context": report["retrieved_company_context"],
    }


def _validate_token(token: str) -> None:
    expected_token = os.getenv("INTAKE_TOKEN", "")
    if expected_token and token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid intake token")
