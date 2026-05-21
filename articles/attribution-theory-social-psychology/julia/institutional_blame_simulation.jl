#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function run_simulation(; steps=80, seed=42, output_path="../outputs/julia_institutional_blame_simulation.csv")
    rng = MersenneTwister(seed)
    scenarios = [
        "low_system_visibility",
        "high_system_visibility",
        "accountability_review",
        "individual_blame_culture",
        "systems_learning_culture"
    ]
    rows = Any[]

    for scenario in scenarios
        individual_blame = 0.65
        system_attribution = 0.35

        for step in 1:steps
            if scenario == "low_system_visibility"
                actor_salience, system_visibility, accountability = 0.85, 0.20, 0.25
            elseif scenario == "high_system_visibility"
                actor_salience, system_visibility, accountability = 0.45, 0.75, 0.55
            elseif scenario == "accountability_review"
                actor_salience, system_visibility, accountability = 0.45, 0.80, 0.85
            elseif scenario == "individual_blame_culture"
                actor_salience, system_visibility, accountability = 0.90, 0.15, 0.20
            else
                actor_salience, system_visibility, accountability = 0.35, 0.90, 0.90
            end

            blame_pressure = actor_salience - system_visibility - 0.35 * accountability
            individual_blame = clamp(individual_blame + 0.05 * blame_pressure + randn(rng) * 0.025, 0.0, 1.0)
            system_attribution = clamp(system_attribution + 0.05 * (system_visibility + accountability - actor_salience) + randn(rng) * 0.025, 0.0, 1.0)
            learning_quality = clamp(0.25 + 0.45 * system_attribution + 0.25 * accountability - 0.25 * individual_blame, 0.0, 1.0)

            push!(rows, [scenario, step, individual_blame, system_attribution, learning_quality, actor_salience, system_visibility, accountability])
        end
    end

    header = ["scenario" "step" "individual_blame" "system_attribution" "learning_quality" "actor_salience" "system_visibility" "accountability"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Institutional blame simulation complete. Output: %s\n", output_path)
end

run_simulation()
