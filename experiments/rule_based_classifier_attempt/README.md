# Rule-Based Classifier Attempt

Before pivoting to manual coding, this project tested whether the paper's content analysis could be approximated with transparent keyword rules.

That experiment was useful as a learning exercise, but it was not a faithful recreation of the paper's method. The paper used manual qualitative coding, while this experiment used an automated text-rule instrument. I keep it here as a documented negative result because it explains why the final project uses manual coding.

## What the experiment did
- Loaded a stable AIID snapshot
- Cleaned incident records
- Applied rule-based keyword labels for application areas and ethics issues
- Generated summary tables and charts from those automated labels

## Why it was tempting
It produced clean code, deterministic outputs, and a simple reproducible pipeline. For a portfolio project, that made it appealing as an initial approach.

## What broke
- Keyword rules created false positives
- Rule order affected category rankings
- Many incidents contained mixed signals or needed human interpretation
- The method was not equivalent to the paper's manual content analysis

## Why it is not the main recreation
The paper's published findings came from manually coded incidents, not an automated classifier. Because of that, the main project now uses directed manual coding with the paper's published categories.

## What I learned
The failed automation attempt was still useful. It clarified why manual coding mattered in the original paper and why honest reproduction sometimes means changing direction instead of polishing the wrong method.
