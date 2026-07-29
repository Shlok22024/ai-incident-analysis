"""Clean the extracted AIID incident table for downstream analysis."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "aiid_snapshot_raw.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "incidents_cleaned.csv"
MIN_YEAR = 2010
GENAI_CUTOFF_YEAR = 2023


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().split())


def build_text_for_classification(row: pd.Series) -> str:
    parts = [
        row["title"],
        row["description"],
        row["alleged_deployer"],
        row["alleged_developer"],
        row["alleged_harmed_parties"],
    ]
    return " ".join(part for part in parts if part).lower()


def main() -> None:
    incidents = pd.read_csv(RAW_PATH)

    incidents["incident_date"] = pd.to_datetime(incidents["incident_date"], errors="coerce")
    incidents = incidents.dropna(subset=["incident_date", "incident_id", "title", "description"]).copy()

    for column in [
        "title",
        "description",
        "alleged_deployer",
        "alleged_developer",
        "alleged_harmed_parties",
        "report_ids",
        "snapshot_date",
        "snapshot_url",
    ]:
        incidents[column] = incidents[column].apply(normalize_text)

    incidents = incidents.drop_duplicates(subset=["incident_id"]).copy()
    incidents["incident_year"] = incidents["incident_date"].dt.year.astype(int)
    incidents["incident_month"] = incidents["incident_date"].dt.month.astype(int)
    incidents = incidents.loc[incidents["incident_year"] >= MIN_YEAR].copy()
    incidents["pre_post_genai_period"] = incidents["incident_year"].map(
        lambda year: "Pre-generative-AI period (before 2023)"
        if year < GENAI_CUTOFF_YEAR
        else "Generative-AI period (2023 onward)"
    )
    incidents["text_for_classification"] = incidents.apply(build_text_for_classification, axis=1)

    incidents["incident_date"] = incidents["incident_date"].dt.strftime("%Y-%m-%d")
    incidents = incidents.sort_values(["incident_date", "incident_id"]).reset_index(drop=True)

    output_columns = [
        "incident_id",
        "incident_date",
        "incident_year",
        "incident_month",
        "pre_post_genai_period",
        "title",
        "description",
        "alleged_deployer",
        "alleged_developer",
        "alleged_harmed_parties",
        "report_count",
        "report_ids",
        "text_for_classification",
        "snapshot_date",
        "snapshot_url",
    ]
    incidents[output_columns].to_csv(OUTPUT_PATH, index=False)
    print(
        f"Saved {len(incidents):,} cleaned incidents to {OUTPUT_PATH.relative_to(ROOT)} "
        f"after filtering to incidents from {MIN_YEAR} onward."
    )


if __name__ == "__main__":
    main()
