"""Create a reproducible manual-coding sample for the 2010-2021 recreation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "incidents_cleaned.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "manual_sample_2010_2021.csv"
LOG_PATH = ROOT / "data" / "processed" / "manual_sample_selection_log.md"

START_YEAR = 2010
END_YEAR = 2021
SAMPLE_SIZE = 150


def build_source_reference(row: pd.Series) -> str:
    return f"AIID incident {int(row['incident_id'])}; report_ids={row['report_ids']}"


def main() -> None:
    incidents = pd.read_csv(INPUT_PATH)

    eligible = incidents.loc[
        (incidents["incident_year"] >= START_YEAR)
        & (incidents["incident_year"] <= END_YEAR)
        & incidents["title"].fillna("").str.strip().ne("")
        & incidents["description"].fillna("").str.strip().ne("")
        & incidents["incident_date"].fillna("").str.strip().ne("")
    ].copy()

    eligible = eligible.sort_values("incident_id").reset_index(drop=True)
    sample = eligible.head(SAMPLE_SIZE).copy()

    sample["source_url_or_reference"] = sample.apply(build_source_reference, axis=1)
    sample["included_in_manual_sample"] = True
    sample["sample_selection_reason"] = (
        f"Deterministic selection: first {SAMPLE_SIZE} incidents by incident_id after "
        f"filtering to {START_YEAR}-{END_YEAR} records with non-empty title, description, and date."
    )

    output_columns = [
        "incident_id",
        "title",
        "incident_date",
        "year",
        "description",
        "source_url_or_reference",
        "included_in_manual_sample",
        "sample_selection_reason",
    ]
    sample = sample.rename(columns={"incident_year": "year"})
    sample[output_columns].to_csv(OUTPUT_PATH, index=False)

    log_text = "\n".join(
        [
            "# Manual Sample Selection Log",
            "",
            "## Goal",
            "Recreate the paper's 2010-2021 incident analysis with a reproducible 150-incident sample.",
            "",
            "## Selection rule used in this project",
            f"- Filter the cleaned AIID incident table to incidents dated from {START_YEAR} through {END_YEAR}.",
            "- Keep incidents with non-empty title, description, and date fields.",
            f"- Sort the eligible incidents by incident_id and take the first {SAMPLE_SIZE}.",
            "",
            "## Why this differs from the paper",
            "- The paper states that 150 incidents from 2010-2021 were analyzed, but the exact public selection rule is not fully recoverable from the paper alone.",
            "- This project therefore uses an explicit deterministic rule so another reader can rebuild the exact same sample.",
            "",
            "## Limitation",
            "- This is a reproducible approximation of the paper's incident set, not proof that it matches the authors' original 150-incident sample.",
        ]
    )
    LOG_PATH.write_text(log_text + "\n", encoding="utf-8")

    print(
        f"Saved {len(sample):,} incidents to {OUTPUT_PATH.relative_to(ROOT)} "
        f"using the deterministic {START_YEAR}-{END_YEAR} sample rule."
    )


if __name__ == "__main__":
    main()
