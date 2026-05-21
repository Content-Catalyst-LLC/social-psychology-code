#!/usr/bin/env julia
using Random, DelimitedFiles, Printf

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_collective_effort_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    conditions = ["pooled_group", "identifiable_group", "high_accountability", "traceable_digital_team"]
    for condition in conditions
        for i in 1:cases
            group_size = condition == "pooled_group" || condition == "traceable_digital_team" ? 8 : 6
            ident = condition == "pooled_group" ? 2.0 : condition == "traceable_digital_team" ? 8.0 : 7.0
            acct = condition == "pooled_group" ? 2.0 : condition == "high_accountability" ? 9.0 : 7.5
            trace = condition == "traceable_digital_team" ? 9.0 : condition == "pooled_group" ? 0.0 : 3.0
            value = condition == "traceable_digital_team" ? 7.0 : 6.0
            instrumentality = clamp(2 + 0.3*ident + 0.25*acct + 0.2*value - 0.25*log(1+group_size), 0.0, 10.0)
            motivation_loss = clamp(3 + 1.5*log(1+group_size) - 0.8*ident - 0.8*acct - 0.6*value - 0.5*instrumentality - 0.4*trace + randn(rng)*2, 0.0, 40.0)
            solo = clamp(80 + randn(rng)*7, 0.0, 100.0)
            group = clamp(solo - motivation_loss + randn(rng)*3, 0.0, 100.0)
            push!(rows, [condition, group_size, ident, acct, value, trace, instrumentality, motivation_loss, solo, group, solo-group])
        end
    end
    mkpath(dirname(output_path))
    writedlm(output_path, vcat([["condition" "group_size" "identifiability" "accountability" "task_value" "digital_traceability" "perceived_instrumentality" "motivation_loss" "solo_effort" "group_effort" "effort_loss"]], rows), ",")
    @printf("Wrote %s\n", output_path)
end

run_simulation()
