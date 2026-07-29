"""Recreate application-area and ethics-issue categories from public AIID fields."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "incidents_cleaned.csv"
RULE_OUTPUT_PATH = ROOT / "data" / "processed" / "category_mapping.csv"
MAPPING_OUTPUT_PATH = ROOT / "data" / "processed" / "incident_categories_recreated.csv"


APPLICATION_RULES = [
    {
        "category": "AI education",
        "triggers": [
            "proctor",
            "exam",
            "teacher",
            "classroom",
            "grading",
            "education",
            "school district",
            "university",
            "homework",
        ],
        "reason": "Matched education-related deployment terms.",
    },
    {
        "category": "AI recruitment",
        "triggers": ["resume", "cv", "recruit", "recruitment", "hiring", "job applicant", "interview screening"],
        "reason": "Matched hiring or candidate-screening terms.",
    },
    {
        "category": "AI supervision",
        "triggers": [
            "employee monitoring",
            "worker monitoring",
            "workplace surveillance",
            "algorithmic manager",
            "productivity tracking",
            "employee productivity",
            "staff monitoring",
            "gig worker",
            "delivery driver",
            "employee",
            "worker",
            "firing",
            "termination",
            "shift scheduling",
            "warehouse worker",
        ],
        "reason": "Matched worker supervision or algorithmic management terms.",
    },
    {
        "category": "Predictive policing",
        "triggers": [
            "predictive policing",
            "police department",
            "law enforcement",
            "sentencing",
            "recidivism",
            "parole",
            "probation",
            "criminal justice",
            "jail",
            "prison",
            "mugshot",
            "crime prediction",
            "shotspotter",
        ],
        "reason": "Matched policing or criminal-justice terms.",
    },
    {
        "category": "Identity authentication",
        "triggers": [
            "facial recognition",
            "face recognition",
            "identity verification",
            "identity check",
            "facial verification",
            "passport checker",
            "biometric",
            "authentication",
        ],
        "reason": "Matched identity verification or biometric authentication terms.",
    },
    {
        "category": "Autonomous driving",
        "triggers": [
            "self-driving",
            "autonomous vehicle",
            "driverless",
            "autopilot",
            "robotaxi",
            "av ",
            "cruise vehicle",
            "waymo",
            "tesla full self-driving",
        ],
        "reason": "Matched autonomous-driving terms.",
    },
    {
        "category": "Smart healthcare",
        "triggers": [
            "patient",
            "hospital",
            "medical",
            "healthcare",
            "clinic",
            "diagnosis",
            "diagnostic",
            "radiology",
            "nurse",
            "physician",
        ],
        "reason": "Matched healthcare or clinical terms.",
    },
    {
        "category": "Smart finance",
        "triggers": [
            "bank",
            "banking",
            "credit",
            "loan",
            "mortgage",
            "insurance",
            "trading",
            "stock exchange",
            "financial",
            "taxpayer",
        ],
        "reason": "Matched finance, insurance, or trading terms.",
    },
    {
        "category": "Intelligent recommendation",
        "triggers": [
            "recommendation",
            "recommender",
            "recommended",
            "ranking algorithm",
            "autocomplete",
            "news feed",
            "feed ranking",
            "content ranking",
            "app store ranking",
            "suggested",
            "ranking order",
            "recommendation engine",
        ],
        "reason": "Matched recommendation, ranking, or personalization terms.",
    },
    {
        "category": "Language/vision model",
        "triggers": [
            "llm",
            "large language model",
            "language model",
            "chatgpt",
            "gpt-",
            "gpt ",
            "chatbot",
            "generative ai",
            "ai-generated",
            "ai generated",
            "generated image",
            "generated video",
            "generated voice",
            "voice clone",
            "synthetic voice",
            "text generator",
            "image generator",
            "vision model",
            "image classification",
            "image classifier",
            "object detection",
            "speech recognition",
            "machine translation",
            "openai model",
            "claude",
            "gemini",
            "llama",
            "midjourney",
            "stable diffusion",
        ],
        "reason": "Matched language-model, chatbot, or computer-vision terms.",
    },
    {
        "category": "Smart home",
        "triggers": ["smart home", "home assistant", "alexa", "siri", "google home", "ring doorbell", "thermostat"],
        "reason": "Matched home-assistant or smart-home terms.",
    },
    {
        "category": "AI game",
        "triggers": ["video game", "game ai", "gaming", "game bot", "npc", "esports"],
        "reason": "Matched gaming-related AI terms.",
    },
    {
        "category": "Intelligent service robots",
        "triggers": [
            "robot",
            "robotic",
            "warehouse automation",
            "delivery robot",
            "drone",
            "manufacturing automation",
            "industrial automation",
        ],
        "reason": "Matched robotics or embodied-system terms.",
    },
]

ETHICS_RULES = [
    {
        "category": "Racial discrimination",
        "triggers": [
            "racial discrimination",
            "racist",
            "racial bias",
            "race bias",
            "anti-semitic",
            "antisemitic",
            "bias against black",
            "bias against asian",
            "bias against hispanic",
            "ethnic bias",
        ],
        "reason": "Matched race, ethnicity, or antisemitism discrimination terms.",
    },
    {
        "category": "Gender discrimination",
        "triggers": [
            "gender discrimination",
            "sex discrimination",
            "sexist",
            "misogyn",
            "gender bias",
            "bias against women",
            "bias against female",
            "homophobic",
            "transphobic",
        ],
        "reason": "Matched sex, gender, or sexuality discrimination terms.",
    },
    {
        "category": "Physical safety",
        "triggers": [
            "killed",
            "injured",
            "injury",
            "fatal",
            "death",
            "died",
            "crash",
            "collision",
            "hospitalized",
            "physical harm",
            "explosion",
        ],
        "reason": "Matched physical harm, collision, or fatality terms.",
    },
    {
        "category": "Unfair algorithm (evaluation)",
        "triggers": [
            "risk assessment",
            "credit score",
            "score people",
            "algorithmic rating",
            "teacher evaluation",
            "grading system",
            "evaluation algorithm",
            "eligibility",
            "benefits",
            "benefit denial",
            "denied service",
            "screening algorithm",
            "admissions algorithm",
            "resume screening",
            "assessment",
            "audit",
            "rating",
            "scoring",
            "flagged",
        ],
        "reason": "Matched automated evaluation, scoring, or eligibility terms.",
    },
    {
        "category": "Privacy",
        "triggers": [
            "privacy",
            "surveillance",
            "tracked",
            "tracking",
            "monitor",
            "monitored",
            "monitor students",
            "data collection",
            "personal data",
            "biometric data",
            "without consent",
            "data exposure",
            "data leak",
        ],
        "reason": "Matched privacy, surveillance, or data-protection terms.",
    },
    {
        "category": "Unethical use (illegal use)",
        "triggers": [
            "deepfake",
            "fraud",
            "scam",
            "phishing",
            "impersonat",
            "spoof",
            "bypass",
            "jailbreak",
            "prompt injection",
            "cyberattack",
            "hack",
            "malware",
            "exploit",
            "stolen",
        ],
        "reason": "Matched fraud, malicious misuse, or adversarial exploitation terms.",
    },
    {
        "category": "Mental health",
        "triggers": [
            "mental health",
            "suicide",
            "suicidal",
            "self-harm",
            "depression",
            "psychological harm",
            "emotional distress",
            "loneliness",
            "manipulate users",
        ],
        "reason": "Matched mental-health or emotional-harm terms.",
    },
    {
        "category": "Inappropriate use (bad performance)",
        "triggers": [
            "failed",
            "failure",
            "incorrect",
            "wrongly",
            "wrong ",
            "inaccurate",
            "malfunction",
            "bug",
            "error",
            "hallucinat",
            "misclassif",
            "poor performance",
            "outage",
            "disruption",
        ],
        "reason": "Matched poor performance, malfunction, or incorrect-output terms.",
    },
]


def first_matching_trigger(text: str, triggers: list[str]) -> str | None:
    for trigger in triggers:
        if trigger in text:
            return trigger
    return None


def write_rule_table() -> None:
    rows: list[dict[str, str]] = []
    for rule in APPLICATION_RULES:
        rows.append(
            {
                "source_field": "text_for_classification",
                "source_value": " | ".join(rule["triggers"]),
                "mapped_ethics_issue": "",
                "mapped_application_area": rule["category"],
                "mapping_reason": rule["reason"],
            }
        )
    for rule in ETHICS_RULES:
        rows.append(
            {
                "source_field": "text_for_classification",
                "source_value": " | ".join(rule["triggers"]),
                "mapped_ethics_issue": rule["category"],
                "mapped_application_area": "",
                "mapping_reason": rule["reason"],
            }
        )

    with RULE_OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_field",
                "source_value",
                "mapped_ethics_issue",
                "mapped_application_area",
                "mapping_reason",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def classify_application_area(text: str) -> tuple[str, str, str]:
    for rule in APPLICATION_RULES:
        trigger = first_matching_trigger(text, rule["triggers"])
        if trigger:
            return rule["category"], trigger, rule["reason"]
    return (
        "Other or unclear",
        "",
        "No application-area trigger matched the public incident text.",
    )


def classify_ethics_issues(text: str) -> list[tuple[str, str, str]]:
    matches: list[tuple[str, str, str]] = []
    for rule in ETHICS_RULES:
        trigger = first_matching_trigger(text, rule["triggers"])
        if trigger:
            matches.append((rule["category"], trigger, rule["reason"]))

    if not matches:
        matches.append(
            (
                "Other or unclear",
                "",
                "No ethics-issue trigger matched the public incident text.",
            )
        )
    return matches


def main() -> None:
    incidents = pd.read_csv(INPUT_PATH)
    write_rule_table()

    mapping_rows: list[dict[str, object]] = []
    for row in incidents.itertuples(index=False):
        incident_text = row.text_for_classification
        application_area, trigger, reason = classify_application_area(incident_text)
        mapping_rows.append(
            {
                "incident_id": row.incident_id,
                "source_field": "text_for_classification",
                "source_value": trigger,
                "mapped_ethics_issue": "",
                "mapped_application_area": application_area,
                "mapping_reason": reason,
            }
        )

        for ethics_issue, ethics_trigger, ethics_reason in classify_ethics_issues(incident_text):
            mapping_rows.append(
                {
                    "incident_id": row.incident_id,
                    "source_field": "text_for_classification",
                    "source_value": ethics_trigger,
                    "mapped_ethics_issue": ethics_issue,
                    "mapped_application_area": "",
                    "mapping_reason": ethics_reason,
                }
            )

    mapping_frame = pd.DataFrame(mapping_rows)
    mapping_frame.to_csv(MAPPING_OUTPUT_PATH, index=False)
    print(
        f"Saved {len(mapping_frame):,} mapping rows to {MAPPING_OUTPUT_PATH.relative_to(ROOT)} "
        f"and the rule table to {RULE_OUTPUT_PATH.relative_to(ROOT)}."
    )


if __name__ == "__main__":
    main()
