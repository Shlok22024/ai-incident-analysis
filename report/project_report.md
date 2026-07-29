# Project Report

## Background
AI governance discussions often focus on principles such as fairness, safety, privacy, and accountability. Those principles are important, but they can still feel abstract. This project looks at the other side of the problem: real incidents where AI systems caused or nearly caused harm in practice.

I built this as a small reproduction and update project based on the paper "AI Ethics Issues in Real World: Evidence from AI Incident Database" by Mengyi Wei and Zhixuan Zhou. The goal was not to produce a perfect academic replication. The goal was to create a readable, reproducible portfolio project that shows what kinds of harms appear in real-world incident reporting.

## Research question
Main question: What kinds of real-world problems show up most often when AI systems fail or cause harm?

Secondary question: Did the rise of generative AI change the types of AI incidents being reported?

## Data
The main data source is the AI Incident Database (AIID). For reproducibility, this project uses the public weekly snapshot dated July 27, 2026, which was accessed on July 29, 2026.

The raw AIID extract used here contains 1,597 incidents. After filtering to incidents from 2010 onward and standardizing the fields used for analysis, the cleaned dataset contains 1,581 incidents covering 2010 to 2026.

The project also records the paper source, the snapshot page, and the exact archive URL in `data/raw/source_documents_log.csv`.

## Method
The original paper analyzed 150 incidents and assigned application areas and ethics categories through manual content analysis. The public AIID snapshot does not include those original hand-coded labels. Because of that, I used a transparent rule-based recreation instead of claiming an exact replication.

The workflow was:

1. Download a stable AIID snapshot.
2. Extract and clean the incident table.
3. Recreate application-area labels and ethics-issue labels from public text fields.
4. Count incidents by recreated category.
5. Compare the recreated counts with the paper's reported counts.
6. Compare incidents before 2023 with incidents from 2023 onward.

The 2023 cutoff is a practical way to separate the recent generative-AI period from the earlier period. It should not be treated as a precise causal boundary.

## Results
The recreated dataset includes 1,581 incidents. The largest named recreated application area is Language/vision model with 477 incidents, or 30.2% of the cleaned dataset. The largest recreated ethics issue is Unethical use (illegal use) with 623 incidents, or 39.4%.

Other prominent recreated application areas include AI education (144 incidents), Smart finance (117), and AI supervision (90). Other prominent recreated ethics issues include Inappropriate use (bad performance) with 291 incidents, Privacy with 148, Physical safety with 143, and Unfair algorithm (evaluation) with 139.

Compared with the paper, the current recreated counts are much larger and the mix of categories looks different. That is expected because the database is much larger now, the time window extends to 2026, and this project uses transparent public-field rules rather than the paper's original manual coding.

## What changed after 2023?
The cleaned dataset contains 511 incidents before 2023 and 1,070 incidents from 2023 onward.

In this recreated update, the share of incidents involving Language/vision model systems rose from 8.6% before 2023 to 40.5% from 2023 onward. The share of incidents involving misinformation or manipulation related content rose from 10.4% to 56.4%. Privacy was relatively stable, moving from 10.0% to 9.1%, while discrimination-related incidents declined from 6.3% to 1.7% in this recreated rule set.

The most important interpretation is that the reported incident mix looks different after 2023. More of the reported incidents in the later period involve language/vision systems, generated media, and manipulation-style behavior. This is a descriptive pattern in the incident data, not proof of a direct causal effect.

## Limitations
The AI Incident Database changes over time, and the original paper's exact hand-coded labels may not be available in the current public snapshot. This project is a reproduction-oriented update, not a perfect copy of the original paper.

The public database does not include the paper's exact hand-coded labels, so this project recreates the analysis using available AIID fields and a simplified mapping.

This means the recreated counts depend on the text rules defined in `data/processed/category_mapping.csv`. Some incidents fit multiple possible categories, and many newer incidents do not map cleanly onto the paper's original categories. The database is also not a complete record of all AI harms. It is a useful reported-incident source, not a census of everything that goes wrong with AI.

## What I learned
The main takeaway is that AI harms are not one single problem. In this recreated update, harms show up through misuse, bad performance, privacy issues, discrimination, safety failures, and a strong post-2023 shift toward language/vision and manipulation-style incidents.

For a portfolio project, this was a helpful reminder that governance rules and real incidents answer different questions. Rules tell us what should happen. Incident data shows what repeatedly goes wrong in deployment.
