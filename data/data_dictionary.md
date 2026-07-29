# Data Dictionary

## Raw data

### `data/raw/source_documents_log.csv`
Tracks the source documents, snapshot links, access dates, and notes used in the project.

### `data/raw/aiid_snapshot_raw.csv`
Placeholder for the raw AI Incident Database snapshot used in the analysis.

### `data/raw/original_paper_reference_counts.csv`
Placeholder for manually entered reference counts from the original paper, when needed for comparison.

## Processed data

### `data/processed/incidents_cleaned.csv`
Cleaned incident-level dataset used for analysis.

### `data/processed/incident_categories_recreated.csv`
Transparent mapping of source fields into recreated ethics issue and application area categories.

### `data/processed/application_area_summary.csv`
Summary table of incident counts by application area.

### `data/processed/ethics_issue_summary.csv`
Summary table of incident counts by ethics issue category.

### `data/processed/pre_post_genai_summary.csv`
Summary table comparing practical pre-2023 and 2023-and-later groupings.

### `data/processed/summary_stats.md`
Plain-English project summary statistics for reuse in the README and report.
