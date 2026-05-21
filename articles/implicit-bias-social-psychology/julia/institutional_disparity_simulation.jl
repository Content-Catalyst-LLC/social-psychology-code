#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; decisions=10000, seed=42, output_path="../outputs/julia_institutional_disparity_simulation.csv")
    rng = MersenneTwister(seed)
    scenarios = ["unstructured_discretion", "time_pressure", "accountability", "structured_decision_support", "combined_mitigation"]
    rows = Any[]

    for scenario in scenarios
        cumulative = 0.0
        for decision in 1:decisions
            if scenario == "unstructured_discretion"
                bias = 0.018 + randn(rng) * 0.060
            elseif scenario == "time_pressure"
                bias = 0.032 + randn(rng) * 0.070
            elseif scenario == "accountability"
                bias = 0.010 + randn(rng) * 0.050
            elseif scenario == "structured_decision_support"
                bias = 0.004 + randn(rng) * 0.040
            else
                bias = 0.002 + randn(rng) * 0.035
            end

            cumulative += bias
            if decision % 100 == 0
                push!(rows, [scenario, decision, bias, cumulative])
            end
        end
    end

    header = ["scenario" "decision" "mean_bias_contribution" "cumulative_disparity"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Institutional disparity simulation complete. Output: %s\n", output_path)
end

run_simulation()
