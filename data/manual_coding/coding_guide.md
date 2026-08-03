# Coding Guide

This guide applies the paper's published taxonomy to a reproducible AIID sample.

Important framing:
- The original paper derived the taxonomy through conventional content analysis.
- This project applies the published taxonomy through LLM-assisted directed coding.
- AI-assisted coding suggestions were reviewed and accepted by the project author before retaining labels.
- Application area is coded as a single primary label.
- Ethics issue is coded as multi-label.
- Use `Other or unclear` only when the incident genuinely does not fit a paper category with confidence.

## Application Areas

### Intelligent service robots
Physical or embodied service systems such as warehouse robots, delivery robots, assistive robots, or robotic surgical systems.
Edge case: Use this when the robot itself is the primary deployment context, not just because a company owns robots.

### Language/vision model
Systems centered on chatbots, text generation, translation, sentiment analysis, search ranking from language understanding, or image recognition/generation.
Edge case: Use this when the model itself is the main application area, not just when a broader sector incident mentions AI-generated content.

### Autonomous driving
Self-driving cars, autopilot systems, robotaxis, or related vehicle autonomy incidents.

### Intelligent recommendation
Recommendation, feed ranking, app ranking, personalization, or suggestion systems.

### Identity authentication
Facial recognition, biometric verification, or identity-check systems used to verify or match a person.

### AI supervision
Worker monitoring, productivity tracking, algorithmic management, content moderation oversight, or state/corporate supervision systems.

### Smart healthcare
Healthcare, diagnosis, treatment, triage, medical risk scoring, or hospital-care systems.

### AI recruitment
Hiring, applicant screening, resume scoring, or interview-assessment systems.

### Predictive policing
Crime prediction, police targeting, recidivism scoring, sentencing support, or criminal-justice decision systems.

### Smart finance
Banking, credit, insurance, lending, or financial-risk systems.

### AI game
Game-playing or game-related AI systems.

### Smart home
Home assistants, connected home devices, or domestic automation.

### AI education
Proctoring, grading, student evaluation, or education-focused AI systems.

### Other or unclear
Use only when no published category fits well enough to support a single primary label.

## Ethics Issue Categories

### Inappropriate use (bad performance)
The AI system performs poorly, generates incorrect outputs, or fails in deployment.

### Racial discrimination
The incident disproportionately harms or stereotypes people by race or ethnicity.

### Physical safety
The incident causes or risks bodily harm, injury, death, or dangerous physical outcomes.

### Unfair algorithm (evaluation)
The system evaluates, scores, ranks, or decides unfairly in ways that affect people or opportunities.

### Gender discrimination
The incident disproportionately harms or stereotypes people by gender or sex.

### Privacy
The incident involves privacy invasion, surveillance, consent failure, or inappropriate data exposure.

### Unethical use (illegal use)
The technology is used for fraud, illegal abuse, exploitation, or other clearly unethical misuse.

### Mental health
The incident causes or is strongly linked to emotional distress, self-harm risk, or mental-health harm.

### Other or unclear
Use only when the harm does not fit a published ethics category with confidence.

## Geography

Use one geography label per incident:
- United States
- China
- United Kingdom
- Global
- Other country/region
- Unknown or unclear

Use `Global` when the incident clearly spans multiple countries or is framed as cross-border.

## Evidence Notes

Keep notes short and practical:
- Mention the phrase or fact that justified the application area
- Note why each ethics label was chosen
- Flag ambiguous incidents in `uncertainty_flag`

## Reliability Note

This is a single-author portfolio workflow. It does not reproduce the paper's two-coder reliability design. No second independent coding pass was completed, so this project does not report intercoder reliability metrics.
