"""Download a stable AIID snapshot and extract the raw incident table."""

from __future__ import annotations

import ast
import csv
import io
import tarfile
from datetime import date
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
ARCHIVE_NAME = "backup-20260727110451.tar.bz2"
ARCHIVE_PATH = RAW_DIR / ARCHIVE_NAME
SNAPSHOT_DATE = "2026-07-27"
SNAPSHOT_PAGE_URL = "https://incidentdatabase.ai/research/snapshots/"
SNAPSHOT_URL = (
    "https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/"
    "backup-20260727110451.tar.bz2"
)
EXPECTED_ARCHIVE_BYTES = 104_995_975
INCIDENTS_MEMBER = "mongodump_full_snapshot/incidents.csv"
RAW_OUTPUT_PATH = RAW_DIR / "aiid_snapshot_raw.csv"
SOURCE_LOG_PATH = RAW_DIR / "source_documents_log.csv"
PAPER_COUNTS_PATH = RAW_DIR / "original_paper_reference_counts.csv"

PAPER_COUNTS = [
    ("application_area", "Intelligent service robots", 31, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Language/vision model", 27, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Autonomous driving", 17, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Intelligent recommendation", 14, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Identity authentication", 14, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "AI supervision", 14, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Smart healthcare", 10, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "AI recruitment", 10, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Predictive policing", 5, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Smart finance", 4, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "AI game", 2, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "Smart home", 2, "Wei and Zhou (2022), Section 4.3"),
    ("application_area", "AI education", 2, "Wei and Zhou (2022), Section 4.3"),
    ("ethics_issue", "Inappropriate use (bad performance)", 48, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Racial discrimination", 38, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Physical safety", 32, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Unfair algorithm (evaluation)", 22, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Gender discrimination", 19, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Privacy", 12, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Unethical use (illegal use)", 11, "Wei and Zhou (2022), Section 4.4"),
    ("ethics_issue", "Mental health", 4, "Wei and Zhou (2022), Section 4.4"),
]


def ensure_raw_dir() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_snapshot() -> None:
    """Download the chosen stable snapshot only when needed."""
    if ARCHIVE_PATH.exists() and ARCHIVE_PATH.stat().st_size == EXPECTED_ARCHIVE_BYTES:
        print(f"Using existing snapshot archive: {ARCHIVE_PATH.name}")
        return

    temp_path = ARCHIVE_PATH.with_suffix(ARCHIVE_PATH.suffix + ".part")
    if temp_path.exists():
        temp_path.unlink()

    response = requests.get(SNAPSHOT_URL, stream=True, timeout=60)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))

    with temp_path.open("wb") as handle, tqdm(
        total=total,
        unit="B",
        unit_scale=True,
        desc="Downloading AIID snapshot",
    ) as progress:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if not chunk:
                continue
            handle.write(chunk)
            progress.update(len(chunk))

    if temp_path.stat().st_size != EXPECTED_ARCHIVE_BYTES:
        temp_path.unlink(missing_ok=True)
        raise ValueError(
            "Downloaded archive size does not match the expected snapshot size. "
            "Please rerun the loader."
        )

    temp_path.replace(ARCHIVE_PATH)
    print(f"Downloaded snapshot archive: {ARCHIVE_PATH.name}")


def read_csv_from_archive(member_name: str) -> pd.DataFrame:
    """Read a CSV file directly from the compressed AIID backup."""
    with tarfile.open(ARCHIVE_PATH, mode="r:bz2") as archive:
        extracted = archive.extractfile(member_name)
        if extracted is None:
            raise FileNotFoundError(f"Missing {member_name} in {ARCHIVE_PATH.name}")
        text_stream = io.TextIOWrapper(extracted, encoding="utf-8")
        return pd.read_csv(text_stream)


def parse_list_cell(value: object) -> list[str]:
    """Convert AIID's serialized list-like strings into plain text values."""
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return [text]
    if isinstance(parsed, list):
        return [normalize_text(item) for item in parsed if str(item).strip()]
    return [normalize_text(parsed)]


def normalize_text(value: object) -> str:
    """Repair common mojibake found in exported AIID text fields."""
    if pd.isna(value):
        return ""

    text = str(value).strip()
    if not text:
        return ""

    try:
        repaired = text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

    if repaired.count("\ufffd") > text.count("\ufffd"):
        return text
    return repaired


def list_to_text(value: object) -> str:
    items = parse_list_cell(value)
    return "; ".join(items)


def report_count(value: object) -> int:
    return len(parse_list_cell(value))


