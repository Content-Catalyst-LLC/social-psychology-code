#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; decisions=10000, seed=42, output_path="../outputs/julia_cumulative_inequality_simulation.csv")
    rng = MersenneTwister(seed)
    scenarios = ["unstructured_discretion", "threat_salience", "structured_criteria", "accountability", "contact_and_structure"]
    rows = Any[]

    for scenario in scenarios
        cumulative = 0.0
        for decision in 1:decisions
            if scenario == "unstructured_discretion"
                disparity = 0.020 + randn(rng) * 0.055
            elseif scenario == "threat_salience"
                disparity = 0.035 + randn(rng) * 0.065
            elseif scenario == "structured_criteria"
                disparity = 0.006 + randn(rng) * 0.035
            elseif scenario == "accountability"
                disparity = 0.008 + randn(rng) * 0.038
            else
                disparity = 0.002 + randn(rng) * 0.030
            end

            cumulative += disparity
            if decision % 100 == 0
                push!(rows, [scenario, decision, disparity, cumulative])
            end
        end
    end

    header = ["scenario" "decision" "decision_disparity" "cumulative_disparity"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Cumulative inequality simulation complete. Output: %s\n", output_path)
end

run_simulation()
