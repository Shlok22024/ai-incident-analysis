"""Generate portfolio-friendly charts for the AI incident analysis project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "outputs" / "figures"

APPLICATION_SUMMARY_PATH = PROCESSED_DIR / "application_area_summary.csv"
ETHICS_SUMMARY_PATH = PROCESSED_DIR / "ethics_issue_summary.csv"
PRE_POST_SUMMARY_PATH = PROCESSED_DIR / "pre_post_genai_summary.csv"
INCIDENTS_PATH = PROCESSED_DIR / "incidents_cleaned.csv"
SUMMARY_STATS_PATH = PROCESSED_DIR / "summary_stats.md"

BACKGROUND = "#f7f4ec"
INK = "#1f2430"
ACCENT = "#d96b3b"
ACCENT_DARK = "#8c3b22"
SECONDARY = "#2c6e63"
GOLD = "#c89b3c"
GRID = "#d8d0c3"


def set_theme() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.facecolor": BACKGROUND,
            "axes.facecolor": BACKGROUND,
            "axes.edgecolor": GRID,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.titleweight": "bold",
            "axes.titlesize": 18,
            "axes.labelsize": 12,
            "font.size": 11,
        }
    )


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]]:
    application_summary = pd.read_csv(APPLICATION_SUMMARY_PATH)
    ethics_summary = pd.read_csv(ETHICS_SUMMARY_PATH)
    pre_post_summary = pd.read_csv(PRE_POST_SUMMARY_PATH)
    incidents = pd.read_csv(INCIDENTS_PATH)
    summary_stats = SUMMARY_STATS_PATH.read_text(encoding="utf-8").splitlines()
    return application_summary, ethics_summary, pre_post_summary, incidents, summary_stats


def style_axes(ax: plt.Axes) -> None:
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)


def annotate_bar_counts(ax: plt.Axes, is_horizontal: bool = True, suffix: str = "") -> None:
    for patch in ax.patches:
        value = patch.get_width() if is_horizontal else patch.get_height()
        if value <= 0.01:
            continue
        if is_horizontal:
            ax.text(
                patch.get_width() + max(ax.get_xlim()[1] * 0.01, 1),
                patch.get_y() + patch.get_height() / 2,
                f"{int(round(value))}{suffix}",
                va="center",
                ha="left",
                fontsize=10,
                color=INK,
            )
        else:
            ax.text(
                patch.get_x() + patch.get_width() / 2,
                patch.get_height() + max(ax.get_ylim()[1] * 0.01, 0.5),
                f"{value:.0f}{suffix}",
                va="bottom",
                ha="center",
                fontsize=10,
                color=INK,
            )


def chart_top_application_areas(application_summary: pd.DataFrame) -> None:
    chart_data = (
        application_summary.loc[application_summary["application_area"] != "Other or unclear"]
        .head(10)
        .sort_values("incident_count")
    )

    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    sns.barplot(data=chart_data, x="incident_count", y="application_area", color=SECONDARY, ax=ax)
    ax.set_title("Top Recreated Primary Application Areas\nExcluding 'Other or unclear'")
    ax.set_xlabel("Incident count")
    ax.set_ylabel("")
    style_axes(ax)
    annotate_bar_counts(ax, is_horizontal=True)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "top_application_areas.png", bbox_inches="tight")
    plt.close(fig)


def chart_top_ethics_issues(ethics_summary: pd.DataFrame) -> None:
    chart_data = (
        ethics_summary.loc[ethics_summary["ethics_issue"] != "Other or unclear"]
        .head(8)
        .sort_values("incident_count")
    )

    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    sns.barplot(data=chart_data, x="incident_count", y="ethics_issue", color=ACCENT, ax=ax)
    ax.set_title("Top Recreated AI Incident Issues\nExcluding 'Other or unclear'")
    ax.set_xlabel("Incident count")
    ax.set_ylabel("")
    style_axes(ax)
    annotate_bar_counts(ax, is_horizontal=True)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "top_ethics_issues.png", bbox_inches="tight")
    plt.close(fig)


def chart_incidents_by_year(incidents: pd.DataFrame) -> None:
    year_counts = (
        incidents.groupby("incident_year")["incident_id"]
        .nunique()
        .reset_index(name="incident_count")
        .sort_values("incident_year")
    )

    fig, ax = plt.subplots(figsize=(13, 7), dpi=200)
    ax.plot(year_counts["incident_year"], year_counts["incident_count"], color=SECONDARY, linewidth=3)
    ax.fill_between(year_counts["incident_year"], year_counts["incident_count"], color=SECONDARY, alpha=0.15)
    ax.axvline(2023, color=ACCENT_DARK, linestyle="--", linewidth=2)
    ax.text(2023.2, year_counts["incident_count"].max() * 0.92, "2023 cutoff", color=ACCENT_DARK, fontsize=11)
    ax.set_title("Reported AI Incidents in the Cleaned Dataset by Year")
    ax.set_xlabel("Incident year")
    ax.set_ylabel("Incident count")
    ax.set_xlim(year_counts["incident_year"].min(), year_counts["incident_year"].max())
    style_axes(ax)
    fig.text(
        0.01,
        0.01,
        "Note: The 2026 count is partial because the snapshot was collected in July 2026.",
        fontsize=10,
        color=INK,
    )
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "incidents_by_year.png", bbox_inches="tight")
    plt.close(fig)


def chart_pre_post_comparison(pre_post_summary: pd.DataFrame) -> None:
    share_data = pre_post_summary.loc[pre_post_summary["metric"] == "share_of_incidents"].copy()
    share_data["value"] = share_data["value"].astype(float) * 100
    share_data["period"] = share_data["period"].replace(
        {
            "Pre-generative-AI period (before 2023)": "Before 2023",
            "Generative-AI period (2023 onward)": "2023 onward",
        }
    )

    category_order = [
        "Language/vision or generative-AI terms",
        "Misinformation or manipulation",
        "Harmful content",
        "Privacy",
        "Discrimination",
    ]
    share_data["category"] = pd.Categorical(share_data["category"], categories=category_order, ordered=True)
    share_data = share_data.sort_values("category")

    fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
    sns.barplot(
        data=share_data,
        x="category",
        y="value",
        hue="period",
        palette=[GOLD, ACCENT],
        ax=ax,
    )
    ax.set_title("How the Mix of Reported Incidents Changes After 2023")
    ax.set_xlabel("")
    ax.set_ylabel("Share of incidents")
    ax.yaxis.set_major_formatter(PercentFormatter())
    style_axes(ax)
    ax.legend(title="")
    plt.setp(ax.get_xticklabels(), rotation=18, ha="right")
    annotate_bar_counts(ax, is_horizontal=False, suffix="%")
    fig.text(
        0.01,
        0.01,
        "Note: Uses a practical 2023 cutoff and a separate language/vision or generative-AI involvement flag.",
        fontsize=10,
        color=INK,
    )
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "pre_post_genai_comparison.png", bbox_inches="tight")
    plt.close(fig)


def extract_stat(summary_stats: list[str], prefix: str) -> str:
    for line in summary_stats:
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return "Pending"


def chart_summary_card(summary_stats: list[str]) -> None:
    total_incidents = extract_stat(summary_stats, "- Total incidents analyzed")
    top_app = extract_stat(summary_stats, "- Top recreated application area")
    top_issue = extract_stat(summary_stats, "- Top recreated ethics issue")
    biggest_change = extract_stat(summary_stats, "- Biggest tracked post-2023 share increase")

    fig = plt.figure(figsize=(10, 10), dpi=200, facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    ax.add_patch(plt.Rectangle((0.04, 0.04), 0.92, 0.92, color="#fffaf0", ec=GRID, lw=2))
    ax.add_patch(plt.Rectangle((0.04, 0.88), 0.92, 0.08, color=SECONDARY, ec=SECONDARY))
    ax.text(0.07, 0.92, "What Actually Goes Wrong With AI?", fontsize=24, fontweight="bold", color="white")
    ax.text(
        0.07,
        0.865,
        "A simple reproduction and update of an AI incident database study",
        fontsize=12,
        color=INK,
    )

    card_text = [
        ("Total incidents analyzed", total_incidents),
        ("Top recreated issue label", top_issue),
        ("Top recreated primary application area", top_app),
        ("Biggest post-2023 shift", biggest_change),
    ]

    y = 0.75
    for label, value in card_text:
        ax.text(0.08, y, label.upper(), fontsize=10, fontweight="bold", color=ACCENT_DARK)
        ax.text(0.08, y - 0.055, value, fontsize=15, color=INK, wrap=True)
        y -= 0.16

    ax.text(0.08, 0.18, "Key lesson", fontsize=12, fontweight="bold", color=SECONDARY)
    ax.text(
        0.08,
        0.11,
        "AI harms are not one problem. In this recreated dataset, they show up as misuse,\n"
        "bad performance, privacy issues, discrimination, safety risks, and a sharp post-2023\n"
        "rise in incidents involving language/vision or generative-AI terms.",
        fontsize=13,
        color=INK,
    )
    ax.text(0.08, 0.05, "2026 is a partial year because the snapshot was collected in July 2026.", fontsize=10, color=INK)

    fig.savefig(FIGURES_DIR / "portfolio_summary_card.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    set_theme()
    application_summary, ethics_summary, pre_post_summary, incidents, summary_stats = load_inputs()
    chart_top_application_areas(application_summary)
    chart_top_ethics_issues(ethics_summary)
    chart_incidents_by_year(incidents)
    chart_pre_post_comparison(pre_post_summary)
    chart_summary_card(summary_stats)
    print("Saved five chart outputs to outputs/figures.")


if __name__ == "__main__":
    main()
