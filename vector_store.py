import hashlib
import os
import re
from typing import Iterable

import numpy as np

from company_store import load_company_records
from candidate_store import load_candidates, update_candidate_score
from resume_analyzer import analyze_resume, tokenize


VECTOR_DIMENSION = 384


def embed_text(text: str, dimension: int = VECTOR_DIMENSION) -> list[float]:
    """Create a deterministic lightweight embedding for demo and fallback use."""
    vector = np.zeros(dimension, dtype=np.float32)
    tokens = tokenize(text)
    if not tokens:
        return vector.tolist()

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimension
        sign = 1 if digest[4] % 2 == 0 else -1
        vector[index] += sign

    norm = np.linalg.norm(vector)
    if norm:
        vector = vector / norm
    return vector.tolist()


def local_rank_candidates(role_description: str, limit: int = 10) -> list[dict]:
    role_vector = np.array(embed_text(role_description), dtype=np.float32)
    ranked = []
    for candidate in load_candidates():
        resume_vector = np.array(embed_text(candidate["resume_text"]), dtype=np.float32)
        vector_score = float(np.dot(role_vector, resume_vector))
        analysis = analyze_resume(candidate["resume_text"], role_description)
        final_score = round((analysis["ats_score"] * 0.75) + (max(vector_score, 0) * 100 * 0.25))
        potential, recommendation = candidate_potential(final_score, analysis)
        update_candidate_score(candidate["candidate_id"], final_score, role_description[:80])
        ranked.append(
            {
                **candidate,
                "match_score": final_score,
                "potential": potential,
                "recommendation": recommendation,
                "ats_score": analysis["ats_score"],
                "semantic_match": analysis["semantic_match"],
                "missing_skills": ", ".join(analysis["missing_skills"][:8]),
                "strengths": "; ".join(analysis["strengths"][:2]),
            }
        )
    return sorted(ranked, key=lambda item: item["match_score"], reverse=True)[:limit]


def rag_match_report(requirement: str, limit: int = 10, use_pinecone: bool = True) -> dict:
    """Retrieve company context + resumes, then generate an explainable match report."""
    company_context = []
    if use_pinecone and pinecone_enabled():
        company_context = search_company_pinecone(requirement, limit=5)
    if not company_context:
        company_context = local_company_context(requirement, limit=5)

    context_text = "\n".join(
        f"{item.get('record_type', '')}: {item.get('title', '')} - {item.get('details', '')}"
        for item in company_context
    )
    augmented_requirement = requirement
    if context_text:
        augmented_requirement = f"{requirement}\n\nRetrieved company context:\n{context_text}"

    candidates = []
    if use_pinecone and pinecone_enabled():
        candidates = search_pinecone(augmented_requirement, limit=limit)
    if not candidates:
        candidates = local_rank_candidates(augmented_requirement, limit=limit)

    best = candidates[0] if candidates else {}
    answer = _rag_answer(requirement, company_context, candidates)
    return {
        "requirement": requirement,
        "retrieved_company_context": company_context,
        "ranked_candidates": candidates,
        "best_candidate": best,
        "answer": answer,
    }


def local_company_context(query: str, limit: int = 5) -> list[dict]:
    query_vector = np.array(embed_text(query), dtype=np.float32)
    rows = []
    for record in load_company_records():
        text = _company_record_text(record)
        record_vector = np.array(embed_text(text), dtype=np.float32)
        rows.append({**record, "match_score": round(float(np.dot(query_vector, record_vector)) * 100)})
    return sorted(rows, key=lambda item: item["match_score"], reverse=True)[:limit]


def pinecone_enabled() -> bool:
    return bool(os.getenv("PINECONE_API_KEY") and os.getenv("PINECONE_INDEX_NAME"))


def get_pinecone_index():
    if not pinecone_enabled():
        return None
    try:
        from pinecone import Pinecone, ServerlessSpec
    except Exception:
        return None

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "resume-candidates")
    cloud = os.getenv("PINECONE_CLOUD", "aws")
    region = os.getenv("PINECONE_REGION", "us-east-1")
    pc = Pinecone(api_key=api_key)
    listed = pc.list_indexes()
    if hasattr(listed, "names"):
        existing = listed.names()
    else:
        existing = [item.get("name", getattr(item, "name", "")) for item in listed]
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=VECTOR_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
    return pc.Index(index_name)


def upsert_candidate_to_pinecone(candidate: dict) -> bool:
    index = get_pinecone_index()
    if index is None:
        return False
    index.upsert(
        vectors=[
            {
                "id": candidate["candidate_id"],
                "values": embed_text(candidate["resume_text"]),
                "metadata": _metadata(candidate),
            }
        ]
    )
    return True


def upsert_candidates_to_pinecone(candidates: Iterable[dict] | None = None) -> int:
    index = get_pinecone_index()
    if index is None:
        return 0
    candidates = list(candidates or load_candidates())
    if not candidates:
        return 0
    index.upsert(
        vectors=[
            {
                "id": candidate["candidate_id"],
                "values": embed_text(candidate["resume_text"]),
                "metadata": _metadata(candidate),
            }
            for candidate in candidates
        ]
    )
    return len(candidates)


