import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


DATA_DIR = Path("data")
STORE_PATH = DATA_DIR / "candidates.json"
ACTIVE_DAYS = 183


@dataclass
class Candidate:
    candidate_id: str
    name: str
    email: str
    phone: str
    role_applied: str
    source: str
    resume_text: str
    uploaded_at: str
    expires_at: str
    latest_score: int
    latest_role: str
    status: str
    notes: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat()


def load_candidates(include_expired: bool = False) -> list[dict]:
    if not STORE_PATH.exists():
        return []
    with STORE_PATH.open("r", encoding="utf-8") as file:
        candidates = json.load(file)
    if include_expired:
        return candidates
    now = utc_now()
    return [item for item in candidates if _parse_dt(item["expires_at"]) >= now]


def save_candidates(candidates: list[dict]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with STORE_PATH.open("w", encoding="utf-8") as file:
        json.dump(candidates, file, indent=2)


def add_candidate(
    name: str,
    email: str,
    phone: str,
    role_applied: str,
    resume_text: str,
    source: str = "manual",
    latest_score: int = 0,
    latest_role: str = "",
    notes: str = "",
) -> dict:
    now = utc_now()
    candidate = Candidate(
        candidate_id=str(uuid.uuid4()),
        name=name.strip() or "Unknown Candidate",
        email=email.strip(),
        phone=phone.strip(),
        role_applied=role_applied.strip(),
        source=source.strip() or "manual",
        resume_text=resume_text.strip(),
        uploaded_at=iso(now),
        expires_at=iso(now + timedelta(days=ACTIVE_DAYS)),
        latest_score=int(latest_score),
        latest_role=latest_role.strip(),
        status="active",
        notes=notes.strip(),
    )
    candidates = load_candidates(include_expired=True)
    candidates.append(asdict(candidate))
    save_candidates(candidates)
    return asdict(candidate)


def update_candidate_score(candidate_id: str, score: int, role: str) -> None:
    candidates = load_candidates(include_expired=True)
    for candidate in candidates:
        if candidate["candidate_id"] == candidate_id:
            candidate["latest_score"] = int(score)
            candidate["latest_role"] = role
            break
    save_candidates(candidates)


def purge_expired() -> int:
    candidates = load_candidates(include_expired=True)
    now = utc_now()
    active = [item for item in candidates if _parse_dt(item["expires_at"]) >= now]
    save_candidates(active)
    return len(candidates) - len(active)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
