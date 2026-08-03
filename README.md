# What Actually Goes Wrong With AI?

_A simple reproduction and update of an AI incident database study_

## What this project is
This project recreates and extends a paper about real-world AI incidents.

The original paper manually coded 150 incidents from the AI Incident Database (AIID). I recreated that approach by manually coding a reproducible 2010-2021 sample using the paper's published categories, then applied the same categories to a small post-2021 sample to see whether they still fit newer incidents.

## Why I did it
After studying AI governance rules in an earlier project, I wanted to look at the other side of the problem: what actually goes wrong when AI systems are deployed.

Rules show what organizations are supposed to do.
Incident databases show what can go wrong in practice.

## Paper studied
This project studies:

- Mengyi Wei and Zhixuan Zhou, "AI Ethics Issues in Real World: Evidence from AI Incident Database"
- HICSS 2023

In the paper, the authors manually analyzed 150 AIID incidents from 2010 to 2021 and coded four attributes: time, geography, application area, and ethics issue. They then reported a 13-category application-area taxonomy and an 8-category ethics-issue taxonomy grounded in those incidents. The paper's main contribution is not a predictive model. It is a qualitative taxonomy of recurring real-world AI harms.

## What the original paper did
- Used 150 incidents from 2010 to 2021
- Used manual content analysis
- Coded time, geography, application area, and ethics issue
- Used single-label application areas and multi-label ethics issues
- Reported 13 application areas and 8 ethics issue categories
- Used two coders and reported intercoder reliability

## What I recreated
- Used the public AIID snapshot recorded in this repo
- Filtered incidents to 2010-2021
- Selected a reproducible 150-incident sample using an explicit deterministic rule
- Applied the paper's published taxonomy through directed content analysis
- Manually coded geography, application area, and ethics issues
- Compared the resulting counts with the paper's reported counts
- Checked paper-named incident IDs where the current public snapshot still makes that possible
- Added a separate 50-incident post-2021 extension sample to test taxonomy fit

## Important differences from the paper
- The paper's exact incident selection rule is not fully recoverable from the public text, so this project uses a transparent deterministic rule instead.
- The paper derived its taxonomy through conventional content analysis. This project applies the already-published taxonomy through directed content analysis.
- This project does not reproduce the paper's two-coder reliability design.
- The current public AIID snapshot does not reliably preserve the same incident-ID meanings used in the paper, so named incident spot-checks reveal substantial drift.
- This is a portfolio reproduction and update, not a perfect academic replication.

## What I found
For the 2010-2021 manual recreation sample:

- Top application area: `Language/vision model` with 32 of 150 incidents (21.3%)
- Top ethics issue: `Inappropriate use (bad performance)` with 75 of 150 incidents (50.0%)
- Most common geography label: `United States` with 73 of 150 incidents (48.7%)
- `United States + China + United Kingdom` account for 82 of 150 incidents in this recreation, compared with the paper's reported 89 of 150
- `Global` accounts for 38 incidents, close to the paper's reported 40

The paper comparison tables also show where this recreation lines up and where it does not. For example, autonomous driving matches the paper's reported count exactly in this sample (`17`), while language/vision models are somewhat higher (`32` here vs `27` in the paper) and intelligent service robots are lower (`14` here vs `31` in the paper).

The named incident spot-check file is useful as a limitation check. Only 8 of 46 in-sample paper anchors matched the current public snapshot's incident IDs and this project's resulting labels. That does not mean the paper is wrong. It strongly suggests that AIID incident numbering and record content have drifted since the paper's analysis.

## Extension: do the old categories still fit newer incidents?
For the post-2021 extension sample of 50 incidents:

- `Language/vision model` becomes even more prominent at 17 of 50 incidents (34.0%)
- `Unethical use (illegal use)` rises from 6.0% of the 2010-2021 sample to 32.0% of the extension sample
- The taxonomy fit check shows 26 incidents that fit the original taxonomy well, 15 that fit partially, and 9 that do not fit well

The main takeaway from the extension is that the paper's taxonomy still works for many newer incidents, especially bias, privacy, safety, and evaluation harms. But it strains on synthetic media, deepfakes, prompt-injection misuse, recommendation-driven misinformation, and other generative-AI cases that do not map neatly onto the older categories.

## Negative result: why I moved away from keyword automation
An earlier version of this project tried to approximate the paper's manual coding with transparent keyword rules across the full public AIID snapshot. That approach was reproducible, but it was not methodologically equivalent to the paper. Keyword rules created false positives, and the resulting rankings were sensitive to rule design and record wording.

I kept that attempt as an archived experiment in [experiments/rule_based_classifier_attempt/README.md](experiments/rule_based_classifier_attempt/README.md) because it helps explain why the final project uses manual coding instead.

## Charts
The main chart files are generated into `outputs/figures/`:

- `manual_application_areas.png`
- `manual_ethics_issues.png`
- `manual_geographic_distribution.png`
- `paper_comparison.png`
- `post_2021_taxonomy_fit.png`
- `portfolio_summary_card.png`

## How to reproduce
```bash
python src/load_aiid_data.py
python src/clean_incidents.py
python src/select_manual_sample.py
python src/build_manual_coding_template.py
python src/apply_manual_coding.py
python src/select_post_2021_extension_sample.py
python src/apply_post_2021_extension_coding.py
python src/build_summary_tables.py
python src/make_charts.py
```

## Method transparency
AI assistance was used for repository scaffolding, code generation, review support, draft organization, and first-pass coding support. The retained outputs are presented as a directed coding recreation and extension, not as a claim of exact replication or two-coder academic reliability.
