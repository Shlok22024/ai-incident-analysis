# Data Dictionary

## Raw data

### `data/raw/source_documents_log.csv`
Tracks the source documents, snapshot links, access dates, and notes used in the project.

### `data/raw/aiid_snapshot_raw.csv`
Raw incident-level extract built from the official AIID snapshot dated July 27, 2026. Includes incident date, title, description, report count, and key organization/party fields used in the later mapping steps.

### `data/raw/original_paper_reference_counts.csv`
Reference counts transcribed from the Wei and Zhou paper for the original application-area and ethics-issue categories.

## Processed data

### `data/processed/incidents_cleaned.csv`
Cleaned incident-level dataset used for analysis.

### `data/processed/incident_categories_recreated.csv`
Long-form incident-to-category output. Each row records either one recreated application-area assignment or one recreated ethics-issue assignment for a specific incident.

### `data/processed/category_mapping.csv`
Transparent rule table used to recreate application areas and ethics issues from the public AIID text fields.

### `data/processed/application_area_summary.csv`
Summary table of incident counts by application area.

### `data/processed/ethics_issue_summary.csv`
Summary table of incident counts by ethics issue category.

### `data/processed/pre_post_genai_summary.csv`
Summary table comparing practical pre-2023 and 2023-and-later groupings.

### `data/processed/summary_stats.md`
Plain-English project summary statistics for reuse in the README and report.
