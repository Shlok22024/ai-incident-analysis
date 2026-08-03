"""Populate the manual 2010-2021 coding workbook from directed coding decisions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "processed" / "manual_sample_2010_2021.csv"
OUTPUT_PATH = ROOT / "data" / "manual_coding" / "manual_coding_2010_2021.csv"

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
UNCLEAR = "Other or unclear"

MAIN_CODES: dict[int, tuple[str, str, list[str], bool]] = {
    1: (US, IR, [BAD], False),
    2: (US, ISR, [SAFE], False),
    3: (OT, OTH, [SAFE, BAD], True),
    4: (US, AD, [SAFE], False),
    5: (GL, ISR, [SAFE, BAD], False),
    6: (US, LVM, [RACE, GENDER], False),
    7: (GL, AIS, [BAD], True),
    8: (US, AD, [SAFE, BAD], False),
    9: (US, AIE, [UNFAIR, BAD], False),
    10: (US, AIS, [UNFAIR], False),
    11: (US, PP, [RACE, UNFAIR], False),
    12: (GL, LVM, [GENDER], False),
    13: (GL, LVM, [RACE, GENDER], False),
    14: (GL, LVM, [RACE, GENDER], False),
    16: (US, LVM, [RACE], False),
    17: (GL, LVM, [BAD], False),
    18: (GL, LVM, [GENDER], False),
    19: (GL, IR, [RACE, GENDER], False),
    20: (US, AD, [SAFE], False),
    21: (GL, LVM, [BAD], True),
    22: (US, IR, [SAFE, BAD], False),
    23: (US, AD, [SAFE], False),
    24: (OT, ISR, [SAFE], False),
    25: (US, AD, [SAFE], False),
    26: (OT, IA, [ILLEGAL, PRIV], False),
    28: (US, SF, [BAD], False),
    29: (UN, LVM, [BAD], False),
    30: (US, ISR, [BAD], True),
    31: (OT, AD, [SAFE, BAD], False),
    32: (GL, IA, [PRIV], True),
    33: (US, SMH, [BAD], False),
    34: (US, SMH, [BAD], False),
    35: (UN, AIS, [UNFAIR], False),
    36: (CN, IA, [BAD, PRIV], False),
    37: (US, AIR, [GENDER, UNFAIR], False),
    38: (UK, AIG, [BAD], False),
    39: (US, LVM, [ILLEGAL], False),
    40: (US, PP, [BAD], False),
    41: (US, LVM, [BAD], False),
    45: (GL, IR, [BAD], False),
    46: (US, SMH, [SAFE, BAD], False),
    47: (US, IR, [GENDER], False),
    48: (OT, IA, [RACE, BAD], False),
    49: (GL, LVM, [RACE], False),
    50: (GL, SF, [ILLEGAL], False),
    51: (US, ISR, [SAFE], False),
    52: (US, AD, [SAFE], False),
    53: (US, LVM, [RACE], False),
    54: (US, PP, [RACE], False),
    55: (US, SMH, [BAD], False),
    56: (UN, LVM, [BAD], True),
    57: (OT, SF, [BAD, UNFAIR], False),
    58: (OT, LVM, [RACE], False),
    59: (GL, LVM, [GENDER], False),
    60: (GL, LVM, [RACE], False),
    61: (GL, LVM, [BAD], False),
    62: (US, LVM, [BAD], True),
    63: (UN, LVM, [BAD], True),
    64: (UK, ISR, [BAD], False),
    65: (GL, AIG, [BAD], False),
    66: (CN, LVM, [BAD], False),
    67: (US, AD, [SAFE], False),
    68: (US, ISR, [BAD], False),
    69: (OT, ISR, [SAFE], False),
    70: (OT, AD, [BAD], False),
    71: (US, AD, [SAFE], False),
    72: (OT, LVM, [BAD], False),
    73: (US, AIG, [RACE], False),
    74: (US, IA, [RACE, BAD, PRIV], False),
    75: (OT, IR, [RACE], False),
    76: (OT, IA, [RACE, BAD, PRIV], False),
    77: (US, ISR, [BAD, SAFE], False),
    78: (GL, AIE, [UNFAIR, BAD], False),
    80: (UK, OTH, [BAD], True),
    81: (GL, SH, [RACE, GENDER], False),
    82: (OT, AIS, [BAD], False),
    83: (GL, AIS, [RACE, BAD], False),
    84: (US, AIS, [BAD], False),
    85: (GL, LVM, [BAD], True),
    86: (OT, AIE, [UNFAIR, BAD], False),
    87: (UK, IA, [RACE, GENDER, BAD], False),
    88: (GL, LVM, [RACE], False),
    89: (OT, IR, [BAD], True),
    91: (US, SH, [UNFAIR], False),
    92: (US, SF, [GENDER, UNFAIR], False),
    93: (US, IR, [RACE, GENDER], False),
    94: (OT, AIS, [UNFAIR], False),
    95: (US, AIR, [PRIV, UNFAIR], False),
    96: (US, AIE, [UNFAIR], False),
    97: (UN, AD, [BAD], True),
    98: (US, ISR, [PRIV], True),
    99: (US, AIE, [RACE, UNFAIR], False),
    100: (OT, SF, [UNFAIR, BAD], False),
    101: (OT, SF, [RACE, UNFAIR], False),
    102: (GL, LVM, [RACE, BAD], False),
    103: (GL, LVM, [RACE, GENDER], False),
    104: (US, SH, [RACE, UNFAIR], False),
    105: (US, AD, [SAFE], False),
    106: (OT, LVM, [RACE, GENDER], False),
    107: (CN, IA, [RACE, PRIV], False),
    108: (US, IA, [RACE, BAD], False),
    109: (GL, IA, [PRIV, ILLEGAL], False),
    110: (US, SH, [UNFAIR, BAD], False),
    111: (US, AIS, [UNFAIR], False),
    112: (US, PP, [BAD], False),
    113: (US, LVM, [RACE], False),
    114: (US, IA, [RACE, BAD], False),
    115: (GL, LVM, [GENDER, BAD], False),
    116: (US, AIS, [UNFAIR, BAD], False),
    117: (GL, IR, [RACE], False),
    118: (GL, LVM, [RACE], False),
    119: (OT, AIS, [PRIV, UNFAIR], False),
    120: (GL, LVM, [UNCLEAR], True),
    121: (OT, OTH, [SAFE, ILLEGAL], True),
    122: (US, IA, [PRIV], False),
    123: (US, SH, [BAD], False),
    124: (US, SH, [RACE, UNFAIR], False),
    125: (US, ISR, [SAFE], False),
    126: (UK, ISR, [SAFE, BAD], False),
    127: (US, AIS, [RACE, BAD], False),
    128: (US, AD, [BAD], False),
    129: (GL, AIS, [BAD], False),
    131: (US, AIE, [PRIV, UNFAIR], False),
    132: (GL, AIS, [BAD, MENTAL], False),
    133: (GL, AIS, [RACE, GENDER], False),
    134: (CN, ISR, [SAFE, BAD], False),
    135: (US, AIE, [UNFAIR], False),
    136: (GL, AIS, [BAD], True),
    137: (OT, SF, [UNFAIR, PRIV], False),
    138: (US, AIE, [PRIV, RACE, BAD], False),
    139: (US, IR, [BAD], False),
    140: (OT, AIE, [PRIV, RACE, BAD], False),
    141: (US, AIS, [ILLEGAL], False),
    142: (US, AIS, [BAD], False),
    143: (GL, AIS, [BAD], False),
    144: (GL, AIS, [BAD], False),
    145: (US, AD, [BAD], False),
    146: (US, LVM, [RACE], False),
    147: (GL, SF, [ILLEGAL], False),
    148: (GL, OTH, [ILLEGAL], True),
    149: (US, SF, [BAD], False),
    150: (OT, SH, [BAD, SAFE], False),
    151: (US, AD, [SAFE], False),
    152: (OT, ISR, [BAD], False),
    153: (US, AD, [SAFE], False),
    155: (US, IR, [SAFE, BAD], False),
    157: (US, AIS, [SAFE], False),
    158: (US, AIE, [RACE, BAD], False),
    159: (GL, AD, [ILLEGAL], True),
    160: (US, SMH, [SAFE], False),
}


def expand_ethics(issues: list[str]) -> list[str]:
    padded = issues[:4] + [""] * max(0, 4 - len(issues))
    return padded[:4]


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    sample_ids = sample["incident_id"].tolist()
    coded_ids = sorted(MAIN_CODES)

    missing = sorted(set(sample_ids) - set(coded_ids))
    extra = sorted(set(coded_ids) - set(sample_ids))
    if missing or extra:
        raise ValueError(f"Manual code coverage mismatch. Missing={missing}; Extra={extra}")

    rows: list[dict[str, object]] = []
    for row in sample.itertuples(index=False):
        geography, application_area, ethics_issues, uncertainty_flag = MAIN_CODES[int(row.incident_id)]
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
                "ethics_issue_notes": "",
                "evidence_notes": row.title,
                "coder": "ai_assisted_directed_coding",
                "coding_pass": "pass1",
                "uncertainty_flag": uncertainty_flag,
            }
        )

    coded = pd.DataFrame(rows)
    coded.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved directed manual coding draft to {OUTPUT_PATH.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