def build_raw_snapshot() -> pd.DataFrame:
    incidents = read_csv_from_archive(INCIDENTS_MEMBER)

    raw_snapshot = incidents.rename(
        columns={
            "incident_id": "incident_id",
            "date": "incident_date",
            "title": "title",
            "description": "description",
            "reports": "report_ids",
            "Alleged deployer of AI system": "alleged_deployer",
            "Alleged developer of AI system": "alleged_developer",
            "Alleged harmed or nearly harmed parties": "alleged_harmed_parties",
        }
    )[
        [
            "incident_id",
            "incident_date",
            "title",
            "description",
            "report_ids",
            "alleged_deployer",
            "alleged_developer",
            "alleged_harmed_parties",
        ]
    ].copy()

    raw_snapshot["report_count"] = raw_snapshot["report_ids"].apply(report_count)
    raw_snapshot["title"] = raw_snapshot["title"].apply(normalize_text)
    raw_snapshot["description"] = raw_snapshot["description"].apply(normalize_text)
    raw_snapshot["alleged_deployer"] = raw_snapshot["alleged_deployer"].apply(list_to_text)
    raw_snapshot["alleged_developer"] = raw_snapshot["alleged_developer"].apply(list_to_text)
    raw_snapshot["alleged_harmed_parties"] = raw_snapshot["alleged_harmed_parties"].apply(list_to_text)
    raw_snapshot["snapshot_date"] = SNAPSHOT_DATE
    raw_snapshot["snapshot_url"] = SNAPSHOT_URL

    ordered_columns = [
        "incident_id",
        "incident_date",
        "title",
        "description",
        "report_count",
        "report_ids",
        "alleged_deployer",
        "alleged_developer",
        "alleged_harmed_parties",
        "snapshot_date",
        "snapshot_url",
    ]
    raw_snapshot = raw_snapshot[ordered_columns].sort_values("incident_id").reset_index(drop=True)
    return raw_snapshot


def write_source_log() -> None:
    accessed_date = date.today().isoformat()
    rows = [
        {
            "document_type": "snapshot_page",
            "source_name": "AI Incident Database snapshots page",
            "source_url": SNAPSHOT_PAGE_URL,
            "accessed_date": accessed_date,
            "snapshot_date": SNAPSHOT_DATE,
            "notes": "Used to verify the latest stable weekly snapshot and exact download link.",
        },
        {
            "document_type": "snapshot_archive",
            "source_name": ARCHIVE_NAME,
            "source_url": SNAPSHOT_URL,
            "accessed_date": accessed_date,
            "snapshot_date": SNAPSHOT_DATE,
            "notes": "Official AIID backup archive used as the reproducible raw source.",
        },
        {
            "document_type": "paper_abs",
            "source_name": "arXiv abstract page",
            "source_url": "https://arxiv.org/abs/2206.07635",
            "accessed_date": accessed_date,
            "snapshot_date": "",
            "notes": "Paper metadata and abstract.",
        },
        {
            "document_type": "paper_pdf",
            "source_name": "arXiv PDF",
            "source_url": "https://arxiv.org/pdf/2206.07635",
            "accessed_date": accessed_date,
            "snapshot_date": "",
            "notes": "Used for application-area and ethics-issue reference counts.",
        },
        {
            "document_type": "paper_hicss",
            "source_name": "ScholarSpace HICSS paper page",
            "source_url": "https://scholarspace.manoa.hawaii.edu/items/5c4f0c5c-427b-4e36-8d71-94f3e70934e3",
            "accessed_date": accessed_date,
            "snapshot_date": "",
            "notes": "Venue landing page for the HICSS version of the paper.",
        },
        {
            "document_type": "source_repo",
            "source_name": "AI Incident Database GitHub repository",
            "source_url": "https://github.com/responsible-ai-collaborative/aiid",
            "accessed_date": accessed_date,
            "snapshot_date": "",
            "notes": "Reference repository for database structure and provenance.",
        },
    ]

    with SOURCE_LOG_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "document_type",
                "source_name",
                "source_url",
                "accessed_date",
                "snapshot_date",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_paper_reference_counts() -> None:
    with PAPER_COUNTS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["category_type", "category_name", "paper_reported_count", "notes"])
        writer.writerows(PAPER_COUNTS)


def main() -> None:
    ensure_raw_dir()
    download_snapshot()
    raw_snapshot = build_raw_snapshot()
    raw_snapshot.to_csv(RAW_OUTPUT_PATH, index=False)
    write_source_log()
    write_paper_reference_counts()
    print(
        "Saved "
        f"{len(raw_snapshot):,} incidents to {RAW_OUTPUT_PATH.relative_to(ROOT)} "
        f"using the {SNAPSHOT_DATE} AIID snapshot."
    )


if __name__ == "__main__":
    main()
