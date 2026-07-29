# What Actually Goes Wrong With AI?

## A simple reproduction and update of an AI incident database study

## What this project is
This project studies real-world AI incidents using the AI Incident Database. An AI incident is a case where an AI system caused or nearly caused harm. The goal is to understand what kinds of problems show up most often.

## Why I did it
After studying AI governance rules, I wanted to look at the other side: actual AI failures and harms. Rules tell us what should happen. Incidents show us what can go wrong.

## Paper studied
This project is based on the paper "AI Ethics Issues in Real World: Evidence from AI Incident Database" by Mengyi Wei and Zhixuan Zhou (HICSS 2023).

The paper examines reported AI incidents and groups them into application areas and ethical issue categories. It uses the AI Incident Database as evidence for understanding how AI harms appear in practice. This project recreates the core counting logic in a simplified, transparent way and then updates the analysis using newer public records where possible.

## What I tried to recreate
- Application areas
- Ethics issue categories
- Incident counts
- Updated trends using newer data

## What I found
Results will be added after the data has been collected, cleaned, mapped, and summarized.

Planned placeholders:
- Total incidents analyzed: pending
- Top issue category: pending
- Top application area: pending
- Main pre/post-2023 comparison: pending

## Important limitation
The AI Incident Database changes over time, and the original paper's exact hand-coded labels may not be available in the current public snapshot. This project is a reproduction-oriented update, not a perfect copy of the original paper.

## How I did it
1. Downloaded a stable AIID snapshot.
2. Cleaned incident records.
3. Mapped incidents into issue categories and application areas.
4. Compared the results with the paper.
5. Looked at how incidents changed before and after 2023.

## Charts
Charts will be added after the analysis is complete. Planned outputs:

- `outputs/figures/top_ethics_issues.png`
- `outputs/figures/top_application_areas.png`
- `outputs/figures/incidents_by_year.png`
- `outputs/figures/pre_post_genai_comparison.png`
- `outputs/figures/portfolio_summary_card.png`

## How to reproduce
```bash
python src/load_aiid_data.py
python src/clean_incidents.py
python src/classify_incidents.py
python src/build_summary_tables.py
python src/make_charts.py
```

## Method transparency
AI assistance was used for repository scaffolding, code generation, source-search support, and draft organization. Coding decisions, category mappings, and interpretation were reviewed by the project author.
