import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


DATA_DIR = Path("data")
COMPANY_PATH = DATA_DIR / "company_knowledge.json"
ACTIVE_DAYS = 183


@dataclass
class CompanyRecord:
    record_id: str
    company_name: str
    record_type: str
    title: str
    date_or_period: str
    details: str
    tags: str
    created_at: str
    expires_at: str
    status: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def load_company_records() -> list[dict]:
    if not COMPANY_PATH.exists():
        return []
    with COMPANY_PATH.open("r", encoding="utf-8") as file:
        records = json.load(file)
    now = utc_now()
    return [record for record in records if _parse_expiry(record) >= now]


def save_company_records(records: list[dict]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with COMPANY_PATH.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def add_company_record(
    company_name: str,
    record_type: str,
    title: str,
    date_or_period: str,
    details: str,
    tags: str = "",
) -> dict:
    record = CompanyRecord(
        record_id=str(uuid.uuid4()),
        company_name=company_name.strip() or "Company",
        record_type=record_type.strip() or "General",
        title=title.strip() or "Untitled Record",
        date_or_period=date_or_period.strip(),
        details=details.strip(),
        tags=tags.strip(),
        created_at=utc_now().replace(microsecond=0).isoformat(),
        expires_at=(utc_now() + timedelta(days=ACTIVE_DAYS)).replace(microsecond=0).isoformat(),
        status="active",
    )
    records = load_company_records()
    records.append(asdict(record))
    save_company_records(records)
    return asdict(record)


def company_context_text(records: list[dict] | None = None, limit: int = 12) -> str:
    records = list(records or load_company_records())
    if not records:
        return ""
    latest = records[-limit:]
    chunks = []
    for record in latest:
        chunks.append(
            f"{record.get('company_name', '')} | {record.get('record_type', '')} | "
            f"{record.get('title', '')} | {record.get('date_or_period', '')}: "
            f"{record.get('details', '')} Tags: {record.get('tags', '')}"
        )
    return "\n".join(chunks)


def sample_company_records() -> list[dict]:
    examples = [
        (
            "DemoTech Solutions",
            "Establishment",
            "Company founded",
            "2019",
            "Started as a software services company focused on web applications, automation, and analytics dashboards for local businesses.",
            "foundation, software, services",
        ),
        (
            "DemoTech Solutions",
            "Growth",
            "AI and data practice launched",
            "2022",
            "Expanded into data analytics, machine learning prototypes, and Streamlit dashboards for hiring, sales, and operations teams.",
            "growth, ai, data, streamlit",
        ),
        (
            "DemoTech Solutions",
            "Requirement",
            "Python developer hiring need",
            "Current",
            "Needs candidates who can build Python automation, SQL data workflows, Streamlit dashboards, and communicate with business users.",
            "python, sql, streamlit, communication",
        ),
    ]
    return [
        {
            "record_id": str(uuid.uuid4()),
            "company_name": item[0],
            "record_type": item[1],
            "title": item[2],
            "date_or_period": item[3],
            "details": item[4],
            "tags": item[5],
            "created_at": utc_now().replace(microsecond=0).isoformat(),
            "expires_at": (utc_now() + timedelta(days=ACTIVE_DAYS)).replace(microsecond=0).isoformat(),
            "status": "active",
        }
        for item in examples
    ]


def purge_expired_company_records() -> int:
    if not COMPANY_PATH.exists():
        return 0
    with COMPANY_PATH.open("r", encoding="utf-8") as file:
        records = json.load(file)
    now = utc_now()
    active = [record for record in records if _parse_expiry(record) >= now]
    save_company_records(active)
    return len(records) - len(active)


def _parse_expiry(record: dict) -> datetime:
    value = record.get("expires_at")
    if not value:
        return utc_now() + timedelta(days=ACTIVE_DAYS)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
