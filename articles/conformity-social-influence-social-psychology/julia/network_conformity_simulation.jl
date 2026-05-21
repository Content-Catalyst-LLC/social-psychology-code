#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles
using Statistics

function run_simulation(; agents=500, steps=30, seed=42, output_path="../outputs/julia_network_conformity_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    scenarios = ["low_social_proof", "high_social_proof", "visible_dissent", "algorithmic_amplification", "consistent_minority"]

    for scenario in scenarios
        beliefs = randn(rng, agents)

        for step in 1:steps
            mean_belief = mean(beliefs)

            if scenario == "low_social_proof"
                influence, dissent = 0.10, 0.30
            elseif scenario == "high_social_proof"
                influence, dissent = 0.35, 0.10
            elseif scenario == "visible_dissent"
                influence, dissent = 0.18, 0.55
            elseif scenario == "algorithmic_amplification"
                influence, dissent = 0.48, 0.08
            else
                influence, dissent = 0.20, 0.45
            end

            minority_signal = scenario == "consistent_minority" ? -1.0 : 0.0
            beliefs = (1 - influence) .* beliefs .+ influence .* mean_belief .+ 0.12 .* minority_signal .* dissent .+ randn(rng, agents) .* 0.10
            conformity_index = 1.0 / (1.0 + var(beliefs))

            push!(rows, [scenario, step, mean(beliefs), var(beliefs), conformity_index, influence, dissent])
        end
    end

    header = ["scenario" "step" "mean_belief" "belief_variance" "conformity_index" "influence_weight" "dissent_visibility"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Network conformity simulation complete. Output: %s\n", output_path)
end

run_simulation()
