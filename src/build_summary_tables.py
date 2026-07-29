"""Build summary tables for the recreated AI incident analysis."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_TABLES_DIR = ROOT / "outputs" / "tables"
INCIDENTS_PATH = PROCESSED_DIR / "incidents_cleaned.csv"
MAPPINGS_PATH = PROCESSED_DIR / "incident_categories_recreated.csv"
PAPER_COUNTS_PATH = ROOT / "data" / "raw" / "original_paper_reference_counts.csv"
APPLICATION_SUMMARY_PATH = PROCESSED_DIR / "application_area_summary.csv"
ETHICS_SUMMARY_PATH = PROCESSED_DIR / "ethics_issue_summary.csv"
PRE_POST_SUMMARY_PATH = PROCESSED_DIR / "pre_post_genai_summary.csv"
SUMMARY_STATS_PATH = PROCESSED_DIR / "summary_stats.md"

PRE_PERIOD = "Pre-generative-AI period (before 2023)"
POST_PERIOD = "Generative-AI period (2023 onward)"

MISINFO_TERMS = [
    "misinformation",
    "disinformation",
    "deepfake",
    "fabricated",
    "fabrication",
    "synthetic voice",
    "voice clone",
    "hoax",
    "synthetic media",
]
MISINFO_STEMS = ["impersonat", "deceiv", "manipulat"]
HARMFUL_CONTENT_TERMS = [
    "inappropriate content",
    "harmful content",
    "hate speech",
    "explicit content",
    "sexual content",
    "violent content",
    "toxic content",
    "abusive content",
    "graphic content",
    "porn",
]


def load_incident_frame() -> pd.DataFrame:
    incidents = pd.read_csv(INCIDENTS_PATH)
    mappings = pd.read_csv(MAPPINGS_PATH).fillna("")

    application_map = (
        mappings.loc[mappings["mapped_application_area"] != "", ["incident_id", "mapped_application_area"]]
        .drop_duplicates(subset=["incident_id"])
        .rename(columns={"mapped_application_area": "application_area"})
    )

    ethics_map = mappings.loc[mappings["mapped_ethics_issue"] != "", ["incident_id", "mapped_ethics_issue"]].copy()
    ethics_grouped = (
        ethics_map.groupby("incident_id")["mapped_ethics_issue"]
        .apply(lambda values: sorted(set(values)))
        .reset_index(name="ethics_issues")
    )

    incidents = incidents.merge(application_map, on="incident_id", how="left")
    incidents = incidents.merge(ethics_grouped, on="incident_id", how="left")
    incidents["application_area"] = incidents["application_area"].fillna("Other or unclear")
    incidents["ethics_issues"] = incidents["ethics_issues"].apply(
        lambda value: value if isinstance(value, list) else ["Other or unclear"]
    )
    incidents["ethics_issues_text"] = incidents["ethics_issues"].apply("; ".join)
    return incidents


def build_application_summary(incidents: pd.DataFrame, paper_counts: pd.DataFrame) -> pd.DataFrame:
    total = len(incidents)
    summary = (
        incidents.groupby("application_area")["incident_id"]
        .nunique()
        .reset_index(name="incident_count")
        .sort_values(["incident_count", "application_area"], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary["share"] = summary["incident_count"] / total

    paper_app_counts = (
        paper_counts.loc[paper_counts["category_type"] == "application_area", ["category_name", "paper_reported_count"]]
        .rename(columns={"category_name": "application_area"})
    )
    summary = summary.merge(paper_app_counts, on="application_area", how="left")
    summary["difference_from_paper"] = summary["incident_count"] - summary["paper_reported_count"].fillna(0)
    return summary


def build_ethics_summary(incidents: pd.DataFrame, paper_counts: pd.DataFrame) -> pd.DataFrame:
    ethics_rows = incidents[["incident_id", "ethics_issues"]].explode("ethics_issues")
    total = incidents["incident_id"].nunique()
    summary = (
        ethics_rows.groupby("ethics_issues")["incident_id"]
        .nunique()
        .reset_index(name="incident_count")
        .rename(columns={"ethics_issues": "ethics_issue"})
        .sort_values(["incident_count", "ethics_issue"], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary["share"] = summary["incident_count"] / total

    paper_issue_counts = (
        paper_counts.loc[paper_counts["category_type"] == "ethics_issue", ["category_name", "paper_reported_count"]]
        .rename(columns={"category_name": "ethics_issue"})
    )
    summary = summary.merge(paper_issue_counts, on="ethics_issue", how="left")
    summary["difference_from_paper"] = summary["incident_count"] - summary["paper_reported_count"].fillna(0)
    return summary


def make_whole_word_pattern(term: str) -> str:
    return rf"(?<!\w){re.escape(term.strip())}(?!\w)"


def make_stem_pattern(term: str) -> str:
    return rf"\b{re.escape(term.strip())}"


def has_text_term(text: str, whole_word_terms: list[str], stem_terms: list[str] | None = None) -> bool:
    if any(re.search(make_whole_word_pattern(term), text) for term in whole_word_terms):
        return True
    return any(re.search(make_stem_pattern(term), text) for term in stem_terms or [])


def build_period_metrics(incidents: pd.DataFrame) -> pd.DataFrame:
    incidents = incidents.copy()
    incidents["text_for_classification"] = incidents["text_for_classification"].fillna("")
    incidents["has_privacy"] = incidents["ethics_issues"].apply(lambda issues: "Privacy" in issues)
    incidents["has_discrimination"] = incidents["ethics_issues"].apply(
        lambda issues: "Racial discrimination" in issues or "Gender discrimination" in issues
    )
    incidents["has_misinformation_or_manipulation"] = incidents["text_for_classification"].apply(
        lambda text: has_text_term(text, MISINFO_TERMS, MISINFO_STEMS)
    )
    incidents["has_harmful_content"] = incidents["text_for_classification"].apply(
        lambda text: has_text_term(text, HARMFUL_CONTENT_TERMS)
    )

    rows: list[dict[str, object]] = []
    for period, period_frame in incidents.groupby("pre_post_genai_period", sort=False):
        total = len(period_frame)
        rows.append(
            {
                "period": period,
                "metric": "incident_count",
                "category": "All incidents",
                "value": total,
                "notes": "Total cleaned incidents in this period.",
            }
        )

        for label, column in [
            ("Language/vision or generative-AI terms", "has_language_vision_terms"),
            ("Misinformation or manipulation", "has_misinformation_or_manipulation"),
            ("Harmful content", "has_harmful_content"),
            ("Privacy", "has_privacy"),
            ("Discrimination", "has_discrimination"),
        ]:
            count = int(period_frame[column].sum())
            rows.append(
                {
                    "period": period,
                    "metric": "share_of_incidents",
                    "category": label,
                    "value": round(count / total, 6),
                    "notes": f"Count={count}",
                }
            )

        top_apps = (
            period_frame.groupby("application_area")["incident_id"]
            .nunique()
            .reset_index(name="incident_count")
            .sort_values(["incident_count", "application_area"], ascending=[False, True])
            .head(3)
            .reset_index(drop=True)
        )
        for rank, top_row in enumerate(top_apps.itertuples(index=False), start=1):
            rows.append(
                {
                    "period": period,
                    "metric": "top_application_area",
                    "category": top_row.application_area,
                    "value": int(top_row.incident_count),
                    "notes": f"Rank={rank}; Share={top_row.incident_count / total:.3f}",
                }
            )

    return pd.DataFrame(rows)


def write_summary_stats(
    incidents: pd.DataFrame,
    application_summary: pd.DataFrame,
    ethics_summary: pd.DataFrame,
    pre_post_summary: pd.DataFrame,
) -> None:
    total_incidents = len(incidents)
    min_year = incidents["incident_year"].min()
    max_year = incidents["incident_year"].max()
    top_application = application_summary.iloc[0]
    top_ethics = ethics_summary.iloc[0]

    period_totals = (
        pre_post_summary.loc[pre_post_summary["metric"] == "incident_count", ["period", "value"]]
        .set_index("period")["value"]
        .to_dict()
    )

    metric_shares = pre_post_summary.loc[pre_post_summary["metric"] == "share_of_incidents"].copy()
    metric_shares["value"] = metric_shares["value"].astype(float)
    pre_shares = metric_shares.loc[metric_shares["period"] == PRE_PERIOD].set_index("category")["value"]
    post_shares = metric_shares.loc[metric_shares["period"] == POST_PERIOD].set_index("category")["value"]
    share_changes = (post_shares - pre_shares).sort_values(ascending=False)
    biggest_change_label = share_changes.index[0]
    biggest_change_points = share_changes.iloc[0] * 100

    summary_lines = [
        "# Summary Stats",
        "",
        f"- Total incidents analyzed: {total_incidents:,}",
        f"- Date range covered: {min_year} to {max_year}",
        f"- Source snapshot date: 2026-07-27",
        "- The 2026 count is partial because the snapshot was collected in July 2026.",
        f"- Top recreated application area: {top_application['application_area']} ({int(top_application['incident_count']):,} incidents, {top_application['share']:.1%})",
        f"- Top recreated ethics issue: {top_ethics['ethics_issue']} ({int(top_ethics['incident_count']):,} incidents, {top_ethics['share']:.1%})",
        f"- Pre-2023 incident count: {int(period_totals.get(PRE_PERIOD, 0)):,}",
        f"- 2023-and-later incident count: {int(period_totals.get(POST_PERIOD, 0)):,}",
        (
            "- Biggest tracked post-2023 share increase: "
            f"{biggest_change_label} ({biggest_change_points:+.1f} percentage points)"
        ),
        "",
        "Interpretation note:",
        "These counts come from a transparent rule-based recreation using the public AIID snapshot, not from the paper's original hand-coded labels.",
    ]
    SUMMARY_STATS_PATH.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def save_outputs(application_summary: pd.DataFrame, ethics_summary: pd.DataFrame, pre_post_summary: pd.DataFrame) -> None:
    application_summary.to_csv(APPLICATION_SUMMARY_PATH, index=False)
    ethics_summary.to_csv(ETHICS_SUMMARY_PATH, index=False)
    pre_post_summary.to_csv(PRE_POST_SUMMARY_PATH, index=False)

    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    application_summary.to_csv(OUTPUT_TABLES_DIR / "application_area_summary.csv", index=False)
    ethics_summary.to_csv(OUTPUT_TABLES_DIR / "ethics_issue_summary.csv", index=False)
    pre_post_summary.to_csv(OUTPUT_TABLES_DIR / "pre_post_genai_summary.csv", index=False)


def main() -> None:
    incidents = load_incident_frame()
    paper_counts = pd.read_csv(PAPER_COUNTS_PATH)

    application_summary = build_application_summary(incidents, paper_counts)
    ethics_summary = build_ethics_summary(incidents, paper_counts)
    pre_post_summary = build_period_metrics(incidents)

    save_outputs(application_summary, ethics_summary, pre_post_summary)
    write_summary_stats(incidents, application_summary, ethics_summary, pre_post_summary)
    print("Saved application, ethics, pre/post, and summary stats outputs.")


if __name__ == "__main__":
    main()
