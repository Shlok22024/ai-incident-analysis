# Manual Sample Selection Log

## Goal
Recreate the paper's 2010-2021 incident analysis with a reproducible 150-incident sample.

## Selection rule used in this project
- Filter the cleaned AIID incident table to incidents dated from 2010 through 2021.
- Keep incidents with non-empty title, description, and date fields.
- Sort the eligible incidents by incident_id and take the first 150.

## Why this differs from the paper
- The paper states that 150 incidents from 2010-2021 were analyzed, but the exact public selection rule is not fully recoverable from the paper alone.
- This project therefore uses an explicit deterministic rule so another reader can rebuild the exact same sample.

## Limitation
- This is a reproducible approximation of the paper's incident set, not proof that it matches the authors' original 150-incident sample.
