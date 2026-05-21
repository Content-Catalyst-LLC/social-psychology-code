#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; steps=80, seed=42, output_path="../outputs/julia_institutional_bias_simulation.csv")
    rng = MersenneTwister(seed)
    scenarios = [
        "unstructured_judgment",
        "high_accountability",
        "calibration_feedback",
        "base_rate_prompting",
        "structured_decision_protocol"
    ]
    rows = Any[]

    for scenario in scenarios
        accumulated_error = 0.0
        calibration_error = 0.25

        for step in 1:steps
            if scenario == "unstructured_judgment"
                bias_pressure, discipline = 0.85, 0.15
            elseif scenario == "high_accountability"
                bias_pressure, discipline = 0.55, 0.65
            elseif scenario == "calibration_feedback"
                bias_pressure, discipline = 0.50, 0.75
            elseif scenario == "base_rate_prompting"
                bias_pressure, discipline = 0.45, 0.80
            else
                bias_pressure, discipline = 0.35, 0.90
            end

            decision_error = 0.02 + 0.10*bias_pressure - 0.08*discipline + randn(rng)*0.05
            accumulated_error += decision_error
            calibration_error = clamp(calibration_error + 0.04*bias_pressure - 0.05*discipline + randn(rng)*0.01, 0.0, 1.0)
            decision_quality = clamp(1.0 - abs(decision_error) - calibration_error/2 + 0.25*discipline, 0.0, 1.0)

            push!(rows, [scenario, step, decision_error, accumulated_error, calibration_error, decision_quality, bias_pressure, discipline])
        end
    end

    header = ["scenario" "step" "decision_error" "accumulated_error" "calibration_error" "decision_quality" "bias_pressure" "evidence_discipline"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Institutional bias simulation complete. Output: %s\n", output_path)
end

run_simulation()
