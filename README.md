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
Using the public AI Incident Database snapshot from July 27, 2026, this project analyzed 1,581 incidents from 2010 to 2026.

- Top recreated primary application area: Language/vision model (623 incidents, 39.4%)
- Top recreated ethics issue label: Unethical use (illegal use) (571 incidents, 36.1%)
- Pre-2023 incident count: 511
- 2023-and-later incident count: 1,070
- Share of incidents involving language/vision or generative-AI terms rose from 21.9% before 2023 to 77.2% from 2023 onward
- Share of misinformation or manipulation related incidents rose from 9.4% before 2023 to 54.4% from 2023 onward

In this rule-based recreated update, the post-2023 period contains many more reported incidents involving language/vision or generative-AI terms, synthetic media, and manipulation-style harms than the earlier period. This is a descriptive comparison using a practical 2023 cutoff, not a causal claim.

The 2026 count is partial because the snapshot was collected in July 2026.

## Important limitation
The AI Incident Database changes over time, and the original paper's exact hand-coded labels may not be available in the current public snapshot. This project is a reproduction-oriented update, not a perfect copy of the original paper.

The public database does not include the paper's exact hand-coded labels, so this project recreates the analysis using available AIID fields and a simplified mapping.

## How I did it
1. Downloaded a stable AIID snapshot dated July 27, 2026.
2. Cleaned incident records.
3. Mapped incidents into rule-based recreated issue categories and primary application areas using transparent text rules.
4. Compared the recreated counts with the paper's reported categories.
5. Looked at how incidents changed before and after 2023 using a separate language/vision or generative-AI involvement flag.

## Charts
### Portfolio summary card
![Portfolio summary card](outputs/figures/portfolio_summary_card.png)

### Incident counts by year
![Incidents by year](outputs/figures/incidents_by_year.png)

### Top recreated primary application areas
![Top application areas](outputs/figures/top_application_areas.png)

### Top recreated AI incident issues
![Top ethics issues](outputs/figures/top_ethics_issues.png)

### Before and after 2023
![Pre/post 2023 comparison](outputs/figures/pre_post_genai_comparison.png)

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
