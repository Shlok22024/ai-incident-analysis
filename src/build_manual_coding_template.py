"""Create blank directed-coding workbooks from the selected incident sample."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "processed" / "manual_sample_2010_2021.csv"
MANUAL_DIR = ROOT / "data" / "manual_coding"
WORKBOOK_PATH = MANUAL_DIR / "manual_coding_2010_2021.csv"
PASS2_PATH = MANUAL_DIR / "manual_coding_2010_2021_pass2.csv"


def build_template(sample: pd.DataFrame, coder: str, coding_pass: str) -> pd.DataFrame:
    template = pd.DataFrame(
        {
            "incident_id": sample["incident_id"],
            "title": sample["title"],
            "year": sample["year"],
            "geographic_location": "",
            "application_area": "",
            "ethics_issue_1": "",
            "ethics_issue_2": "",
            "ethics_issue_3": "",
            "ethics_issue_4": "",
            "ethics_issue_notes": "",
            "evidence_notes": "",
            "coder": coder,
            "coding_pass": coding_pass,
            "uncertainty_flag": False,
        }
    )
    return template


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)

    build_template(sample, coder="project_author", coding_pass="pass1").to_csv(WORKBOOK_PATH, index=False)
    build_template(sample, coder="project_author", coding_pass="pass2").to_csv(PASS2_PATH, index=False)

    print(
        "Saved blank directed-coding workbooks to "
        f"{WORKBOOK_PATH.relative_to(ROOT)} and {PASS2_PATH.relative_to(ROOT)}."
    )


if __name__ == "__main__":
    main()
