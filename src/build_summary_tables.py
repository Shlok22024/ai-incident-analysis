"""Build manual-coding summary tables for the AI incident analysis project."""

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
PAPER_NAMED_CHECKS_PATH = PROCESSED_DIR / "paper_named_incident_checks.csv"
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

NAMED_INCIDENT_CHECKS: list[dict[str, object]] = [
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


def format_project_category(row: pd.Series, paper_category_type: str) -> str:
    if paper_category_type == "application_area":
        return str(row["application_area"])
    return "; ".join(row["ethics_issues"])


def build_notes(
    title: str,
    in_cleaned_snapshot: bool,
    in_manual_sample: bool,
    agreement: str,
) -> str:
    if not in_cleaned_snapshot:
        return "Incident ID was not present in the current cleaned public snapshot, so this paper anchor could not be checked."
    if not in_manual_sample:
        return f"Current snapshot title: {title}. Present in the public snapshot but outside the reproducible 150-incident manual sample."
    if agreement == "Agree":
        return f"Current snapshot title: {title}. Manual directed coding matched the paper-named category on this checked incident."
    return (
        f"Current snapshot title: {title}. The current public snapshot and this project's coding do not match the paper-named "
        "category, which likely reflects AIID drift, different incident descriptions, or sample-selection differences."
    )


def build_named_incident_checks(manual: pd.DataFrame, cleaned: pd.DataFrame, sample_ids: set[int]) -> pd.DataFrame:
    manual_lookup = manual.set_index("incident_id")
    cleaned_lookup = cleaned.set_index("incident_id")

    rows: list[dict[str, object]] = []
    for check in NAMED_INCIDENT_CHECKS:
        incident_id = int(check["incident_id"])
        paper_category_type = str(check["paper_category_type"])
        paper_category = str(check["paper_category"])
        in_cleaned_snapshot = incident_id in cleaned_lookup.index
        in_manual_sample = incident_id in sample_ids

        project_category = ""
        agreement = "Not checked"
        title = ""

        if in_cleaned_snapshot:
            title = str(cleaned_lookup.loc[incident_id, "title"])

        if in_manual_sample:
            manual_row = manual_lookup.loc[incident_id]
            project_category = format_project_category(manual_row, paper_category_type)
            if paper_category_type == "application_area":
                agreement = "Agree" if project_category == paper_category else "Disagree"
            else:
                agreement = "Agree" if paper_category in manual_row["ethics_issues"] else "Disagree"
        elif in_cleaned_snapshot:
            agreement = "Outside sample"
        else:
            agreement = "Missing from snapshot"

        rows.append(
            {
                "incident_id": incident_id,
                "paper_category_type": paper_category_type,
                "paper_category": paper_category,
                "project_category": project_category,
                "agreement": agreement,
                "notes": build_notes(title, in_cleaned_snapshot, in_manual_sample, agreement),
            }
        )

    checks = pd.DataFrame(rows)
    return checks.sort_values(["paper_category_type", "paper_category", "incident_id"]).reset_index(drop=True)


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
    named_checks: pd.DataFrame,
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

    checked_subset = named_checks.loc[named_checks["agreement"].isin(["Agree", "Disagree"])].copy()
    agreement_count = int((checked_subset["agreement"] == "Agree").sum())
    checked_count = len(checked_subset)
    outside_sample_count = int((named_checks["agreement"] == "Outside sample").sum())
    missing_snapshot_count = int((named_checks["agreement"] == "Missing from snapshot").sum())

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
        f"- Named paper incident checks with in-sample project labels: {agreement_count} agrees out of {checked_count} checked anchors",
        f"- Named paper anchors outside the reproducible sample: {outside_sample_count}",
        f"- Named paper anchors missing from the current public snapshot: {missing_snapshot_count}",
        f"- Post-2021 extension sample size: {extension['incident_id'].nunique()}",
        f"- Top post-2021 extension application area: {extension_top_app['application_area']} ({int(extension_top_app['incident_count'])} incidents, {extension_top_app['share_of_sample']:.1%})",
        f"- Post-2021 taxonomy fit counts: Fits well={int(extension_fit_lookup.get('Fits well', 0))}, Fits partially={int(extension_fit_lookup.get('Fits partially', 0))}, Does not fit well={int(extension_fit_lookup.get('Does not fit well', 0))}",
        "",
        "Method note:",
        "This summary is based on the directed manual-coding recreation sample rather than the archived rule-based classifier attempt.",
        "",
        "Reliability note:",
        "This project does not reproduce the paper's two-coder intercoder reliability design.",
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
    named_checks: pd.DataFrame,
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
        PAPER_NAMED_CHECKS_PATH: named_checks,
        PRE_POST_SUMMARY_PATH: pre_post_summary,
        POST_2021_TAXONOMY_FIT_PATH: taxonomy_fit_summary,
        OUTPUT_TABLES_DIR / "application_area_summary.csv": application_summary,
        OUTPUT_TABLES_DIR / "ethics_issue_summary.csv": ethics_summary,
        OUTPUT_TABLES_DIR / "geographic_summary.csv": geography_summary,
        OUTPUT_TABLES_DIR / "paper_comparison_application_areas.csv": paper_app_comparison,
        OUTPUT_TABLES_DIR / "paper_comparison_ethics_issues.csv": paper_ethics_comparison,
        OUTPUT_TABLES_DIR / "paper_named_incident_checks.csv": named_checks,
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
    named_checks = build_named_incident_checks(manual, cleaned, sample_ids)
    pre_post_summary = build_period_comparison(manual, extension)
    taxonomy_fit_summary = build_taxonomy_fit_summary(extension)

    save_outputs(
        application_summary,
        ethics_summary,
        geography_summary,
        paper_app_comparison,
        paper_ethics_comparison,
        named_checks,
        pre_post_summary,
        taxonomy_fit_summary,
    )
    write_summary_stats(
        manual,
        extension,
        application_summary,
        ethics_summary,
        geography_summary,
        named_checks,
        taxonomy_fit_summary,
    )
    print("Saved manual sample summaries, paper comparisons, and post-2021 extension summaries.")


if __name__ == "__main__":
    main()
