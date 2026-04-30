"""Synthetic social psychology experiment simulation.

This script creates toy participant-level and trial-level data for article examples.
It is educational only and not a psychological assessment tool.
"""

from pathlib import Path
import csv
import random

random.seed(42)

participants = [f"P{i:03d}" for i in range(1, 81)]
target_groups = ["ingroup", "outgroup"]
conditions = ["neutral_frame", "threat_frame", "cooperation_frame"]

rows = []
trial_id = 1

for participant in participants:
    identity_bias = random.gauss(0.0, 0.35)

    for trial in range(1, 13):
        target_group = random.choice(target_groups)
        condition = random.choice(conditions)
        schema_consistent = random.choice([0, 1])

        group_shift = 0.45 if target_group == "ingroup" else -0.35
        threat_shift = -0.40 if condition == "threat_frame" else 0.0
        cooperation_shift = 0.35 if condition == "cooperation_frame" else 0.0

        internal_attr = 3.5 + 0.55 * schema_consistent + identity_bias
        external_attr = 3.5 - 0.25 * schema_consistent + random.gauss(0.0, 0.5)

        trust = 4.0 + group_shift + threat_shift + cooperation_shift + random.gauss(0.0, 0.65)
        warmth = 4.0 + group_shift + cooperation_shift + random.gauss(0.0, 0.65)
        competence = 4.0 + 0.20 * schema_consistent + random.gauss(0.0, 0.6)

        response_time_ms = 850 + 80 * schema_consistent + random.gauss(0.0, 120)

        rows.append({
            "trial_id": trial_id,
            "participant": participant,
            "condition": condition,
            "target_group": target_group,
            "schema_consistent": schema_consistent,
            "attribution_internal": round(max(1, min(7, internal_attr)), 3),
            "attribution_external": round(max(1, min(7, external_attr)), 3),
            "trust_rating": round(max(1, min(7, trust)), 3),
            "warmth_rating": round(max(1, min(7, warmth)), 3),
            "competence_rating": round(max(1, min(7, competence)), 3),
            "response_time_ms": round(max(150, response_time_ms), 2),
        })
        trial_id += 1

out = Path(__file__).resolve().parents[1] / "data" / "processed" / "synthetic_social_trials.csv"
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} synthetic social-psychology trials to {out}")
