"""Recreate application-area and ethics-issue categories from public AIID fields."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "incidents_cleaned.csv"
RULE_OUTPUT_PATH = ROOT / "data" / "processed" / "category_mapping.csv"
MAPPING_OUTPUT_PATH = ROOT / "data" / "processed" / "incident_categories_recreated.csv"


APPLICATION_RULES = [
    {
        "category": "AI education",
        "whole_word_triggers": [
            "proctor",
            "exam",
            "classroom",
            "grading",
            "school district",
            "homework",
            "admissions algorithm",
            "student success",
            "education department",
            "school policy",
            "teacher evaluation",
            "teacher ratings",
        ],
        "reason": "Matched education-related deployment terms.",
    },
    {
        "category": "AI recruitment",
        "whole_word_triggers": [
            "resume screening",
            "job applicant",
            "interview screening",
            "recruitment",
            "recruit",
            "hiring",
            "resume",
            "cv",
        ],
        "reason": "Matched hiring or candidate-screening terms.",
    },
    {
        "category": "AI supervision",
        "whole_word_triggers": [
            "employee monitoring",
            "worker monitoring",
            "workplace surveillance",
            "algorithmic manager",
            "productivity tracking",
            "employee productivity",
            "staff monitoring",
            "gig worker",
            "delivery driver",
            "shift scheduling",
            "warehouse worker",
            "automated termination",
            "employee evaluation",
            "worker evaluation",
            "gig work",
        ],
        "reason": "Matched worker supervision or algorithmic management terms.",
    },
    {
        "category": "Predictive policing",
        "whole_word_triggers": [
            "predictive policing",
            "sentencing",
            "recidivism",
            "parole",
            "probation",
            "criminal justice",
            "mugshot",
            "crime prediction",
            "shotspotter",
            "risk of reoffending",
            "police facial recognition",
        ],
        "reason": "Matched policing or criminal-justice terms.",
    },
    {
        "category": "Identity authentication",
        "whole_word_triggers": [
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
        "whole_word_triggers": [
            "self-driving",
            "autonomous vehicle",
            "driverless",
            "autopilot",
            "robotaxi",
            "autonomous mode",
            "cruise vehicle",
            "waymo",
            "tesla full self-driving",
        ],
        "reason": "Matched autonomous-driving terms.",
    },
    {
        "category": "Smart healthcare",
        "whole_word_triggers": [
            "hospital",
            "clinic",
            "diagnostic",
            "radiology",
            "nurse",
            "physician",
            "oncology",
            "cancer treatment",
            "surgery",
            "surgical",
            "health risk score",
            "medical record",
            "triage",
            "false diagnosis",
            "healthcare provider",
        ],
        "reason": "Matched healthcare or clinical terms.",
    },
    {
        "category": "Smart finance",
        "whole_word_triggers": [
            "banking",
            "bank manager",
            "credit score",
            "loan",
            "mortgage",
            "stock exchange",
            "financial services",
            "taxpayer",
            "claim payout",
            "welfare benefits",
            "insurance claim",
            "auto-insurance",
            "investment",
            "trading bot",
        ],
        "reason": "Matched finance, insurance, or trading terms.",
    },
    {
        "category": "Intelligent recommendation",
        "whole_word_triggers": [
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
        "whole_word_triggers": [
            "llm",
            "large language model",
            "language model",
            "chatgpt",
            "gpt",
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
            "openai",
            "llama",
            "midjourney",
            "stable diffusion",
        ],
        "reason": "Matched language-model, chatbot, or computer-vision terms.",
    },
    {
        "category": "Smart home",
        "whole_word_triggers": [
            "smart home",
            "home assistant",
            "alexa",
            "siri",
            "google home",
            "ring doorbell",
            "thermostat",
        ],
        "reason": "Matched home-assistant or smart-home terms.",
    },
    {
        "category": "AI game",
        "whole_word_triggers": ["video game", "game ai", "gaming", "game bot", "npc", "esports"],
        "reason": "Matched gaming-related AI terms.",
    },
    {
        "category": "Intelligent service robots",
        "whole_word_triggers": [
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
        "whole_word_triggers": [
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
        "stem_triggers": ["discriminat"],
        "reason": "Matched race, ethnicity, or antisemitism discrimination terms.",
    },
    {
        "category": "Gender discrimination",
        "whole_word_triggers": [
            "gender discrimination",
            "sex discrimination",
            "sexist",
            "gender bias",
            "bias against women",
            "bias against female",
            "homophobic",
            "transphobic",
        ],
        "stem_triggers": ["misogyn", "discriminat"],
        "reason": "Matched sex, gender, or sexuality discrimination terms.",
    },
    {
        "category": "Physical safety",
        "whole_word_triggers": [
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
        "whole_word_triggers": [
            "risk assessment",
            "credit score",
            "algorithmic rating",
            "teacher evaluation",
            "grading system",
            "evaluation algorithm",
            "eligibility",
            "benefit denial",
            "denied service",
            "screening algorithm",
            "admissions algorithm",
            "resume screening",
            "scoring",
            "ranking applicants",
        ],
        "reason": "Matched automated evaluation, scoring, or eligibility terms.",
    },
    {
        "category": "Privacy",
        "whole_word_triggers": [
            "privacy",
            "surveillance",
            "monitor students",
            "data collection",
            "personal data",
            "biometric data",
            "without consent",
            "data exposure",
            "data leak",
            "private information",
            "sensitive data",
        ],
        "reason": "Matched privacy, surveillance, or data-protection terms.",
    },
    {
        "category": "Unethical use (illegal use)",
        "whole_word_triggers": [
            "deepfake",
            "fraud",
            "scam",
            "phishing",
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
        "stem_triggers": ["impersonat"],
        "reason": "Matched fraud, malicious misuse, or adversarial exploitation terms.",
    },
    {
        "category": "Mental health",
        "whole_word_triggers": [
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
        "whole_word_triggers": [
            "failed",
            "failure",
            "incorrect",
            "inaccurate",
            "malfunction",
            "bug",
            "error",
            "poor performance",
            "outage",
            "disruption",
        ],
        "stem_triggers": ["hallucinat", "misclassif"],
        "reason": "Matched poor performance, malfunction, or incorrect-output terms.",
    },
]


def make_whole_word_pattern(trigger: str) -> str:
    return rf"(?<!\w){re.escape(trigger.strip())}(?!\w)"


def make_stem_pattern(trigger: str) -> str:
    return rf"\b{re.escape(trigger.strip())}"


def first_matching_trigger(
    text: str,
    whole_word_triggers: list[str] | None = None,
    stem_triggers: list[str] | None = None,
) -> str | None:
    for trigger in whole_word_triggers or []:
        if re.search(make_whole_word_pattern(trigger), text):
            return trigger
    for trigger in stem_triggers or []:
        if re.search(make_stem_pattern(trigger), text):
            return trigger
    return None


def write_rule_table() -> None:
    rows: list[dict[str, str]] = []
    for rule in APPLICATION_RULES:
        trigger_text = " | ".join(rule.get("whole_word_triggers", []))
        stem_text = " | ".join(rule.get("stem_triggers", []))
        rows.append(
            {
                "source_field": "text_for_classification",
                "source_value": " | ".join(part for part in [trigger_text, stem_text] if part),
                "mapped_ethics_issue": "",
                "mapped_application_area": rule["category"],
                "mapping_reason": rule["reason"],
            }
        )
    for rule in ETHICS_RULES:
        trigger_text = " | ".join(rule.get("whole_word_triggers", []))
        stem_text = " | ".join(rule.get("stem_triggers", []))
        rows.append(
            {
                "source_field": "text_for_classification",
                "source_value": " | ".join(part for part in [trigger_text, stem_text] if part),
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
        trigger = first_matching_trigger(
            text,
            whole_word_triggers=rule.get("whole_word_triggers"),
            stem_triggers=rule.get("stem_triggers"),
        )
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
        trigger = first_matching_trigger(
            text,
            whole_word_triggers=rule.get("whole_word_triggers"),
            stem_triggers=rule.get("stem_triggers"),
        )
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
