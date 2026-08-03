"""Build directed-coding summary tables for the AI incident analysis project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
MANUAL_DIR = ROOT / "data" / "manual_coding"
OUTPUT_TABLES_DIR = ROOT / "outputs" / "tables"

MANUAL_CODING_PATH = MANUAL_DIR / "manual_coding_2010_2021.csv"
EXTENSION_CODING_PATH = MANUAL_DIR / "manual_coding_post_2021_extension.csv"
PAPER_COUNTS_PATH = ROOT / "data" / "raw" / "original_paper_reference_counts.csv"
CLEANED_INCIDENTS_PATH = PROCESSED_DIR / "incidents_cleaned.csv"
SAMPLE_PATH = PROCESSED_DIR / "manual_sample_2010_2021.csv"

APPLICATION_SUMMARY_PATH = PROCESSED_DIR / "application_area_summary.csv"
ETHICS_SUMMARY_PATH = PROCESSED_DIR / "ethics_issue_summary.csv"
GEOGRAPHIC_SUMMARY_PATH = PROCESSED_DIR / "geographic_summary.csv"
PAPER_APP_COMPARISON_PATH = PROCESSED_DIR / "paper_comparison_application_areas.csv"
PAPER_ETHICS_COMPARISON_PATH = PROCESSED_DIR / "paper_comparison_ethics_issues.csv"
PAPER_NAMED_MISMATCH_PATH = PROCESSED_DIR / "paper_named_incident_id_mismatch_check.csv"
PRE_POST_SUMMARY_PATH = PROCESSED_DIR / "pre_post_genai_summary.csv"
POST_2021_TAXONOMY_FIT_PATH = PROCESSED_DIR / "post_2021_taxonomy_fit_summary.csv"
SUMMARY_STATS_PATH = PROCESSED_DIR / "summary_stats.md"

ETHICS_COLUMNS = ["ethics_issue_1", "ethics_issue_2", "ethics_issue_3", "ethics_issue_4"]

PRE_PERIOD = "2010-2021 manual recreation"
POST_PERIOD = "2022-2026 extension sample"

COMPARE_APPLICATION_AREAS = [
    "Language/vision model",
    "Autonomous driving",
    "AI supervision",
    "Intelligent recommendation",
]
COMPARE_ETHICS_ISSUES = [
    "Racial discrimination",
    "Privacy",
    "Unethical use (illegal use)",
    "Mental health",
    "Physical safety",
]

PAPER_NAMED_REFERENCES: list[dict[str, object]] = [
    {"incident_id": 5, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 63, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 64, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 114, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 9, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 56, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 141, "paper_category_type": "application_area", "paper_category": "Intelligent service robots"},
    {"incident_id": 14, "paper_category_type": "application_area", "paper_category": "Language/vision model"},
    {"incident_id": 134, "paper_category_type": "application_area", "paper_category": "Language/vision model"},
    {"incident_id": 11, "paper_category_type": "application_area", "paper_category": "Autonomous driving"},
    {"incident_id": 66, "paper_category_type": "application_area", "paper_category": "Autonomous driving"},
    {"incident_id": 90, "paper_category_type": "application_area", "paper_category": "Autonomous driving"},
    {"incident_id": 2, "paper_category_type": "application_area", "paper_category": "Intelligent recommendation"},
    {"incident_id": 17, "paper_category_type": "application_area", "paper_category": "Intelligent recommendation"},
    {"incident_id": 28, "paper_category_type": "application_area", "paper_category": "Identity authentication"},
    {"incident_id": 31, "paper_category_type": "application_area", "paper_category": "Identity authentication"},
    {"incident_id": 46, "paper_category_type": "application_area", "paper_category": "Identity authentication"},
    {"incident_id": 70, "paper_category_type": "application_area", "paper_category": "Identity authentication"},
    {"incident_id": 133, "paper_category_type": "application_area", "paper_category": "Identity authentication"},
    {"incident_id": 138, "paper_category_type": "application_area", "paper_category": "Identity authentication"},
    {"incident_id": 3, "paper_category_type": "application_area", "paper_category": "AI supervision"},
    {"incident_id": 91, "paper_category_type": "application_area", "paper_category": "AI supervision"},
    {"incident_id": 123, "paper_category_type": "application_area", "paper_category": "AI supervision"},
    {"incident_id": 131, "paper_category_type": "application_area", "paper_category": "AI supervision"},
    {
        "incident_id": 103,
        "paper_category_type": "ethics_issue",
        "paper_category": "Inappropriate use (bad performance)",
    },
    {
        "incident_id": 63,
        "paper_category_type": "ethics_issue",
        "paper_category": "Inappropriate use (bad performance)",
    },
    {
        "incident_id": 30,
        "paper_category_type": "ethics_issue",
        "paper_category": "Inappropriate use (bad performance)",
    },
    {"incident_id": 139, "paper_category_type": "ethics_issue", "paper_category": "Racial discrimination"},
    {"incident_id": 70, "paper_category_type": "ethics_issue", "paper_category": "Racial discrimination"},
    {"incident_id": 115, "paper_category_type": "ethics_issue", "paper_category": "Racial discrimination"},
    {"incident_id": 133, "paper_category_type": "ethics_issue", "paper_category": "Racial discrimination"},
    {"incident_id": 134, "paper_category_type": "ethics_issue", "paper_category": "Racial discrimination"},
    {"incident_id": 27, "paper_category_type": "ethics_issue", "paper_category": "Physical safety"},
    {"incident_id": 90, "paper_category_type": "ethics_issue", "paper_category": "Physical safety"},
    {"incident_id": 142, "paper_category_type": "ethics_issue", "paper_category": "Physical safety"},
    {"incident_id": 5, "paper_category_type": "ethics_issue", "paper_category": "Physical safety"},
    {"incident_id": 122, "paper_category_type": "ethics_issue", "paper_category": "Physical safety"},
    {
        "incident_id": 12,
        "paper_category_type": "ethics_issue",
        "paper_category": "Unfair algorithm (evaluation)",
    },
    {
        "incident_id": 39,
        "paper_category_type": "ethics_issue",
        "paper_category": "Unfair algorithm (evaluation)",
    },
    {"incident_id": 14, "paper_category_type": "ethics_issue", "paper_category": "Gender discrimination"},
    {"incident_id": 20, "paper_category_type": "ethics_issue", "paper_category": "Gender discrimination"},
    {"incident_id": 36, "paper_category_type": "ethics_issue", "paper_category": "Gender discrimination"},
    {"incident_id": 45, "paper_category_type": "ethics_issue", "paper_category": "Gender discrimination"},
    {"incident_id": 17, "paper_category_type": "ethics_issue", "paper_category": "Gender discrimination"},
    {"incident_id": 110, "paper_category_type": "ethics_issue", "paper_category": "Privacy"},
    {"incident_id": 38, "paper_category_type": "ethics_issue", "paper_category": "Unethical use (illegal use)"},
    {"incident_id": 48, "paper_category_type": "ethics_issue", "paper_category": "Unethical use (illegal use)"},
    {"incident_id": 92, "paper_category_type": "ethics_issue", "paper_category": "Mental health"},
    {"incident_id": 127, "paper_category_type": "ethics_issue", "paper_category": "Mental health"},
]

KNOWN_PAPER_EXAMPLES = {
    3: "Paper Incident 3 is described as a Starbucks worker monitoring example.",
    5: "Paper Incident 5 is cited as an intelligent service robots example.",
    11: "Paper Incident 11 is described as the Uber self-driving fatality example.",
    14: "Paper Incident 14 is cited as a language/vision example.",
    28: "Paper Incident 28 is described as an iPhone Face ID bypass example.",
    46: "Paper Incident 46 is described as a New Zealand passport checker example.",
    63: "Paper Incident 63 is cited as an intelligent service robots example.",
    64: "Paper Incident 64 is cited as an intelligent service robots example.",
    70: "Paper Incident 70 is discussed in the paper's authentication-process examples.",
    91: "Paper Incident 91 is cited as an AI supervision example.",
    114: "Paper Incident 114 is cited as an intelligent service robots example.",
    123: "Paper Incident 123 is cited as an AI supervision example.",
    131: "Paper Incident 131 is cited as an AI supervision example.",
    133: "Paper Incident 133 is discussed in the paper's authentication-process examples.",
    134: "Paper Incident 134 is cited as a language/vision example.",
    138: "Paper Incident 138 is discussed in the paper's authentication-process examples.",
}


def load_coding_workbook(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path).fillna("")
    frame["incident_id"] = frame["incident_id"].astype(int)
    frame["year"] = frame["year"].astype(int)
    frame["ethics_issues"] = frame[ETHICS_COLUMNS].apply(
        lambda row: [value for value in row.tolist() if value],
        axis=1,
    )
    return frame


def build_single_label_summary(frame: pd.DataFrame, column: str, count_name: str) -> pd.DataFrame:
    total = len(frame)
    summary = (
        frame.groupby(column)["incident_id"]
        .nunique()
        .reset_index(name=count_name)
        .sort_values([count_name, column], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary["share_of_sample"] = (summary[count_name] / total).round(6)
    return summary


def build_ethics_summary(frame: pd.DataFrame) -> pd.DataFrame:
    exploded = frame[["incident_id", "ethics_issues"]].explode("ethics_issues")
    summary = (
        exploded.groupby("ethics_issues")["incident_id"]
        .nunique()
        .reset_index(name="incident_count")
        .rename(columns={"ethics_issues": "ethics_issue"})
        .sort_values(["incident_count", "ethics_issue"], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary["share_of_sample"] = (summary["incident_count"] / frame["incident_id"].nunique()).round(6)
    return summary


def build_taxonomy_fit_summary(frame: pd.DataFrame) -> pd.DataFrame:
    order = ["Fits well", "Fits partially", "Does not fit well", "Unclear"]
    summary = build_single_label_summary(frame, "taxonomy_fit", "incident_count")
    summary["sort_order"] = summary["taxonomy_fit"].apply(lambda value: order.index(value) if value in order else len(order))
    summary = summary.sort_values(["sort_order", "taxonomy_fit"]).drop(columns=["sort_order"]).reset_index(drop=True)
    return summary


def build_paper_comparison(
    summary: pd.DataFrame,
    paper_counts: pd.DataFrame,
    *,
    category_type: str,
    category_column: str,
) -> pd.DataFrame:
    paper_subset = (
        paper_counts.loc[paper_counts["category_type"] == category_type, ["category_name", "paper_reported_count"]]
        .rename(columns={"category_name": category_column})
        .copy()
    )
    summary_subset = summary.rename(columns={"incident_count": "project_count"}).copy()
    comparison = paper_subset.merge(summary_subset, on=category_column, how="left")
    comparison["project_count"] = comparison["project_count"].fillna(0).astype(int)
    comparison["share_of_sample"] = comparison["share_of_sample"].fillna(0.0)
    comparison["count_difference"] = comparison["project_count"] - comparison["paper_reported_count"]
    comparison["paper_rank"] = range(1, len(comparison) + 1)

    project_ranks = (
        summary_subset[[category_column, "project_count"]]
        .sort_values(["project_count", category_column], ascending=[False, True])
        .reset_index(drop=True)
    )
    project_ranks["project_rank"] = range(1, len(project_ranks) + 1)
    comparison = comparison.merge(project_ranks[[category_column, "project_rank"]], on=category_column, how="left")
    comparison["project_rank"] = comparison["project_rank"].fillna("").astype(str)
    return comparison[
        [category_column, "project_count", "share_of_sample", "paper_reported_count", "count_difference", "project_rank", "paper_rank"]
    ]


def summarize_anchor_context(rows: list[dict[str, object]]) -> str:
    parts = [f"{row['paper_category_type']}: {row['paper_category']}" for row in rows]
    return "; ".join(parts)


def build_mapping_note(
    paper_incident_number: int,
    current_title: str,
    in_cleaned_snapshot: bool,
    anchor_context: str,
) -> tuple[str, str]:
    if not in_cleaned_snapshot:
        return (
            "Unable to verify",
            "The paper's incident number could not be checked against the current cleaned snapshot because no matching AIID incident ID was present.",
        )

    if paper_incident_number in {3, 11, 28, 46}:
        example_text = KNOWN_PAPER_EXAMPLES[paper_incident_number]
        return (
            "Does not map cleanly",
            f"{example_text} Current AIID incident ID {paper_incident_number} is '{current_title}', so the paper's numbering does not line up with the current public ID space.",
        )

    example_text = KNOWN_PAPER_EXAMPLES.get(
        paper_incident_number,
        f"Paper Incident {paper_incident_number} was cited in the paper's results discussion.",
    )
    return (
        "ID space mismatch likely",
        f"{example_text} Current AIID incident ID {paper_incident_number} is '{current_title}'. This suggests the paper used internal sequence numbers for its 150-case sample rather than stable public AIID IDs. Paper context: {anchor_context}.",
    )


def build_named_incident_mapping_attempts(cleaned: pd.DataFrame) -> pd.DataFrame:
    cleaned_lookup = cleaned.set_index("incident_id")

    grouped_references: dict[int, list[dict[str, object]]] = {}
    for reference in PAPER_NAMED_REFERENCES:
        grouped_references.setdefault(int(reference["incident_id"]), []).append(reference)

    rows: list[dict[str, object]] = []
    for paper_incident_number, references in grouped_references.items():
        in_cleaned_snapshot = paper_incident_number in cleaned_lookup.index
        current_title = str(cleaned_lookup.loc[paper_incident_number, "title"]) if in_cleaned_snapshot else ""
        anchor_context = summarize_anchor_context(references)
        mapping_status, notes = build_mapping_note(
            paper_incident_number,
            current_title,
            in_cleaned_snapshot,
            anchor_context,
        )
        rows.append(
            {
                "paper_incident_number": paper_incident_number,
                "paper_described_example": KNOWN_PAPER_EXAMPLES.get(
                    paper_incident_number,
                    f"Paper Incident {paper_incident_number} was cited in the paper's results discussion.",
                ),
                "current_aiid_incident_id_checked": paper_incident_number,
                "current_aiid_title": current_title,
                "mapping_status": mapping_status,
                "notes": notes,
            }
        )

    attempts = pd.DataFrame(rows)
    return attempts.sort_values("paper_incident_number").reset_index(drop=True)


def share_for_single_label(frame: pd.DataFrame, column: str, category: str) -> tuple[float, int]:
    count = int((frame[column] == category).sum())
    share = round(count / len(frame), 6)
    return share, count


def share_for_multi_label(frame: pd.DataFrame, category: str) -> tuple[float, int]:
    count = int(frame["ethics_issues"].apply(lambda issues: category in issues).sum())
    share = round(count / len(frame), 6)
    return share, count


def build_period_comparison(pre_frame: pd.DataFrame, post_frame: pd.DataFrame) -> pd.DataFrame:
    period_frames = [(PRE_PERIOD, pre_frame), (POST_PERIOD, post_frame)]
    rows: list[dict[str, object]] = []

    for period, frame in period_frames:
        rows.append(
            {
                "period": period,
                "metric": "incident_count",
                "category": "All incidents",
                "value": len(frame),
                "notes": "Count of incidents in this coded sample.",
            }
        )

        for application_area in COMPARE_APPLICATION_AREAS:
            share, count = share_for_single_label(frame, "application_area", application_area)
            rows.append(
                {
                    "period": period,
                    "metric": "share_of_sample",
                    "category": application_area,
                    "value": share,
                    "notes": f"Application area count={count}",
                }
            )

        for ethics_issue in COMPARE_ETHICS_ISSUES:
            share, count = share_for_multi_label(frame, ethics_issue)
            rows.append(
                {
                    "period": period,
                    "metric": "share_of_sample",
                    "category": ethics_issue,
                    "value": share,
                    "notes": f"Ethics issue count={count}",
                }
            )

    taxonomy_fit_summary = build_taxonomy_fit_summary(post_frame)
    for row in taxonomy_fit_summary.itertuples(index=False):
        rows.append(
            {
                "period": POST_PERIOD,
                "metric": "taxonomy_fit_share",
                "category": row.taxonomy_fit,
                "value": row.share_of_sample,
                "notes": f"Count={int(row.incident_count)}",
            }
        )

    return pd.DataFrame(rows)


def write_summary_stats(
    manual: pd.DataFrame,
    extension: pd.DataFrame,
    application_summary: pd.DataFrame,
    ethics_summary: pd.DataFrame,
    geography_summary: pd.DataFrame,
    mapping_attempts: pd.DataFrame,
    taxonomy_fit_summary: pd.DataFrame,
) -> None:
    total_incidents = manual["incident_id"].nunique()
    top_application = application_summary.iloc[0]
    top_ethics = ethics_summary.iloc[0]
    top_geography = geography_summary.iloc[0]

    top_three_country_count = int(
        geography_summary.loc[
            geography_summary["geographic_location"].isin(["United States", "China", "United Kingdom"]),
            "incident_count",
        ].sum()
    )
    global_count = int(
        geography_summary.loc[geography_summary["geographic_location"] == "Global", "incident_count"].sum()
    )

    mismatch_count = int((mapping_attempts["mapping_status"] == "Does not map cleanly").sum())
    id_space_count = int((mapping_attempts["mapping_status"] == "ID space mismatch likely").sum())
    unable_count = int((mapping_attempts["mapping_status"] == "Unable to verify").sum())

    extension_top_app = build_single_label_summary(extension, "application_area", "incident_count").iloc[0]
    extension_fit_lookup = taxonomy_fit_summary.set_index("taxonomy_fit")["incident_count"].to_dict()

    summary_lines = [
        "# Summary Stats",
        "",
        f"- Manual recreation sample size: {total_incidents}",
        f"- Sample date range: {manual['year'].min()} to {manual['year'].max()}",
        f"- Top application area: {top_application['application_area']} ({int(top_application['incident_count'])} incidents, {top_application['share_of_sample']:.1%})",
        f"- Top ethics issue: {top_ethics['ethics_issue']} ({int(top_ethics['incident_count'])} incidents, {top_ethics['share_of_sample']:.1%})",
        f"- Most common geography label: {top_geography['geographic_location']} ({int(top_geography['incident_count'])} incidents, {top_geography['share_of_sample']:.1%})",
        f"- United States + China + United Kingdom incidents: {top_three_country_count} of {total_incidents}",
        "- Paper reference point: the paper reports 89 of 150 incidents in the United States, China, and the United Kingdom.",
        f"- Global incidents in this recreation: {global_count}",
        "- Paper reference point: the paper reports 40 global incidents.",
        f"- Paper-named incident mapping attempts recorded: {len(mapping_attempts)}",
        f"- Does not map cleanly cases: {mismatch_count}",
        f"- ID space mismatch likely cases: {id_space_count}",
        f"- Mapping attempts missing from the current public snapshot: {unable_count}",
        f"- Post-2021 extension sample size: {extension['incident_id'].nunique()}",
        f"- Top post-2021 extension application area: {extension_top_app['application_area']} ({int(extension_top_app['incident_count'])} incidents, {extension_top_app['share_of_sample']:.1%})",
        f"- Post-2021 taxonomy fit counts: Fits well={int(extension_fit_lookup.get('Fits well', 0))}, Fits partially={int(extension_fit_lookup.get('Fits partially', 0))}, Does not fit well={int(extension_fit_lookup.get('Does not fit well', 0))}",
        "",
        "Method note:",
        "This summary is based on the reviewed LLM-assisted directed coding sample rather than the archived rule-based classifier attempt.",
        "",
        "Reliability note:",
        "This project does not reproduce the paper's two-coder intercoder reliability design or a completed second coding pass.",
    ]
    SUMMARY_STATS_PATH.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def save_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def save_outputs(
    application_summary: pd.DataFrame,
    ethics_summary: pd.DataFrame,
    geography_summary: pd.DataFrame,
    paper_app_comparison: pd.DataFrame,
    paper_ethics_comparison: pd.DataFrame,
    mapping_attempts: pd.DataFrame,
    pre_post_summary: pd.DataFrame,
    taxonomy_fit_summary: pd.DataFrame,
) -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

    files_to_write = {
        APPLICATION_SUMMARY_PATH: application_summary,
        ETHICS_SUMMARY_PATH: ethics_summary,
        GEOGRAPHIC_SUMMARY_PATH: geography_summary,
        PAPER_APP_COMPARISON_PATH: paper_app_comparison,
        PAPER_ETHICS_COMPARISON_PATH: paper_ethics_comparison,
        PAPER_NAMED_MISMATCH_PATH: mapping_attempts,
        PRE_POST_SUMMARY_PATH: pre_post_summary,
        POST_2021_TAXONOMY_FIT_PATH: taxonomy_fit_summary,
        OUTPUT_TABLES_DIR / "application_area_summary.csv": application_summary,
        OUTPUT_TABLES_DIR / "ethics_issue_summary.csv": ethics_summary,
        OUTPUT_TABLES_DIR / "geographic_summary.csv": geography_summary,
        OUTPUT_TABLES_DIR / "paper_comparison_application_areas.csv": paper_app_comparison,
        OUTPUT_TABLES_DIR / "paper_comparison_ethics_issues.csv": paper_ethics_comparison,
        OUTPUT_TABLES_DIR / "paper_named_incident_id_mismatch_check.csv": mapping_attempts,
        OUTPUT_TABLES_DIR / "pre_post_genai_summary.csv": pre_post_summary,
        OUTPUT_TABLES_DIR / "post_2021_taxonomy_fit_summary.csv": taxonomy_fit_summary,
    }
    for path, frame in files_to_write.items():
        save_csv(frame, path)


def main() -> None:
    manual = load_coding_workbook(MANUAL_CODING_PATH)
    extension = load_coding_workbook(EXTENSION_CODING_PATH)
    paper_counts = pd.read_csv(PAPER_COUNTS_PATH)
    cleaned = pd.read_csv(CLEANED_INCIDENTS_PATH).fillna("")
    sample_ids = set(pd.read_csv(SAMPLE_PATH)["incident_id"].astype(int).tolist())

    application_summary = build_single_label_summary(manual, "application_area", "incident_count")
    ethics_summary = build_ethics_summary(manual)
    geography_summary = build_single_label_summary(manual, "geographic_location", "incident_count")

    paper_app_comparison = build_paper_comparison(
        application_summary,
        paper_counts,
        category_type="application_area",
        category_column="application_area",
    )
    paper_ethics_comparison = build_paper_comparison(
        ethics_summary,
        paper_counts,
        category_type="ethics_issue",
        category_column="ethics_issue",
    )
    mapping_attempts = build_named_incident_mapping_attempts(cleaned)
    pre_post_summary = build_period_comparison(manual, extension)
    taxonomy_fit_summary = build_taxonomy_fit_summary(extension)

    save_outputs(
        application_summary,
        ethics_summary,
        geography_summary,
        paper_app_comparison,
        paper_ethics_comparison,
        mapping_attempts,
        pre_post_summary,
        taxonomy_fit_summary,
    )
    write_summary_stats(
        manual,
        extension,
        application_summary,
        ethics_summary,
        geography_summary,
        mapping_attempts,
        taxonomy_fit_summary,
    )
    print("Saved directed coding summaries, mapping-attempt outputs, and post-2021 extension summaries.")


if __name__ == "__main__":
    main()
