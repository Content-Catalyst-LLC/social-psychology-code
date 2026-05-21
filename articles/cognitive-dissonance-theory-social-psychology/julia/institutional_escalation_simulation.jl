#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-x))
end

function run_simulation(; steps=80, seed=42, output_path="../outputs/julia_institutional_escalation_simulation.csv")
    rng = MersenneTwister(seed)
    scenarios = [
        "low_sunk_cost_high_accountability",
        "high_sunk_cost_low_accountability",
        "public_commitment_high_identity_threat",
        "evidence_review_with_oversight",
        "face_saving_reversal_pathway"
    ]
    rows = Any[]

    for scenario in scenarios
        commitment = 0.45

        for step in 1:steps
            if scenario == "low_sunk_cost_high_accountability"
                sunk, public, threat, evidence, accountability = 0.2, 0.2, 0.2, 0.8, 0.9
            elseif scenario == "high_sunk_cost_low_accountability"
                sunk, public, threat, evidence, accountability = 0.9, 0.8, 0.7, 0.8, 0.2
            elseif scenario == "public_commitment_high_identity_threat"
                sunk, public, threat, evidence, accountability = 0.7, 0.95, 0.95, 0.8, 0.3
            elseif scenario == "evidence_review_with_oversight"
                sunk, public, threat, evidence, accountability = 0.5, 0.5, 0.4, 0.9, 0.9
            else
                sunk, public, threat, evidence, accountability = 0.7, 0.8, 0.8, 0.8, 0.7
            end

            rationalization_pressure = sunk + public + threat - evidence - accountability
            commitment = clamp(commitment + 0.06 * rationalization_pressure + randn(rng) * 0.025, 0.0, 1.0)
            reversal_probability = logistic(-4.0 * (commitment - 0.5))

            push!(rows, [scenario, step, commitment, rationalization_pressure, reversal_probability, sunk, public, threat, evidence, accountability])
        end
    end

    header = ["scenario" "step" "commitment_escalation" "rationalization_pressure" "reversal_probability" "sunk_cost" "public_commitment" "identity_threat" "evidence_strength" "accountability"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Institutional escalation simulation complete. Output: %s\n", output_path)
end

run_simulation()
