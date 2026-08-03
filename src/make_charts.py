"""Generate directed-coding charts for the AI incident analysis project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "outputs" / "figures"

APPLICATION_SUMMARY_PATH = PROCESSED_DIR / "application_area_summary.csv"
ETHICS_SUMMARY_PATH = PROCESSED_DIR / "ethics_issue_summary.csv"
GEOGRAPHIC_SUMMARY_PATH = PROCESSED_DIR / "geographic_summary.csv"
PAPER_APP_COMPARISON_PATH = PROCESSED_DIR / "paper_comparison_application_areas.csv"
PAPER_ETHICS_COMPARISON_PATH = PROCESSED_DIR / "paper_comparison_ethics_issues.csv"
PRE_POST_SUMMARY_PATH = PROCESSED_DIR / "pre_post_genai_summary.csv"
POST_2021_TAXONOMY_FIT_PATH = PROCESSED_DIR / "post_2021_taxonomy_fit_summary.csv"
SUMMARY_STATS_PATH = PROCESSED_DIR / "summary_stats.md"

BACKGROUND = "#f5f0e6"
PANEL = "#fffaf2"
INK = "#22252b"
TEAL = "#2d6a67"
ORANGE = "#cf6b3e"
GOLD = "#b88c38"
BRICK = "#8f3e2e"
GRID = "#d9cebc"

OBSOLETE_FIGURES = [
    "incidents_by_year.png",
    "pre_post_genai_comparison.png",
    "top_application_areas.png",
    "top_ethics_issues.png",
]


def set_theme() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.facecolor": BACKGROUND,
            "axes.facecolor": PANEL,
            "axes.edgecolor": GRID,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.titleweight": "bold",
            "axes.titlesize": 18,
            "axes.labelsize": 12,
            "font.size": 11,
            "savefig.facecolor": BACKGROUND,
            "savefig.edgecolor": BACKGROUND,
        }
    )


def load_inputs() -> dict[str, pd.DataFrame | list[str]]:
    return {
        "application_summary": pd.read_csv(APPLICATION_SUMMARY_PATH),
        "ethics_summary": pd.read_csv(ETHICS_SUMMARY_PATH),
        "geographic_summary": pd.read_csv(GEOGRAPHIC_SUMMARY_PATH),
        "paper_app_comparison": pd.read_csv(PAPER_APP_COMPARISON_PATH),
        "paper_ethics_comparison": pd.read_csv(PAPER_ETHICS_COMPARISON_PATH),
        "pre_post_summary": pd.read_csv(PRE_POST_SUMMARY_PATH),
        "taxonomy_fit_summary": pd.read_csv(POST_2021_TAXONOMY_FIT_PATH),
        "summary_stats": SUMMARY_STATS_PATH.read_text(encoding="utf-8").splitlines(),
    }


def style_axes(ax: plt.Axes) -> None:
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)


def annotate_horizontal(ax: plt.Axes) -> None:
    for patch in ax.patches:
        value = patch.get_width()
        ax.text(
            value + max(ax.get_xlim()[1] * 0.01, 0.4),
            patch.get_y() + patch.get_height() / 2,
            f"{int(round(value))}",
            va="center",
            ha="left",
            fontsize=10,
            color=INK,
        )


def annotate_vertical(ax: plt.Axes) -> None:
    for patch in ax.patches:
        value = patch.get_height()
        ax.text(
            patch.get_x() + patch.get_width() / 2,
            value + max(ax.get_ylim()[1] * 0.02, 0.3),
            f"{int(round(value))}",
            va="bottom",
            ha="center",
            fontsize=10,
            color=INK,
        )


def chart_manual_application_areas(application_summary: pd.DataFrame) -> None:
    chart_data = (
        application_summary.loc[application_summary["application_area"] != "Other or unclear"]
        .sort_values("incident_count")
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=200)
    sns.barplot(data=chart_data, x="incident_count", y="application_area", color=TEAL, ax=ax)
    ax.set_title("Application Areas in the Directed Coding Sample (2010-2021)")
    ax.set_xlabel("Incident count in 150-incident sample")
    ax.set_ylabel("")
    style_axes(ax)
    annotate_horizontal(ax)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "manual_application_areas.png", bbox_inches="tight")
    plt.close(fig)


def chart_manual_ethics_issues(ethics_summary: pd.DataFrame) -> None:
    chart_data = (
        ethics_summary.loc[ethics_summary["ethics_issue"] != "Other or unclear"]
        .sort_values("incident_count")
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=200)
    sns.barplot(data=chart_data, x="incident_count", y="ethics_issue", color=ORANGE, ax=ax)
    ax.set_title("Ethics Issues in the Directed Coding Sample (2010-2021)")
    ax.set_xlabel("Incident count in 150-incident sample")
    ax.set_ylabel("")
    style_axes(ax)
    annotate_horizontal(ax)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "manual_ethics_issues.png", bbox_inches="tight")
    plt.close(fig)


def chart_manual_geography(geographic_summary: pd.DataFrame) -> None:
    chart_data = geographic_summary.sort_values("incident_count")

    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=200)
    sns.barplot(data=chart_data, x="incident_count", y="geographic_location", color=GOLD, ax=ax)
    ax.set_title("Geographic Distribution in the Directed Coding Sample (2010-2021)")
    ax.set_xlabel("Incident count in 150-incident sample")
    ax.set_ylabel("")
    style_axes(ax)
    annotate_horizontal(ax)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "manual_geographic_distribution.png", bbox_inches="tight")
    plt.close(fig)


def plot_grouped_comparison(ax: plt.Axes, frame: pd.DataFrame, category_column: str, title: str) -> None:
    chart_data = frame.copy().sort_values("paper_rank", ascending=False)
    y_positions = range(len(chart_data))
    bar_height = 0.38

    ax.barh(
        [position - bar_height / 2 for position in y_positions],
        chart_data["paper_reported_count"],
        height=bar_height,
        color=BRICK,
        label="Paper",
    )
    ax.barh(
        [position + bar_height / 2 for position in y_positions],
        chart_data["project_count"],
        height=bar_height,
        color=TEAL,
        label="Project sample",
    )

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(chart_data[category_column])
    ax.set_title(title)
    ax.set_xlabel("Incident count")
    ax.set_ylabel("")
    style_axes(ax)


def chart_paper_comparison(
    paper_app_comparison: pd.DataFrame,
    paper_ethics_comparison: pd.DataFrame,
) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(13, 14), dpi=200)
    plot_grouped_comparison(
        axes[0],
        paper_app_comparison,
        "application_area",
        "Comparison With Paper-Reported Counts: Application Areas",
    )
    plot_grouped_comparison(
        axes[1],
        paper_ethics_comparison,
        "ethics_issue",
        "Comparison With Paper-Reported Counts: Ethics Issues",
    )
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.98))
    fig.text(
        0.02,
        0.015,
        "Note: Counts are compared against the paper's reported totals, but the paper's incident numbers do not map cleanly onto the current public AIID ID space.",
        fontsize=10,
        color=INK,
    )
    plt.tight_layout(rect=(0, 0.03, 1, 0.96))
    fig.savefig(FIGURES_DIR / "paper_comparison.png", bbox_inches="tight")
    plt.close(fig)


def chart_taxonomy_fit(taxonomy_fit_summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    ax.bar(
        taxonomy_fit_summary["taxonomy_fit"],
        taxonomy_fit_summary["incident_count"],
        color=[TEAL, GOLD, ORANGE][: len(taxonomy_fit_summary)],
    )
    ax.set_title("Post-2021 Extension: How Well the Original Taxonomy Fits")
    ax.set_xlabel("")
    ax.set_ylabel("Incident count in 50-incident extension sample")
    style_axes(ax)
    annotate_vertical(ax)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "post_2021_taxonomy_fit.png", bbox_inches="tight")
    plt.close(fig)


def extract_stat(summary_stats: list[str], prefix: str) -> str:
    for line in summary_stats:
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return "Pending"


def extract_metric(pre_post_summary: pd.DataFrame, period: str, category: str) -> str:
    match = pre_post_summary.loc[
        (pre_post_summary["period"] == period)
        & (pre_post_summary["metric"] == "share_of_sample")
        & (pre_post_summary["category"] == category),
        "value",
    ]
    if match.empty:
        return "Pending"
    return f"{float(match.iloc[0]) * 100:.1f}%"


def chart_summary_card(summary_stats: list[str], pre_post_summary: pd.DataFrame) -> None:
    total_sample = extract_stat(summary_stats, "- Directed coding sample size")
    top_app = extract_stat(summary_stats, "- Top application area")
    top_issue = extract_stat(summary_stats, "- Top ethics issue")
    taxonomy_fit = extract_stat(summary_stats, "- Post-2021 taxonomy fit counts")
    lvm_pre = extract_metric(pre_post_summary, "2010-2021 directed coding sample", "Language/vision model")
    lvm_post = extract_metric(pre_post_summary, "2022-2026 extension sample", "Language/vision model")
    illegal_pre = extract_metric(pre_post_summary, "2010-2021 directed coding sample", "Unethical use (illegal use)")
    illegal_post = extract_metric(pre_post_summary, "2022-2026 extension sample", "Unethical use (illegal use)")

    fig = plt.figure(figsize=(10, 10), dpi=200, facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    ax.add_patch(
        FancyBboxPatch(
            (0.04, 0.04),
            0.92,
            0.92,
            boxstyle="round,pad=0.012,rounding_size=0.03",
            linewidth=2,
            edgecolor=GRID,
            facecolor=PANEL,
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (0.06, 0.84),
            0.88,
            0.1,
            boxstyle="round,pad=0.015,rounding_size=0.03",
            linewidth=0,
            facecolor=TEAL,
        )
    )
    ax.text(0.09, 0.89, "What Actually Goes Wrong With AI?", fontsize=24, fontweight="bold", color="white")
    ax.text(0.09, 0.845, "LLM-assisted directed coding of a reproducible AIID sample", fontsize=12, color="white")

    cards = [
        ("Directed sample", f"{total_sample} incidents from 2010-2021"),
        ("Top issue", top_issue),
        ("Top application area", top_app),
        ("Post-2021 fit", taxonomy_fit),
    ]

    y = 0.74
    for label, value in cards:
        ax.text(0.09, y, label.upper(), fontsize=10, fontweight="bold", color=BRICK)
        ax.text(0.09, y - 0.055, value, fontsize=15, color=INK, wrap=True)
        y -= 0.14

    ax.text(0.09, 0.15, "Key shifts", fontsize=12, fontweight="bold", color=TEAL)
    ax.text(
        0.09,
        0.095,
        f"Language/vision cases rise from {lvm_pre} to {lvm_post}.\n"
        f"Unethical-use labels rise from {illegal_pre} to {illegal_post}.",
        fontsize=13,
        color=INK,
    )
    ax.text(0.09, 0.055, "Main lesson", fontsize=12, fontweight="bold", color=TEAL)
    ax.text(
        0.09,
        0.02,
        "Older categories still explain many incidents, but generative and synthetic-media harms create visible strain.",
        fontsize=11.5,
        color=INK,
    )

    fig.savefig(FIGURES_DIR / "portfolio_summary_card.png", bbox_inches="tight")
    plt.close(fig)


def remove_obsolete_figures() -> None:
    for filename in OBSOLETE_FIGURES:
        path = FIGURES_DIR / filename
        if path.exists():
            path.unlink()


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    set_theme()
    inputs = load_inputs()

    chart_manual_application_areas(inputs["application_summary"])
    chart_manual_ethics_issues(inputs["ethics_summary"])
    chart_manual_geography(inputs["geographic_summary"])
    chart_paper_comparison(inputs["paper_app_comparison"], inputs["paper_ethics_comparison"])
    chart_taxonomy_fit(inputs["taxonomy_fit_summary"])
    chart_summary_card(inputs["summary_stats"], inputs["pre_post_summary"])
    remove_obsolete_figures()
    print("Saved directed-coding chart outputs to outputs/figures.")


if __name__ == "__main__":
    main()