def upsert_company_records_to_pinecone(records: Iterable[dict] | None = None) -> int:
    index = get_pinecone_index()
    if index is None:
        return 0
    records = list(records or load_company_records())
    if not records:
        return 0
    index.upsert(
        vectors=[
            {
                "id": f"company-{record['record_id']}",
                "values": embed_text(_company_record_text(record)),
                "metadata": _company_metadata(record),
            }
            for record in records
        ]
    )
    return len(records)


def search_pinecone(role_description: str, limit: int = 10) -> list[dict]:
    index = get_pinecone_index()
    if index is None:
        return []
    results = index.query(
        vector=embed_text(role_description),
        top_k=limit,
        include_metadata=True,
        filter={"record_kind": {"$eq": "candidate_resume"}, "status": {"$eq": "active"}},
    )
    rows = []
    for match in results.get("matches", []):
        metadata = match.get("metadata", {})
        analysis = analyze_resume(metadata.get("resume_preview", ""), role_description)
        rows.append(
            {
                "candidate_id": match["id"],
                "name": metadata.get("name", ""),
                "email": metadata.get("email", ""),
                "phone": metadata.get("phone", ""),
                "role_applied": metadata.get("role_applied", ""),
                "match_score": round(float(match.get("score", 0)) * 100),
                "ats_score": analysis["ats_score"],
                "semantic_match": analysis["semantic_match"],
                "potential": candidate_potential(round(float(match.get("score", 0)) * 100), analysis)[0],
                "recommendation": candidate_potential(round(float(match.get("score", 0)) * 100), analysis)[1],
                "missing_skills": ", ".join(analysis["missing_skills"][:8]),
                "source": "pinecone",
            }
        )
    return rows


def candidate_potential(match_score: int, analysis: dict) -> tuple[str, str]:
    missing_count = len(analysis.get("missing_skills", []))
    if match_score >= 80 and missing_count <= 3:
        return "Ideal Match", "Send to company: high role fit, strong keywords, and low skill gap."
    if match_score >= 65:
        return "Strong Potential", "Good shortlist candidate: review missing skills and project depth."
    if match_score >= 50:
        return "Moderate Potential", "Possible backup candidate: needs improvement or training for this role."
    return "Low Match", "Do not prioritize for this requirement unless the company wants a broad pool."


def _rag_answer(requirement: str, company_context: list[dict], candidates: list[dict]) -> str:
    if not candidates:
        return "No active candidate resume matched this requirement. Add candidate resumes or broaden the requirement."

    best = candidates[0]
    context_titles = [item.get("title", "") for item in company_context[:3] if item.get("title")]
    context_note = ", ".join(context_titles) if context_titles else "stored company documents"
    return (
        f"Recommended candidate: {best.get('name', 'Candidate')} is a "
        f"{best.get('potential', 'Potential Match')} with score {best.get('match_score', 0)}/100. "
        f"Reason: {best.get('recommendation', '')} The ranking used the new requirement plus retrieved context from "
        f"{context_note}. Missing skills to review: {best.get('missing_skills', 'None detected')}."
    )


def search_company_pinecone(query: str, limit: int = 5) -> list[dict]:
    index = get_pinecone_index()
    if index is None:
        return []
    results = index.query(
        vector=embed_text(query),
        top_k=limit,
        include_metadata=True,
        filter={"record_kind": {"$eq": "company_knowledge"}, "status": {"$eq": "active"}},
    )
    rows = []
    for match in results.get("matches", []):
        metadata = match.get("metadata", {})
        rows.append(
            {
                "record_id": match["id"].replace("company-", ""),
                "company_name": metadata.get("company_name", ""),
                "record_type": metadata.get("record_type", ""),
                "title": metadata.get("title", ""),
                "date_or_period": metadata.get("date_or_period", ""),
                "details": metadata.get("details", ""),
                "tags": metadata.get("tags", ""),
                "match_score": round(float(match.get("score", 0)) * 100),
                "source": "pinecone",
            }
        )
    return rows


def normalize_phone(phone: str) -> str:
    return re.sub(r"[^\d+]", "", phone or "")


def _metadata(candidate: dict) -> dict:
    return {
        "record_kind": "candidate_resume",
        "name": candidate.get("name", ""),
        "email": candidate.get("email", ""),
        "phone": normalize_phone(candidate.get("phone", "")),
        "role_applied": candidate.get("role_applied", ""),
        "uploaded_at": candidate.get("uploaded_at", ""),
        "expires_at": candidate.get("expires_at", ""),
        "latest_score": candidate.get("latest_score", 0),
        "status": candidate.get("status", "active"),
        "resume_preview": candidate.get("resume_text", "")[:4000],
    }


def _company_record_text(record: dict) -> str:
    return (
        f"{record.get('company_name', '')} {record.get('record_type', '')} "
        f"{record.get('title', '')} {record.get('date_or_period', '')} "
        f"{record.get('details', '')} {record.get('tags', '')}"
    )


def _company_metadata(record: dict) -> dict:
    return {
        "record_kind": "company_knowledge",
        "company_name": record.get("company_name", ""),
        "record_type": record.get("record_type", ""),
        "title": record.get("title", ""),
        "date_or_period": record.get("date_or_period", ""),
        "details": record.get("details", "")[:4000],
        "tags": record.get("tags", ""),
        "created_at": record.get("created_at", ""),
        "expires_at": record.get("expires_at", ""),
        "status": record.get("status", "active"),
    }
