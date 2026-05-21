#!/usr/bin/env python3
"""
Groupthink research model.

This script can:
1. Generate synthetic groupthink decision-process data.
2. Estimate decision-quality, self-censorship, consensus-pressure, forecast-calibration, implementation-risk, and response-time models.
3. Test cohesion, directive leadership, insulation, stress, consensus pressure, dissent visibility, outside information, and safeguards.
4. Simulate repeated decision cycles under high groupthink risk and safeguard interventions.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

try:
    import statsmodels.formula.api as smf
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "control", "directive_leadership", "high_cohesion", "insulated_group",
    "high_stress", "consensus_pressure", "dissent_visible", "devils_advocate",
    "outside_experts", "subgroup_review", "red_team", "second_chance_meeting"
]

CONTEXTS = [
    "laboratory", "executive_team", "policy_committee", "military_staff",
    "board", "platform_team", "scientific_panel", "crisis_cell"
]


def generate_dataset(n_participants: int = 720, trials_per_participant: int = 4, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "control": {"coh": 5.5, "lead": 4.0, "ins": 4.0, "stress": 4.5, "con": 4.5, "self": 3.5, "inv": 3.0, "rat": 3.5, "mor": 4.0, "out": 3.0, "press": 3.0, "mind": 3.0, "diss": 5.5, "info": 5.5, "alt": 5.8, "risk": 5.6, "cont": 5.4, "devil": 0, "expert": 0, "sub": 0, "imp": 5.5, "safe": 5.8, "qual": 62, "cal": 60, "impl": 42, "review": 56},
        "directive_leadership": {"coh": 7.5, "lead": 9.0, "ins": 6.5, "stress": 6.0, "con": 8.0, "self": 7.0, "inv": 6.5, "rat": 7.0, "mor": 7.2, "out": 6.0, "press": 7.5, "mind": 7.0, "diss": 2.5, "info": 3.0, "alt": 2.8, "risk": 2.6, "cont": 2.5, "devil": 0, "expert": 0, "sub": 0, "imp": 2.0, "safe": 2.5, "qual": 36, "cal": 34, "impl": 78, "review": 30},
        "high_cohesion": {"coh": 9.2, "lead": 6.5, "ins": 6.2, "stress": 5.8, "con": 7.5, "self": 6.8, "inv": 6.0, "rat": 6.5, "mor": 7.0, "out": 5.5, "press": 6.2, "mind": 6.0, "diss": 3.0, "info": 3.2, "alt": 3.4, "risk": 3.0, "cont": 3.0, "devil": 0, "expert": 0, "sub": 0, "imp": 4.0, "safe": 3.5, "qual": 42, "cal": 40, "impl": 72, "review": 34},
        "insulated_group": {"coh": 7.0, "lead": 6.5, "ins": 9.0, "stress": 6.5, "con": 7.0, "self": 7.2, "inv": 6.8, "rat": 7.8, "mor": 7.0, "out": 7.2, "press": 6.8, "mind": 8.5, "diss": 2.2, "info": 1.5, "alt": 2.5, "risk": 2.2, "cont": 2.0, "devil": 0, "expert": 0, "sub": 0, "imp": 3.5, "safe": 3.0, "qual": 32, "cal": 30, "impl": 86, "review": 26},
        "high_stress": {"coh": 7.8, "lead": 7.0, "ins": 7.0, "stress": 9.5, "con": 8.2, "self": 7.5, "inv": 8.0, "rat": 7.8, "mor": 8.0, "out": 7.0, "press": 7.8, "mind": 7.2, "diss": 2.5, "info": 2.8, "alt": 2.6, "risk": 2.5, "cont": 2.0, "devil": 0, "expert": 0, "sub": 0, "imp": 3.0, "safe": 2.5, "qual": 30, "cal": 28, "impl": 90, "review": 24},
        "consensus_pressure": {"coh": 8.0, "lead": 7.5, "ins": 7.0, "stress": 6.5, "con": 9.2, "self": 8.5, "inv": 7.0, "rat": 7.4, "mor": 7.6, "out": 6.5, "press": 8.8, "mind": 7.5, "diss": 1.8, "info": 2.5, "alt": 2.0, "risk": 2.2, "cont": 2.0, "devil": 0, "expert": 0, "sub": 0, "imp": 2.8, "safe": 2.0, "qual": 28, "cal": 26, "impl": 88, "review": 22},
        "dissent_visible": {"coh": 6.5, "lead": 3.5, "ins": 3.0, "stress": 5.0, "con": 3.8, "self": 2.2, "inv": 3.0, "rat": 3.0, "mor": 3.5, "out": 3.2, "press": 2.0, "mind": 2.2, "diss": 8.5, "info": 7.5, "alt": 8.0, "risk": 8.0, "cont": 7.5, "devil": 0, "expert": 1, "sub": 0, "imp": 7.5, "safe": 8.2, "qual": 78, "cal": 76, "impl": 32, "review": 74},
        "devils_advocate": {"coh": 6.8, "lead": 3.2, "ins": 3.2, "stress": 5.5, "con": 3.5, "self": 2.0, "inv": 2.8, "rat": 3.0, "mor": 3.2, "out": 3.0, "press": 2.0, "mind": 2.0, "diss": 8.8, "info": 7.8, "alt": 8.5, "risk": 8.2, "cont": 8.0, "devil": 1, "expert": 1, "sub": 0, "imp": 8.0, "safe": 8.5, "qual": 82, "cal": 80, "impl": 28, "review": 78},
        "outside_experts": {"coh": 6.0, "lead": 4.0, "ins": 2.5, "stress": 6.0, "con": 4.0, "self": 2.5, "inv": 3.2, "rat": 3.0, "mor": 3.5, "out": 3.8, "press": 2.5, "mind": 2.5, "diss": 7.8, "info": 9.0, "alt": 8.2, "risk": 8.5, "cont": 8.0, "devil": 0, "expert": 1, "sub": 0, "imp": 7.5, "safe": 8.0, "qual": 84, "cal": 82, "impl": 26, "review": 80},
        "subgroup_review": {"coh": 6.5, "lead": 4.0, "ins": 3.0, "stress": 5.5, "con": 4.2, "self": 2.8, "inv": 3.5, "rat": 3.2, "mor": 3.8, "out": 3.5, "press": 2.8, "mind": 3.0, "diss": 7.5, "info": 8.0, "alt": 8.5, "risk": 8.4, "cont": 8.2, "devil": 0, "expert": 1, "sub": 1, "imp": 7.2, "safe": 7.8, "qual": 86, "cal": 84, "impl": 24, "review": 82},
        "red_team": {"coh": 6.2, "lead": 3.5, "ins": 2.8, "stress": 6.5, "con": 3.8, "self": 2.4, "inv": 3.0, "rat": 3.0, "mor": 3.2, "out": 3.4, "press": 2.2, "mind": 2.4, "diss": 8.8, "info": 8.5, "alt": 9.0, "risk": 9.0, "cont": 8.5, "devil": 1, "expert": 1, "sub": 1, "imp": 8.0, "safe": 8.5, "qual": 88, "cal": 86, "impl": 22, "review": 84},
        "second_chance_meeting": {"coh": 6.8, "lead": 3.8, "ins": 3.5, "stress": 7.0, "con": 4.0, "self": 2.6, "inv": 3.2, "rat": 3.4, "mor": 3.5, "out": 3.6, "press": 2.5, "mind": 2.5, "diss": 8.0, "info": 8.0, "alt": 8.4, "risk": 8.6, "cont": 8.8, "devil": 1, "expert": 1, "sub": 1, "imp": 7.8, "safe": 8.0, "qual": 86, "cal": 84, "impl": 24, "review": 86},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 121):03d}"
        site_id = f"S{rng.integers(1, 41):02d}"
        dissent_trait = float(np.clip(rng.normal(5.0, 1.5), 0, 10))
        hierarchy_sensitivity = float(np.clip(rng.normal(5.0, 1.5), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context = rng.choice(CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 140):03d}"
            e = effects[condition]

            cohesion = float(np.clip(rng.normal(e["coh"], 1.0), 0, 10))
            leadership_directive = float(np.clip(rng.normal(e["lead"], 1.0), 0, 10))
            group_insulation = float(np.clip(rng.normal(e["ins"], 1.0), 0, 10))
            stress_level = float(np.clip(rng.normal(e["stress"], 1.0), 0, 10))
            consensus_pressure = float(np.clip(rng.normal(e["con"], 1.0), 0, 10))
            self_censorship = float(np.clip(rng.normal(0.70 * e["self"] + 0.30 * hierarchy_sensitivity, 1.0), 0, 10))
            illusion_invulnerability = float(np.clip(rng.normal(e["inv"], 1.0), 0, 10))
            collective_rationalization = float(np.clip(rng.normal(e["rat"], 1.0), 0, 10))
            inherent_morality = float(np.clip(rng.normal(e["mor"], 1.0), 0, 10))
            outgroup_stereotyping = float(np.clip(rng.normal(e["out"], 1.0), 0, 10))
            direct_pressure_dissenters = float(np.clip(rng.normal(e["press"], 1.0), 0, 10))
            mindguarding = float(np.clip(rng.normal(e["mind"], 1.0), 0, 10))
            dissent_visibility = float(np.clip(rng.normal(0.75 * e["diss"] + 0.25 * dissent_trait, 1.0), 0, 10))
            outside_information = float(np.clip(rng.normal(e["info"], 1.0), 0, 10))
            alternative_search = float(np.clip(rng.normal(e["alt"], 1.0), 0, 10))
            risk_analysis = float(np.clip(rng.normal(e["risk"], 1.0), 0, 10))
            contingency_planning = float(np.clip(rng.normal(e["cont"], 1.0), 0, 10))
            devils_advocate = int(e["devil"])
            independent_expert_consulted = int(e["expert"])
            subgroup_review = int(e["sub"])
            leader_impartiality = float(np.clip(rng.normal(e["imp"], 1.0), 0, 10))
            psychological_safety = float(np.clip(rng.normal(e["safe"], 1.0), 0, 10))

            perceived_unanimity = float(np.clip(
                45
                + 4.0 * consensus_pressure
                + 3.0 * cohesion
                + 2.5 * leadership_directive
                + 2.0 * self_censorship
                - 3.0 * dissent_visibility
                - 1.5 * psychological_safety
                + rng.normal(0, 7),
                0, 100
            ))

            private_disagreement = float(np.clip(
                20
                + 3.0 * self_censorship
                + 2.5 * stress_level
                + 2.0 * group_insulation
                - 2.0 * dissent_visibility
                + rng.normal(0, 8),
                0, 100
            ))

            groupthink_risk = (
                cohesion
                + leadership_directive
                + group_insulation
                + stress_level
                + consensus_pressure
                + self_censorship
                + illusion_invulnerability
                + collective_rationalization
                + inherent_morality
                + outgroup_stereotyping
                + direct_pressure_dissenters
                + mindguarding
                - dissent_visibility
                - outside_information
                - leader_impartiality
                - psychological_safety
            ) / 8.0

            safeguard_index = (
                dissent_visibility
                + outside_information
                + alternative_search
                + risk_analysis
                + contingency_planning
                + leader_impartiality
                + psychological_safety
                + 2.0 * devils_advocate
                + 2.0 * independent_expert_consulted
                + 2.0 * subgroup_review
            ) / 9.0

            decision_quality = float(np.clip(
                e["qual"]
                - 3.0 * max(groupthink_risk, 0)
                + 3.0 * safeguard_index
                + 1.6 * alternative_search
                + 1.8 * risk_analysis
                + 1.5 * contingency_planning
                - 1.2 * perceived_unanimity / 10.0
                + rng.normal(0, 7),
                0, 100
            ))

            forecast_calibration = float(np.clip(
                e["cal"]
                - 2.5 * max(groupthink_risk, 0)
                + 2.5 * safeguard_index
                + 1.8 * outside_information
                + 1.5 * risk_analysis
                - 1.2 * illusion_invulnerability
                + rng.normal(0, 7),
                0, 100
            ))

            implementation_risk = float(np.clip(
                e["impl"]
                + 3.2 * max(groupthink_risk, 0)
                - 2.0 * safeguard_index
                - 1.4 * contingency_planning
                - 1.4 * risk_analysis
                + rng.normal(0, 7),
                0, 100
            ))

            post_decision_review_quality = float(np.clip(
                e["review"]
                + 2.0 * psychological_safety
                + 1.8 * outside_information
                + 1.8 * leader_impartiality
                + 1.5 * subgroup_review
                - 1.5 * collective_rationalization
                - 1.3 * inherent_morality
                + rng.normal(0, 7),
                0, 100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(900)
                + 0.040 * stress_level
                + 0.030 * consensus_pressure
                + 0.030 * self_censorship
                - 0.025 * alternative_search
                - 0.025 * risk_analysis
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "condition": condition,
                "trial": t,
                "cohesion": round(cohesion, 3),
                "leadership_directive": round(leadership_directive, 3),
                "group_insulation": round(group_insulation, 3),
                "stress_level": round(stress_level, 3),
                "consensus_pressure": round(consensus_pressure, 3),
                "self_censorship": round(self_censorship, 3),
                "illusion_invulnerability": round(illusion_invulnerability, 3),
                "collective_rationalization": round(collective_rationalization, 3),
                "inherent_morality": round(inherent_morality, 3),
                "outgroup_stereotyping": round(outgroup_stereotyping, 3),
                "direct_pressure_dissenters": round(direct_pressure_dissenters, 3),
                "mindguarding": round(mindguarding, 3),
                "dissent_visibility": round(dissent_visibility, 3),
                "outside_information": round(outside_information, 3),
                "alternative_search": round(alternative_search, 3),
                "risk_analysis": round(risk_analysis, 3),
                "contingency_planning": round(contingency_planning, 3),
                "devils_advocate": devils_advocate,
                "independent_expert_consulted": independent_expert_consulted,
                "subgroup_review": subgroup_review,
                "leader_impartiality": round(leader_impartiality, 3),
                "psychological_safety": round(psychological_safety, 3),
                "perceived_unanimity": round(perceived_unanimity, 3),
                "private_disagreement": round(private_disagreement, 3),
                "decision_quality": round(decision_quality, 3),
                "forecast_calibration": round(forecast_calibration, 3),
                "implementation_risk": round(implementation_risk, 3),
                "post_decision_review_quality": round(post_decision_review_quality, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["symptom_index"] = (
        data["illusion_invulnerability"]
        + data["collective_rationalization"]
        + data["inherent_morality"]
        + data["outgroup_stereotyping"]
        + data["self_censorship"]
        + data["direct_pressure_dissenters"]
        + data["mindguarding"]
    ) / 7.0
    data["antecedent_risk_index"] = (
        data["cohesion"]
        + data["leadership_directive"]
        + data["group_insulation"]
        + data["stress_level"]
        + data["consensus_pressure"]
    ) / 5.0
    data["process_quality_index"] = (
        data["dissent_visibility"]
        + data["outside_information"]
        + data["alternative_search"]
        + data["risk_analysis"]
        + data["contingency_planning"]
        + data["leader_impartiality"]
        + data["psychological_safety"]
    ) / 7.0
    data["safeguard_index"] = (
        data["dissent_visibility"]
        + data["outside_information"]
        + data["alternative_search"]
        + data["risk_analysis"]
        + data["contingency_planning"]
        + data["leader_impartiality"]
        + data["psychological_safety"]
        + 2.0 * data["devils_advocate"]
        + 2.0 * data["independent_expert_consulted"]
        + 2.0 * data["subgroup_review"]
    ) / 9.0
    data["unanimity_gap"] = data["perceived_unanimity"] - (100 - data["private_disagreement"])
    data["groupthink_risk_index"] = (
        data["antecedent_risk_index"]
        + data["symptom_index"]
        - data["process_quality_index"]
    )
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "institution_context"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            groups=("group_id", "nunique"),
            mean_groupthink_risk=("groupthink_risk_index", "mean"),
            mean_antecedent_risk=("antecedent_risk_index", "mean"),
            mean_symptoms=("symptom_index", "mean"),
            mean_process_quality=("process_quality_index", "mean"),
            mean_safeguards=("safeguard_index", "mean"),
            mean_unanimity_gap=("unanimity_gap", "mean"),
            mean_self_censorship=("self_censorship", "mean"),
            mean_dissent_visibility=("dissent_visibility", "mean"),
            mean_outside_information=("outside_information", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
            mean_forecast_calibration=("forecast_calibration", "mean"),
            mean_implementation_risk=("implementation_risk", "mean"),
            mean_review_quality=("post_decision_review_quality", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby("condition")
        .agg(
            n=("participant", "size"),
            mean_groupthink_risk=("groupthink_risk_index", "mean"),
            mean_self_censorship=("self_censorship", "mean"),
            mean_unanimity_gap=("unanimity_gap", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
            mean_forecast_calibration=("forecast_calibration", "mean"),
            mean_implementation_risk=("implementation_risk", "mean"),
            mean_safeguards=("safeguard_index", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    condition_summary.to_csv(outputs / "summary_by_condition.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "decision_quality_model": "decision_quality ~ groupthink_risk_index + safeguard_index + cohesion + leadership_directive + group_insulation + stress_level + consensus_pressure + dissent_visibility + outside_information + alternative_search + risk_analysis + contingency_planning + leader_impartiality + psychological_safety + condition + institution_context",
        "self_censorship_model": "self_censorship ~ cohesion + leadership_directive + group_insulation + stress_level + consensus_pressure + dissent_visibility + leader_impartiality + psychological_safety + condition + institution_context",
        "forecast_calibration_model": "forecast_calibration ~ groupthink_risk_index + safeguard_index + outside_information + risk_analysis + illusion_invulnerability + collective_rationalization + condition + institution_context",
        "implementation_risk_model": "implementation_risk ~ groupthink_risk_index + symptom_index + risk_analysis + contingency_planning + outside_information + safeguard_index + condition + institution_context",
        "response_time_model": "log_response_time ~ stress_level + consensus_pressure + self_censorship + alternative_search + risk_analysis + condition + institution_context",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        model = smf.ols(formula, data=data).fit(
            cov_type="cluster", cov_kwds={"groups": data["group_id"]}
        )
        model_text.append(f"\n\n=== {name} ===\n")
        model_text.append(str(model.summary()))
        coefficient_frames.append(pd.DataFrame({
            "model": name,
            "term": model.params.index,
            "estimate": model.params.values,
            "std_error": model.bse.values,
        }))

    with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(model_text))

    pd.concat(coefficient_frames, ignore_index=True).to_csv(outputs / "model_coefficients.csv", index=False)


def simulate_safeguards(outputs: Path, n_groups: int = 1000, periods: int = 12, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    scenarios = ["unstructured_crisis", "directive_leader", "devils_advocate", "outside_experts", "red_team", "second_chance_meeting"]

    for scenario in scenarios:
        for group in range(1, n_groups + 1):
            if scenario == "unstructured_crisis":
                risk, safeguards, stress, dissent = 7.5, 2.5, 8.5, 2.5
            elif scenario == "directive_leader":
                risk, safeguards, stress, dissent = 8.0, 2.0, 7.0, 2.0
            elif scenario == "devils_advocate":
                risk, safeguards, stress, dissent = 5.0, 7.0, 6.0, 7.5
            elif scenario == "outside_experts":
                risk, safeguards, stress, dissent = 4.5, 7.8, 6.0, 7.2
            elif scenario == "red_team":
                risk, safeguards, stress, dissent = 4.0, 8.5, 6.5, 8.5
            else:
                risk, safeguards, stress, dissent = 4.2, 8.0, 7.0, 8.0

            quality = np.clip(rng.normal(60, 8), 0, 100)
            for period in range(1, periods + 1):
                consensus_pressure = np.clip(risk + 0.15 * period + rng.normal(0, 0.8), 0, 10)
                self_censorship = np.clip(0.65 * risk + 0.45 * stress + 0.55 * consensus_pressure - 0.60 * safeguards - 0.45 * dissent + rng.normal(0, 1.0), 0, 10)
                quality = np.clip(quality - 2.2 * risk - 1.5 * self_censorship + 2.8 * safeguards + 2.0 * dissent + rng.normal(0, 5), 0, 100)
                implementation_risk = np.clip(75 + 2.5 * risk + 2.0 * self_censorship - 2.5 * safeguards - 1.8 * dissent + rng.normal(0, 6), 0, 100)

                rows.append({
                    "scenario": scenario,
                    "group": group,
                    "period": period,
                    "groupthink_risk": risk,
                    "safeguards": safeguards,
                    "stress": stress,
                    "dissent_visibility": dissent,
                    "consensus_pressure": consensus_pressure,
                    "self_censorship": self_censorship,
                    "decision_quality": quality,
                    "implementation_risk": implementation_risk,
                })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby(["scenario", "period"])
        .agg(
            mean_groupthink_risk=("groupthink_risk", "mean"),
            mean_safeguards=("safeguards", "mean"),
            mean_self_censorship=("self_censorship", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
            mean_implementation_risk=("implementation_risk", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "groupthink_safeguard_simulation.csv", index=False)
    summary.to_csv(outputs / "groupthink_safeguard_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/groupthink_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=720)
    parser.add_argument("--trials", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulate:
        df = generate_dataset(n_participants=args.participants, trials_per_participant=args.trials, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote simulated dataset: {args.output}")
    elif args.input:
        df = pd.read_csv(args.input)
    else:
        default_input = Path("data/groupthink_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_safeguards(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
