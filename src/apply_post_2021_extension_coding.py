"""Populate the post-2021 extension workbook from directed coding decisions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "processed" / "post_2021_extension_sample.csv"
OUTPUT_PATH = ROOT / "data" / "manual_coding" / "manual_coding_post_2021_extension.csv"

US = "United States"
CN = "China"
UK = "United Kingdom"
GL = "Global"
OT = "Other country/region"
UN = "Unknown or unclear"

ISR = "Intelligent service robots"
LVM = "Language/vision model"
AD = "Autonomous driving"
IR = "Intelligent recommendation"
IA = "Identity authentication"
AIS = "AI supervision"
SH = "Smart healthcare"
AIR = "AI recruitment"
PP = "Predictive policing"
SF = "Smart finance"
AIG = "AI game"
SMH = "Smart home"
AIE = "AI education"
OTH = "Other or unclear"

BAD = "Inappropriate use (bad performance)"
RACE = "Racial discrimination"
SAFE = "Physical safety"
UNFAIR = "Unfair algorithm (evaluation)"
GENDER = "Gender discrimination"
PRIV = "Privacy"
ILLEGAL = "Unethical use (illegal use)"
MENTAL = "Mental health"

FIT = "Fits well"
PARTIAL = "Fits partially"
POOR = "Does not fit well"

GEN_NOTE = "Synthetic-media or generative-model misuse only partially fits the paper's older ethics taxonomy."
MISINFO_NOTE = "Misinformation or harmful-content amplification is only partially captured by the original taxonomy."
BOUNDARY_NOTE = "The incident sits near the boundary of the paper's categories and was coded with the closest available label."

EXTENSION_CODES: dict[int, tuple[str, str, list[str], str, str, bool]] = {
    154: (US, PP, [RACE, UNFAIR], FIT, "", False),
    156: (US, IR, [MENTAL, ILLEGAL], PARTIAL, MISINFO_NOTE, False),
    168: (GL, IR, [UNFAIR, BAD], FIT, "", False),
    174: (GL, LVM, [ILLEGAL], PARTIAL, GEN_NOTE, False),
    175: (US, AD, [BAD], FIT, "", False),
    176: (US, ISR, [SAFE, BAD], FIT, "", False),
    177: (GL, LVM, [BAD], PARTIAL, BOUNDARY_NOTE, True),
    178: (US, AD, [SAFE, BAD], FIT, "", False),
    179: (GL, LVM, [RACE, GENDER, ILLEGAL], PARTIAL, GEN_NOTE, False),
    181: (US, AD, [BAD], POOR, BOUNDARY_NOTE, True),
    185: (GL, IR, [ILLEGAL, BAD], POOR, MISINFO_NOTE, False),
    187: (US, AD, [SAFE, BAD], FIT, "", False),
    192: (US, AIR, [UNFAIR], FIT, "", False),
    198: (OT, LVM, [ILLEGAL], POOR, MISINFO_NOTE, False),
    203: (US, AIS, [UNFAIR, BAD], FIT, "", False),
    204: (CN, AIS, [UNFAIR, PRIV], FIT, "", False),
    205: (GL, LVM, [ILLEGAL], POOR, MISINFO_NOTE, False),
    221: (OT, AD, [SAFE, BAD], FIT, "", False),
    236: (US, LVM, [ILLEGAL], PARTIAL, GEN_NOTE, False),
    241: (OT, ISR, [SAFE, BAD], FIT, "", False),
    252: (US, ISR, [SAFE, ILLEGAL], PARTIAL, BOUNDARY_NOTE, True),
    253: (US, AD, [BAD], FIT, "", False),
    258: (OT, IA, [PRIV], FIT, "", False),
    259: (GL, LVM, [ILLEGAL, RACE, GENDER], PARTIAL, GEN_NOTE, False),
    262: (GL, LVM, [RACE, GENDER], FIT, "", False),
    264: (UK, AIS, [PRIV, BAD], PARTIAL, BOUNDARY_NOTE, False),
    266: (GL, LVM, [ILLEGAL, MENTAL], POOR, BOUNDARY_NOTE, True),
    271: (US, AD, [SAFE, BAD], FIT, "", False),
    276: (OT, IA, [PRIV, ILLEGAL], FIT, "", False),
    277: (GL, LVM, [ILLEGAL], POOR, GEN_NOTE, False),
    278: (GL, LVM, [RACE, BAD], FIT, "", False),
    285: (OT, LVM, [BAD], FIT, "", False),
    290: (OT, OTH, [BAD, SAFE], POOR, BOUNDARY_NOTE, True),
    293: (US, AD, [SAFE, BAD], FIT, "", False),
    300: (GL, IR, [GENDER, BAD], PARTIAL, MISINFO_NOTE, False),
    301: (US, AIE, [UNFAIR, PRIV], FIT, "", False),
    303: (US, AIS, [PRIV, BAD], FIT, "", False),
    313: (GL, LVM, [BAD], PARTIAL, MISINFO_NOTE, False),
    314: (GL, LVM, [ILLEGAL, PRIV], POOR, GEN_NOTE, False),
    339: (GL, AIE, [ILLEGAL], PARTIAL, GEN_NOTE, False),
    349: (US, AIS, [SAFE, BAD], FIT, "", False),
    350: (US, ISR, [BAD], PARTIAL, BOUNDARY_NOTE, True),
    351: (GL, LVM, [RACE, ILLEGAL], PARTIAL, GEN_NOTE, False),
    352: (GL, LVM, [ILLEGAL, BAD], PARTIAL, GEN_NOTE, False),
    369: (US, LVM, [UNFAIR], POOR, BOUNDARY_NOTE, True),
    372: (GL, IA, [BAD, PRIV], FIT, "", False),
    377: (CN, AIS, [BAD], PARTIAL, BOUNDARY_NOTE, True),
    378: (US, AD, [SAFE, BAD], FIT, "", False),
    383: (US, SMH, [RACE, BAD], FIT, "", False),
    384: (OT, AIS, [UNFAIR, BAD], FIT, "", False),
}


def expand_ethics(issues: list[str]) -> list[str]:
    padded = issues[:4] + [""] * max(0, 4 - len(issues))
    return padded[:4]


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    sample_ids = sample["incident_id"].tolist()
    coded_ids = sorted(EXTENSION_CODES)

    missing = sorted(set(sample_ids) - set(coded_ids))
    extra = sorted(set(coded_ids) - set(sample_ids))
    if missing or extra:
        raise ValueError(f"Extension code coverage mismatch. Missing={missing}; Extra={extra}")

    rows: list[dict[str, object]] = []
    for row in sample.itertuples(index=False):
        geography, application_area, ethics_issues, taxonomy_fit, new_issue_notes, uncertainty_flag = EXTENSION_CODES[
            int(row.incident_id)
        ]
        ethics_1, ethics_2, ethics_3, ethics_4 = expand_ethics(ethics_issues)
        rows.append(
            {
                "incident_id": row.incident_id,
                "title": row.title,
                "year": row.year,
                "geographic_location": geography,
                "application_area": application_area,
                "ethics_issue_1": ethics_1,
                "ethics_issue_2": ethics_2,
                "ethics_issue_3": ethics_3,
                "ethics_issue_4": ethics_4,
                "taxonomy_fit": taxonomy_fit,
                "new_issue_notes": new_issue_notes,
                "evidence_notes": row.title,
                "coder": "ai_assisted_directed_coding",
                "coding_pass": "pass1",
                "uncertainty_flag": uncertainty_flag,
            }
        )

    coded = pd.DataFrame(rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    coded.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved directed extension coding draft to {OUTPUT_PATH.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
