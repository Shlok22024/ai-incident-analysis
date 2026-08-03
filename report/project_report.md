# Project Report

## Background
AI governance conversations often focus on principles such as fairness, safety, privacy, and accountability. Those principles matter, but they can still feel abstract. This project looks at the other side of the problem: reported incidents where AI systems caused or nearly caused harm in practice.

I built this as a small portfolio reproduction and update based on the paper "AI Ethics Issues in Real World: Evidence from AI Incident Database" by Mengyi Wei and Zhixuan Zhou. The goal is not to claim a perfect academic replication. The goal is to understand how the paper works, recreate its coding structure honestly, and update the picture with newer incidents.

## What the paper did
The paper analyzed 150 AI Incident Database incidents from 2010 to 2021. It used manual qualitative content analysis and coded four attributes: time, geography, application area, and ethics issue. Application area was single-label, while ethics issue was multi-label. The paper reported 13 application areas and 8 ethics issue categories, and its published results came from manual coding rather than an automated classifier.

## What this project recreates
This project recreates the paper's coding structure rather than its exact coding process. It applies the paper's published categories to a reproducible public AIID sample, adds geography, compares the resulting distribution with the paper's reported counts, and then tests the same category frame on a small post-2021 extension sample.

## Important method differences
- The paper derived and applied its categories through two-coder manual qualitative coding.
- This project uses LLM-assisted directed coding suggestions reviewed and accepted by one author.
- No second independent coding pass was completed.
- The project does not reproduce the paper's intercoder reliability design.
- The public paper does not fully reveal the exact original 150-case selection rule.

## Sample selection
The paper states that it analyzed 150 incidents from 2010 to 2021, but the exact public selection rule is not recoverable from the paper alone. To keep this project reproducible, I used a deterministic rule:

1. Filter to the target year range.
2. Keep incidents with non-empty title, description, and date fields.
3. Sort by `incident_id`.
4. Take the first `150` incidents for the main sample and the first `50` incidents for the post-2021 extension.

This is an approximation of the paper's incident set, not proof that the samples match the authors' original internal workflow.

## LLM-Assisted Directed Coding Method
The paper derived its taxonomy through conventional content analysis. This project instead applies the already-published taxonomy through LLM-assisted directed coding.

For the 2010-2021 sample, I retained:

- geography
- one primary application area
- up to four ethics issue labels

For the post-2021 extension, I used the same fields and added a `taxonomy_fit` judgment with these outcomes:

- `Fits well`
- `Fits partially`
- `Does not fit well`
- `Unclear`

AI assistance was used for repository scaffolding, code generation, review support, draft organization, and preliminary coding suggestions. Final category assignments, evidence notes, interpretation, and retained outputs were reviewed and accepted by the project author. This project is presented as a single-author LLM-assisted directed coding recreation, not as an exact replication of the paper's two-coder manual content analysis.

## Results
In the 2010-2021 directed coding sample, the most common application area is `Language/vision model` with 32 of 150 incidents. The most common ethics issue is `Inappropriate use (bad performance)` with 75 of 150 incidents. The most common geography label is `United States` with 73 incidents.

At a high level, the geography pattern is reasonably close to the paper. This sample contains 82 incidents in the United States, China, and the United Kingdom combined, compared with the paper's reported 89. It also contains 38 globally framed incidents, compared with the paper's reported 40.

## Comparison with paper
The comparison tables in `data/processed/paper_comparison_application_areas.csv` and `data/processed/paper_comparison_ethics_issues.csv` show that some categories land close to the paper while others shift.

Examples:

- `Autonomous driving` matches the paper's reported count exactly at 17 incidents in this sample.
- `Language/vision model` is somewhat higher here at 32 incidents versus 27 in the paper.
- `Intelligent service robots` is lower here at 14 incidents versus 31 in the paper.

These differences are not surprising. The paper's original coded sample is not public, and this project uses an explicit reproducible rule plus reviewed directed coding on the current public snapshot.

## Failed Named-Incident ID Mapping Attempt
I initially attempted to use paper-named incident numbers as verification anchors. This did not work because the paper's `Incident N` labels do not appear to correspond to stable AIID incident IDs in the current public snapshot.

The mapping attempt file therefore records a reproducibility limitation rather than an agreement score. The paper's incident numbers appear more consistent with internal sequence numbers from its selected 150-case sample than with stable public AIID IDs.

## Post-2021 extension
The extension sample contains 50 incidents from 2022 to 2026. `Language/vision model` becomes even more prominent here, accounting for 17 of 50 incidents. `Unethical use (illegal use)` also becomes much more common than in the 2010-2021 sample.

The taxonomy fit results are:

- `Fits well`: 26 incidents
- `Fits partially`: 15 incidents
- `Does not fit well`: 9 incidents

This suggests the paper's original taxonomy still works for many newer incidents, especially safety, privacy, bias, and evaluation harms. But it is less comfortable for deepfakes, synthetic media misuse, prompt injection, recommendation-driven misinformation, and other generative-AI incidents that were less central in the 2010-2021 period.

## Negative result from keyword automation
An earlier version of this project used transparent keyword rules across the full public AIID snapshot. That approach was reproducible, but it was not methodologically aligned with the paper because the paper used manual qualitative coding. The archived experiment is kept in `experiments/rule_based_classifier_attempt/` as a documented negative finding rather than as the main project.

## Limitations
- This project is not the same as the paper's original manual content analysis.
- The exact original sample selection rule from the paper is not public.
- No two-coder intercoder reliability was reproduced.
- No completed second coding pass was carried out.
- The paper's incident numbers cannot be directly mapped to AIID IDs in the current public snapshot.
- LLM-assisted coding may still introduce classification errors.
- The post-2021 extension is a small descriptive follow-on sample, not a causal test of generative AI.
- The AI Incident Database is a useful incident source, not a complete record of all AI harms.

## What I learned
The main lesson is that AI harm is not one single problem. Even in a small reviewed directed-coding sample, the incidents spread across bad performance, discrimination, privacy, safety, unfair evaluation, and misuse.

The extension adds a second lesson: the older taxonomy still explains a lot, but newer generative and synthetic-media incidents reveal category strain. That makes the project more interesting than either a perfect replication claim or a pure automation exercise.
